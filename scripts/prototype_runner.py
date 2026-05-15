"""Validate prospect research prototype fixture packages.

This runner intentionally uses only the Python standard library so it can run
in a fresh workspace before dependency decisions are made.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ALLOWED_VALUES = {
    "profile_type": {"individual", "organisation"},
    "output_length": {"short", "standard", "detailed", "comprehensive"},
    "source_scope": {"user_provided_only", "public_web_allowed", "internal_sources_allowed"},
    "subject_type": {"individual", "organisation"},
    "identity_status": {"confirmed", "probable", "ambiguous", "unconfirmed"},
    "uc_connection_status": {"confirmed", "not_confirmed", "contradicted", "unknown"},
    "source_type": {
        "official",
        "public_web",
        "user_provided",
        "internal",
        "registry",
        "news",
        "social",
        "database",
        "other",
    },
    "source_visibility": {"public", "internal", "confidential", "unknown"},
    "reliability_tier": {"primary", "strong_secondary", "secondary", "weak", "unknown"},
    "recency_status": {"current", "recent", "dated", "stale", "unknown"},
    "subject_match": {"direct", "probable", "ambiguous", "no_match"},
    "topic": {
        "identity",
        "current_role",
        "career_background",
        "organisation_overview",
        "leadership",
        "uc_connection",
        "philanthropy",
        "community_activity",
        "capacity_indicator",
        "interest_alignment",
        "sensitivity",
        "source_limitation",
        "absence",
        "contradiction",
    },
    "claim_type": {"fact", "inference", "absence", "contradiction", "limitation"},
    "evidence_strength": {"strong", "adequate", "limited", "weak", "none"},
    "confidence": {"high", "medium", "low", "excluded"},
    "identity_link": {"direct", "probable", "ambiguous", "not_established"},
    "inclusion_status": {"include", "include_softened", "internal_only", "exclude", "needs_review"},
    "review_status": {"unreviewed", "reviewed", "challenged", "approved", "rejected"},
    "sensitivity_level": {"none", "low", "medium", "high", "restricted"},
}

REQUIRED_TOP_LEVEL = ("profile_request", "subject", "sources", "claims")
REQUIRED_REQUEST_FIELDS = ("request_id", "requested_at", "profile_type", "output_length", "source_scope")
REQUIRED_SUBJECT_FIELDS = (
    "subject_id",
    "subject_type",
    "display_name",
    "identity_status",
    "identity_risk",
    "uc_connection_status",
)
REQUIRED_SOURCE_FIELDS = (
    "source_id",
    "source_type",
    "title",
    "url_or_reference",
    "access_date",
    "publication_date",
    "source_visibility",
    "reliability_tier",
    "recency_status",
    "subject_match",
    "contains_private_data",
    "contains_sensitive_data",
)
REQUIRED_CLAIM_FIELDS = (
    "claim_id",
    "subject_id",
    "topic",
    "claim_type",
    "text",
    "source_ids",
    "evidence_strength",
    "confidence",
    "confidence_reason",
    "identity_link",
    "source_recency",
    "sensitivity",
    "privacy",
    "inclusion",
    "review_status",
)

UNSUPPORTED_CAPACITY_TERMS = (
    "high-net-worth",
    "major donor",
    "likely donor",
    "giving capacity",
    "donor likelihood",
    "likely a major donor",
    "strong affinity",
)


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    claim_id: str | None = None


@dataclass
class ValidationReport:
    path: str
    valid: bool = True
    findings: list[Finding] = field(default_factory=list)
    claim_summary: dict[str, int] = field(
        default_factory=lambda: {
            "include": 0,
            "include_softened": 0,
            "internal_only": 0,
            "exclude": 0,
            "needs_review": 0,
            "unknown": 0,
        }
    )
    source_summary: dict[str, int] = field(default_factory=lambda: {"total": 0, "ambiguous": 0, "weak": 0})

    def add(self, severity: str, code: str, message: str, claim_id: str | None = None) -> None:
        self.findings.append(Finding(severity, code, message, claim_id))
        if severity == "error":
            self.valid = False


@dataclass
class DraftProfile:
    path: str
    subject_name: str
    profile_type: str
    sections: list[dict[str, Any]]
    omitted_claim_ids: list[str]


class TinyYamlError(ValueError):
    pass


def strip_comment(line: str) -> str:
    in_quote: str | None = None
    escaped = False
    for idx, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char in {"'", '"'}:
            in_quote = None if in_quote == char else char if in_quote is None else in_quote
        if char == "#" and in_quote is None:
            return line[:idx].rstrip()
    return line.rstrip()


def load_tiny_yaml(path: Path) -> Any:
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    lines: list[tuple[int, str]] = []
    for raw in raw_lines:
        cleaned = strip_comment(raw)
        if not cleaned.strip():
            continue
        indent = len(cleaned) - len(cleaned.lstrip(" "))
        if indent % 2 != 0:
            raise TinyYamlError(f"Unsupported odd indentation: {raw!r}")
        lines.append((indent, cleaned.strip()))
    if not lines:
        return {}
    value, index = parse_block(lines, 0, lines[0][0])
    if index != len(lines):
        raise TinyYamlError(f"Could not parse line {index + 1}: {lines[index][1]}")
    return value


def parse_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    current_indent, text = lines[index]
    if current_indent < indent:
        return {}, index
    if current_indent != indent:
        raise TinyYamlError(f"Expected indent {indent}, got {current_indent}: {text}")
    if text.startswith("- "):
        return parse_list(lines, index, indent)
    return parse_mapping(lines, index, indent)


def parse_mapping(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise TinyYamlError(f"Unexpected nested mapping line: {text}")
        if text.startswith("- "):
            break
        key, raw_value = split_key_value(text)
        index += 1
        if raw_value == "":
            if index < len(lines) and lines[index][0] > indent:
                value, index = parse_block(lines, index, lines[index][0])
            else:
                value = None
        else:
            value = parse_scalar(raw_value)
        result[key] = value
    return result, index


def parse_list(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[list[Any], int]:
    result: list[Any] = []
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent != indent or not text.startswith("- "):
            break
        item_text = text[2:].strip()
        index += 1
        if item_text == "":
            if index < len(lines) and lines[index][0] > indent:
                item, index = parse_block(lines, index, lines[index][0])
            else:
                item = None
            result.append(item)
            continue
        if looks_like_key_value(item_text):
            key, raw_value = split_key_value(item_text)
            item_dict: dict[str, Any] = {key: parse_scalar(raw_value) if raw_value else None}
            if index < len(lines) and lines[index][0] > indent:
                nested, index = parse_mapping(lines, index, lines[index][0])
                item_dict.update(nested)
            result.append(item_dict)
        else:
            result.append(parse_scalar(item_text))
    return result, index


def looks_like_key_value(text: str) -> bool:
    return bool(re.match(r"^[A-Za-z0-9_]+:\s*", text))


def split_key_value(text: str) -> tuple[str, str]:
    if ":" not in text:
        raise TinyYamlError(f"Expected key/value pair: {text}")
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        raise TinyYamlError(f"Empty key in line: {text}")
    return key, value.strip()


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value in {"true", "false"}:
        return value == "true"
    if value in {"null", "~"}:
        return None
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in split_inline_list(inner)]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def split_inline_list(value: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    in_quote: str | None = None
    escaped = False
    for char in value:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            current.append(char)
            escaped = True
            continue
        if char in {"'", '"'}:
            in_quote = None if in_quote == char else char if in_quote is None else in_quote
            current.append(char)
            continue
        if char == "," and in_quote is None:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    parts.append("".join(current).strip())
    return parts


def validate_package(data: dict[str, Any], path: Path) -> ValidationReport:
    report = ValidationReport(path=str(path))
    if not isinstance(data, dict):
        report.add("error", "package.not_mapping", "Fixture must be a top-level mapping.")
        return report

    for field_name in REQUIRED_TOP_LEVEL:
        if field_name not in data:
            report.add("error", "package.missing_top_level", f"Missing top-level field `{field_name}`.")

    request = require_mapping(data.get("profile_request"), "profile_request", report)
    subject = require_mapping(data.get("subject"), "subject", report)
    sources = require_list(data.get("sources"), "sources", report)
    claims = require_list(data.get("claims"), "claims", report)
    profile_output = data.get("profile_output")
    if profile_output is not None and not isinstance(profile_output, dict):
        report.add("error", "profile_output.not_mapping", "`profile_output` must be a mapping when present.")

    validate_required_fields(request, REQUIRED_REQUEST_FIELDS, "profile_request", report)
    validate_required_fields(subject, REQUIRED_SUBJECT_FIELDS, "subject", report)
    validate_allowed(request.get("profile_type"), "profile_type", "profile_request.profile_type", report)
    validate_allowed(request.get("output_length"), "output_length", "profile_request.output_length", report)
    validate_allowed(request.get("source_scope"), "source_scope", "profile_request.source_scope", report)
    validate_allowed(subject.get("subject_type"), "subject_type", "subject.subject_type", report)
    validate_allowed(subject.get("identity_status"), "identity_status", "subject.identity_status", report)
    validate_allowed(subject.get("uc_connection_status"), "uc_connection_status", "subject.uc_connection_status", report)

    if request.get("profile_type") and subject.get("subject_type") and request["profile_type"] != subject["subject_type"]:
        report.add("error", "subject.profile_type_mismatch", "`profile_type` must match `subject_type`.")

    source_by_id = validate_sources(sources, report)
    validate_claims(claims, source_by_id, subject, report)
    validate_profile_output(profile_output, {claim.get("claim_id"): claim for claim in claims if isinstance(claim, dict)}, report)
    return report


def require_mapping(value: Any, name: str, report: ValidationReport) -> dict[str, Any]:
    if not isinstance(value, dict):
        report.add("error", f"{name}.not_mapping", f"`{name}` must be a mapping.")
        return {}
    return value


def require_list(value: Any, name: str, report: ValidationReport) -> list[Any]:
    if not isinstance(value, list):
        report.add("error", f"{name}.not_list", f"`{name}` must be a list.")
        return []
    return value


def validate_required_fields(data: dict[str, Any], required: tuple[str, ...], context: str, report: ValidationReport) -> None:
    for field_name in required:
        if field_name not in data:
            report.add("error", f"{context}.missing_field", f"`{context}` missing `{field_name}`.")


def validate_allowed(value: Any, key: str, context: str, report: ValidationReport, claim_id: str | None = None) -> None:
    if value is None:
        return
    allowed = ALLOWED_VALUES[key]
    if value not in allowed:
        report.add("error", f"{context}.invalid_value", f"`{context}` has invalid value `{value}`.", claim_id)


def validate_sources(sources: list[Any], report: ValidationReport) -> dict[str, dict[str, Any]]:
    source_by_id: dict[str, dict[str, Any]] = {}
    report.source_summary["total"] = len(sources)
    for index, source in enumerate(sources, start=1):
        context = f"sources[{index}]"
        if not isinstance(source, dict):
            report.add("error", "source.not_mapping", f"`{context}` must be a mapping.")
            continue
        validate_required_fields(source, REQUIRED_SOURCE_FIELDS, context, report)
        source_id = source.get("source_id")
        if isinstance(source_id, str):
            if source_id in source_by_id:
                report.add("error", "source.duplicate_id", f"Duplicate source_id `{source_id}`.")
            source_by_id[source_id] = source
        validate_allowed(source.get("source_type"), "source_type", f"{context}.source_type", report)
        validate_allowed(source.get("source_visibility"), "source_visibility", f"{context}.source_visibility", report)
        validate_allowed(source.get("reliability_tier"), "reliability_tier", f"{context}.reliability_tier", report)
        validate_allowed(source.get("recency_status"), "recency_status", f"{context}.recency_status", report)
        validate_allowed(source.get("subject_match"), "subject_match", f"{context}.subject_match", report)
        if source.get("subject_match") == "ambiguous":
            report.source_summary["ambiguous"] += 1
        if source.get("reliability_tier") == "weak":
            report.source_summary["weak"] += 1
        if source.get("subject_match") in {"ambiguous", "no_match"}:
            report.add("warning", "source.subject_match_risk", f"Source `{source_id}` has subject match `{source.get('subject_match')}`.")
    return source_by_id


def validate_claims(
    claims: list[Any],
    source_by_id: dict[str, dict[str, Any]],
    subject: dict[str, Any],
    report: ValidationReport,
) -> None:
    seen_claim_ids: set[str] = set()
    for index, claim in enumerate(claims, start=1):
        context = f"claims[{index}]"
        if not isinstance(claim, dict):
            report.add("error", "claim.not_mapping", f"`{context}` must be a mapping.")
            continue
        claim_id = claim.get("claim_id")
        if isinstance(claim_id, str):
            if claim_id in seen_claim_ids:
                report.add("error", "claim.duplicate_id", f"Duplicate claim_id `{claim_id}`.", claim_id)
            seen_claim_ids.add(claim_id)
        else:
            claim_id = None
        validate_required_fields(claim, REQUIRED_CLAIM_FIELDS, context, report)
        validate_allowed(claim.get("topic"), "topic", f"{context}.topic", report, claim_id)
        validate_allowed(claim.get("claim_type"), "claim_type", f"{context}.claim_type", report, claim_id)
        validate_allowed(claim.get("evidence_strength"), "evidence_strength", f"{context}.evidence_strength", report, claim_id)
        validate_allowed(claim.get("confidence"), "confidence", f"{context}.confidence", report, claim_id)
        validate_allowed(claim.get("identity_link"), "identity_link", f"{context}.identity_link", report, claim_id)
        validate_allowed(claim.get("source_recency"), "recency_status", f"{context}.source_recency", report, claim_id)
        validate_allowed(claim.get("review_status"), "review_status", f"{context}.review_status", report, claim_id)

        inclusion = claim.get("inclusion") if isinstance(claim.get("inclusion"), dict) else {}
        privacy = claim.get("privacy") if isinstance(claim.get("privacy"), dict) else {}
        sensitivity = claim.get("sensitivity") if isinstance(claim.get("sensitivity"), dict) else {}
        inclusion_status = inclusion.get("status")
        if inclusion_status in report.claim_summary:
            report.claim_summary[inclusion_status] += 1
        else:
            report.claim_summary["unknown"] += 1
        validate_allowed(inclusion_status, "inclusion_status", f"{context}.inclusion.status", report, claim_id)
        validate_allowed(sensitivity.get("level"), "sensitivity_level", f"{context}.sensitivity.level", report, claim_id)

        source_ids = claim.get("source_ids")
        if not source_ids:
            report.add("error", "claim.no_sources", "Claim must have at least one source_id.", claim_id)
        elif not isinstance(source_ids, list):
            report.add("error", "claim.source_ids_not_list", "`source_ids` must be a list.", claim_id)
        else:
            missing = [source_id for source_id in source_ids if source_id not in source_by_id]
            if missing:
                report.add("error", "claim.unknown_source", f"Claim references unknown sources: {', '.join(missing)}.", claim_id)
            risky_sources = [
                source_id
                for source_id in source_ids
                if source_id in source_by_id and source_by_id[source_id].get("subject_match") in {"ambiguous", "no_match"}
            ]
            if risky_sources and inclusion_status in {"include", "include_softened"}:
                report.add(
                    "error",
                    "claim.risky_source_included",
                    f"Included claim is supported by ambiguous/no-match sources: {', '.join(risky_sources)}.",
                    claim_id,
                )

        if claim.get("confidence") == "high" and claim.get("evidence_strength") in {"weak", "none"}:
            report.add("error", "claim.high_confidence_weak_evidence", "High confidence cannot rely on weak/no evidence.", claim_id)
        if inclusion_status == "include" and claim.get("review_status") != "approved":
            report.add("error", "claim.include_not_approved", "Included claim must have review_status `approved`.", claim_id)
        if inclusion_status == "include" and privacy.get("final_output_allowed") is False:
            report.add("error", "claim.include_private_blocked", "Included claim cannot have final_output_allowed false.", claim_id)
        if claim.get("topic") == "uc_connection" and claim.get("claim_type") == "inference":
            report.add("error", "claim.uc_connection_inferred", "UC connection claims cannot be inference-only.", claim_id)
        if subject.get("identity_status") == "ambiguous" and inclusion_status in {"include", "include_softened"}:
            report.add("error", "claim.included_with_ambiguous_subject", "Do not include claims while subject identity is ambiguous.", claim_id)
        if claim.get("confidence") == "low" and inclusion_status in {"include", "include_softened"}:
            report.add("error", "claim.low_confidence_included", "Low-confidence claims cannot be final-output claims.", claim_id)
        if claim.get("confidence") == "excluded" and inclusion_status not in {"exclude", "internal_only"}:
            report.add("error", "claim.excluded_confidence_not_excluded", "Excluded confidence must use exclude/internal_only status.", claim_id)
        if privacy.get("donor_level_data") is True and inclusion_status in {"include", "include_softened"}:
            report.add("error", "claim.donor_data_included", "Donor-level data cannot be included in final output.", claim_id)
        if claim.get("topic") == "capacity_indicator" and contains_unsupported_capacity_language(str(claim.get("text", ""))):
            if inclusion_status in {"include", "include_softened"}:
                report.add("error", "claim.unsupported_capacity_included", "Unsupported capacity language cannot be included.", claim_id)
            else:
                report.add("info", "claim.unsupported_capacity_detected", "Unsupported capacity language detected and blocked.", claim_id)


def contains_unsupported_capacity_language(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in UNSUPPORTED_CAPACITY_TERMS)


def validate_profile_output(
    profile_output: Any,
    claim_by_id: dict[str, dict[str, Any]],
    report: ValidationReport,
) -> None:
    if not isinstance(profile_output, dict):
        return
    final_checks = profile_output.get("final_checks")
    if final_checks is not None:
        if not isinstance(final_checks, dict):
            report.add("error", "profile_output.final_checks_not_mapping", "`final_checks` must be a mapping.")
        else:
            false_checks = [key for key, value in final_checks.items() if value is not True]
            if false_checks:
                report.add("error", "profile_output.final_checks_false", f"Final checks must all be true: {', '.join(false_checks)}.")
    sections = profile_output.get("sections") or []
    if not isinstance(sections, list):
        report.add("error", "profile_output.sections_not_list", "`sections` must be a list.")
        return
    for section in sections:
        if not isinstance(section, dict):
            report.add("error", "profile_output.section_not_mapping", "Each section must be a mapping.")
            continue
        for claim_id in section.get("supporting_claim_ids", []) or []:
            claim = claim_by_id.get(claim_id)
            if claim is None:
                report.add("error", "profile_output.unknown_supporting_claim", f"Section references unknown claim `{claim_id}`.")
                continue
            inclusion = claim.get("inclusion") if isinstance(claim.get("inclusion"), dict) else {}
            if inclusion.get("status") in {"exclude", "internal_only", "needs_review"}:
                report.add(
                    "error",
                    "profile_output.blocked_claim_referenced",
                    f"Section references blocked claim `{claim_id}`.",
                    claim_id,
                )


def report_to_dict(report: ValidationReport) -> dict[str, Any]:
    return {
        "path": report.path,
        "valid": report.valid,
        "source_summary": report.source_summary,
        "claim_summary": report.claim_summary,
        "findings": [finding.__dict__ for finding in report.findings],
    }


def format_text_report(report: ValidationReport) -> str:
    lines = [
        f"Fixture: {report.path}",
        f"Valid: {'yes' if report.valid else 'no'}",
        (
            "Claims: "
            f"include={report.claim_summary['include']}, "
            f"include_softened={report.claim_summary['include_softened']}, "
            f"internal_only={report.claim_summary['internal_only']}, "
            f"exclude={report.claim_summary['exclude']}, "
            f"needs_review={report.claim_summary['needs_review']}"
        ),
        (
            "Sources: "
            f"total={report.source_summary['total']}, "
            f"ambiguous={report.source_summary['ambiguous']}, "
            f"weak={report.source_summary['weak']}"
        ),
    ]
    if report.findings:
        lines.append("Findings:")
        for finding in report.findings:
            claim = f" [{finding.claim_id}]" if finding.claim_id else ""
            lines.append(f"- {finding.severity.upper()} {finding.code}{claim}: {finding.message}")
    else:
        lines.append("Findings: none")
    return "\n".join(lines)


def validate_path(path: Path) -> ValidationReport:
    try:
        data = load_tiny_yaml(path)
    except Exception as exc:
        report = ValidationReport(path=str(path), valid=False)
        report.add("error", "yaml.parse_error", str(exc))
        return report
    return validate_package(data, path)


def load_package(path: Path) -> dict[str, Any]:
    data = load_tiny_yaml(path)
    if not isinstance(data, dict):
        raise TinyYamlError("Fixture must be a top-level mapping.")
    return data


def eligible_for_draft(claim: dict[str, Any], subject: dict[str, Any]) -> bool:
    inclusion = claim.get("inclusion") if isinstance(claim.get("inclusion"), dict) else {}
    privacy = claim.get("privacy") if isinstance(claim.get("privacy"), dict) else {}
    sensitivity = claim.get("sensitivity") if isinstance(claim.get("sensitivity"), dict) else {}
    inclusion_status = inclusion.get("status")

    if inclusion_status not in {"include", "include_softened"}:
        return False
    if claim.get("review_status") != "approved":
        return False
    if claim.get("confidence") in {"low", "excluded"}:
        return False
    if privacy.get("final_output_allowed") is False:
        return False
    if privacy.get("donor_level_data") is True:
        return False
    if subject.get("identity_status") == "ambiguous":
        return False
    if claim.get("identity_link") in {"ambiguous", "not_established"}:
        return False
    if sensitivity.get("level") in {"high", "restricted"}:
        return False
    if claim.get("topic") == "uc_connection" and claim.get("claim_type") == "inference":
        return False
    if claim.get("topic") == "capacity_indicator" and contains_unsupported_capacity_language(str(claim.get("text", ""))):
        return False
    return True


def section_title(profile_type: str, section_id: str) -> str:
    individual_titles = {
        "snapshot": "Snapshot",
        "current_roles": "Current Roles and Public Profile",
        "current_role": "Current Roles and Public Profile",
        "confirmed_uc_connection": "Connection to UC",
        "uc_connection": "Connection to UC",
        "philanthropy": "Philanthropy and Community Involvement",
        "community_activity": "Philanthropy and Community Involvement",
        "professional_and_wealth_indicators": "Professional and Capacity Indicators",
        "capacity_indicator": "Professional and Capacity Indicators",
        "interest_alignment": "Interests and Alignment",
        "sensitivity": "Due Diligence and Sensitivities",
    }
    organisation_titles = {
        "snapshot": "Snapshot",
        "organisation_overview": "Organisation Overview",
        "leadership": "Leadership and Key People",
        "confirmed_uc_connection": "Confirmed UC Connection",
        "uc_connection": "Confirmed UC Connection",
        "philanthropy": "Philanthropy, Sponsorship, and Community Activity",
        "community_activity": "Philanthropy, Sponsorship, and Community Activity",
        "sector_position_and_partnership_relevance": "Sector Position and Partnership Relevance",
        "interest_alignment": "Sector Position and Partnership Relevance",
        "capacity_indicator": "Capacity and Resourcing Indicators",
        "sensitivity": "Sensitivities and Due Diligence",
    }
    titles = organisation_titles if profile_type == "organisation" else individual_titles
    return titles.get(section_id, section_id.replace("_", " ").title())


def section_order(profile_type: str) -> list[str]:
    if profile_type == "organisation":
        return [
            "snapshot",
            "organisation_overview",
            "leadership",
            "confirmed_uc_connection",
            "uc_connection",
            "philanthropy",
            "community_activity",
            "sector_position_and_partnership_relevance",
            "interest_alignment",
            "capacity_indicator",
            "sensitivity",
        ]
    return [
        "snapshot",
        "current_roles",
        "current_role",
        "confirmed_uc_connection",
        "uc_connection",
        "philanthropy",
        "community_activity",
        "professional_and_wealth_indicators",
        "capacity_indicator",
        "interest_alignment",
        "sensitivity",
    ]


def draft_profile(data: dict[str, Any], path: Path) -> DraftProfile:
    subject = data.get("subject") if isinstance(data.get("subject"), dict) else {}
    request = data.get("profile_request") if isinstance(data.get("profile_request"), dict) else {}
    claims = data.get("claims") if isinstance(data.get("claims"), list) else []
    profile_type = str(request.get("profile_type") or subject.get("subject_type") or "individual")
    subject_name = str(subject.get("display_name") or "Untitled Subject")
    grouped: dict[str, list[dict[str, Any]]] = {}
    omitted: list[str] = []

    for claim in claims:
        if not isinstance(claim, dict):
            continue
        claim_id = str(claim.get("claim_id") or "")
        if not eligible_for_draft(claim, subject):
            if claim_id:
                omitted.append(claim_id)
            continue
        inclusion = claim.get("inclusion") if isinstance(claim.get("inclusion"), dict) else {}
        section_id = str(inclusion.get("profile_section") or claim.get("topic") or "other")
        grouped.setdefault(section_id, []).append(claim)

    ordered_ids = [section_id for section_id in section_order(profile_type) if section_id in grouped]
    ordered_ids.extend(section_id for section_id in grouped if section_id not in ordered_ids)

    sections: list[dict[str, Any]] = []
    for section_id in ordered_ids:
        section_claims = grouped[section_id]
        sections.append(
            {
                "section_id": section_id,
                "heading": section_title(profile_type, section_id),
                "claims": section_claims,
                "supporting_claim_ids": [claim.get("claim_id") for claim in section_claims],
            }
        )

    return DraftProfile(
        path=str(path),
        subject_name=subject_name,
        profile_type=profile_type,
        sections=sections,
        omitted_claim_ids=omitted,
    )


def render_draft_markdown(draft: DraftProfile) -> str:
    lines = [
        f"# Draft Profile: {draft.subject_name}",
        "",
        f"Profile type: {draft.profile_type}",
        "",
        "This is a structured draft generated only from claims that passed the prototype safety filter.",
        "",
    ]
    if not draft.sections:
        lines.extend(["No claims are currently eligible for draft output.", ""])
    for section in draft.sections:
        lines.extend([f"## {section['heading']}", ""])
        for claim in section["claims"]:
            inclusion = claim.get("inclusion") if isinstance(claim.get("inclusion"), dict) else {}
            status = inclusion.get("status")
            prefix = "Softened: " if status == "include_softened" else ""
            guidance = inclusion.get("wording_guidance")
            lines.append(f"- {prefix}{claim.get('text')}")
            if status == "include_softened" and guidance:
                lines.append(f"  - Wording guidance: {guidance}")
        lines.append("")
    if draft.omitted_claim_ids:
        lines.extend(["## Omitted Internal Claims", ""])
        lines.append("The following claims were not eligible for draft output:")
        for claim_id in draft.omitted_claim_ids:
            lines.append(f"- {claim_id}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def iter_fixture_paths(paths: list[Path]) -> list[Path]:
    expanded: list[Path] = []
    for path in paths:
        if path.is_dir():
            expanded.extend(sorted(path.glob("*.yaml")))
        else:
            expanded.append(path)
    return expanded


def output_directory_for_fixture(base_dir: Path, fixture_path: Path) -> Path:
    return base_dir / fixture_path.stem


def write_outputs(base_dir: Path, fixture_path: Path, report: ValidationReport, draft: DraftProfile) -> None:
    target_dir = output_directory_for_fixture(base_dir, fixture_path)
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "review-report.json").write_text(json.dumps(report_to_dict(report), indent=2), encoding="utf-8")
    (target_dir / "draft-profile.md").write_text(render_draft_markdown(draft), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate prospect research prototype fixtures.")
    parser.add_argument("paths", nargs="+", type=Path, help="Fixture YAML file or directory to validate.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument("--draft", action="store_true", help="Include draft profile markdown in text output.")
    parser.add_argument("--output-dir", type=Path, help="Write review-report.json and draft-profile.md under this directory.")
    args = parser.parse_args(argv)

    fixture_paths = iter_fixture_paths(args.paths)
    reports = [validate_path(path) for path in fixture_paths]
    drafts: list[DraftProfile] = []
    for fixture_path in fixture_paths:
        try:
            drafts.append(draft_profile(load_package(fixture_path), fixture_path))
        except Exception:
            drafts.append(DraftProfile(str(fixture_path), "Unknown Subject", "unknown", [], []))
    if args.output_dir:
        for fixture_path, report, draft in zip(fixture_paths, reports, drafts):
            write_outputs(args.output_dir, fixture_path, report, draft)
    if args.json:
        print(json.dumps([report_to_dict(report) for report in reports], indent=2))
    else:
        for idx, (report, draft) in enumerate(zip(reports, drafts)):
            if idx:
                print()
            print(format_text_report(report))
            if args.draft:
                print()
                print(render_draft_markdown(draft).rstrip())
    return 0 if all(report.valid for report in reports) else 1


if __name__ == "__main__":
    sys.exit(main())

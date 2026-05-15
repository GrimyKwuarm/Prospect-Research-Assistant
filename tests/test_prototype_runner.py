import tempfile
import unittest
from pathlib import Path

from scripts.prototype_runner import (
    draft_profile,
    load_package,
    load_tiny_yaml,
    render_draft_markdown,
    validate_path,
    write_outputs,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"


class TinyYamlTests(unittest.TestCase):
    def test_loads_fixture_shape(self):
        data = load_tiny_yaml(FIXTURES / "confirmed-uc-connection.yaml")
        self.assertEqual(data["subject"]["display_name"], "Dr Elena Rivers")
        self.assertEqual(data["claims"][1]["topic"], "uc_connection")
        self.assertEqual(data["claims"][0]["privacy"]["final_output_allowed"], True)


class FixtureValidationTests(unittest.TestCase):
    def test_confirmed_uc_fixture_passes(self):
        report = validate_path(FIXTURES / "confirmed-uc-connection.yaml")
        self.assertTrue(report.valid, report.findings)
        self.assertEqual(report.claim_summary["include"], 2)

    def test_no_confirmed_uc_fixture_passes(self):
        report = validate_path(FIXTURES / "no-confirmed-uc-connection.yaml")
        self.assertTrue(report.valid, report.findings)
        self.assertEqual(report.claim_summary["include"], 2)

    def test_ambiguous_identity_is_blocked_but_valid_fixture(self):
        report = validate_path(FIXTURES / "ambiguous-identity.yaml")
        self.assertTrue(report.valid, report.findings)
        self.assertEqual(report.claim_summary["needs_review"], 1)
        self.assertTrue(any(f.code == "source.subject_match_risk" for f in report.findings))

    def test_unsupported_capacity_is_detected_and_blocked(self):
        report = validate_path(FIXTURES / "unsupported-capacity-claim.yaml")
        self.assertTrue(report.valid, report.findings)
        self.assertEqual(report.claim_summary["exclude"], 1)
        self.assertTrue(any(f.code == "claim.unsupported_capacity_detected" for f in report.findings))

    def test_sector_relevance_without_uc_passes_with_softened_claim(self):
        report = validate_path(FIXTURES / "organisation-sector-relevance-no-uc.yaml")
        self.assertTrue(report.valid, report.findings)
        self.assertEqual(report.claim_summary["include_softened"], 1)

    def test_included_unapproved_claim_fails(self):
        fixture = """
profile_request:
  request_id: "bad_001"
  requested_at: "2026-05-15T09:00:00+12:00"
  profile_type: "individual"
  output_length: "short"
  source_scope: "user_provided_only"
subject:
  subject_id: "subj_001"
  subject_type: "individual"
  display_name: "Bad Fixture"
  identity_status: "confirmed"
  identity_risk:
    level: "low"
    notes: "Test"
  uc_connection_status: "unknown"
sources:
  - source_id: "src_001"
    source_type: "user_provided"
    title: "Note"
    url_or_reference: "fixture"
    access_date: "2026-05-15"
    publication_date: "unknown"
    source_visibility: "internal"
    reliability_tier: "primary"
    recency_status: "unknown"
    subject_match: "direct"
    contains_private_data: false
    contains_sensitive_data: false
claims:
  - claim_id: "clm_001"
    subject_id: "subj_001"
    topic: "current_role"
    claim_type: "fact"
    text: "Bad Fixture is a director."
    source_ids: ["src_001"]
    evidence_strength: "adequate"
    confidence: "high"
    confidence_reason: "Test"
    identity_link: "direct"
    source_recency: "unknown"
    sensitivity:
      level: "none"
      categories: []
    privacy:
      contains_private_data: false
      donor_level_data: false
      final_output_allowed: true
    inclusion:
      status: "include"
      profile_section: "current_roles"
      wording_guidance: "State plainly."
      exclusion_reason: null
    review_status: "unreviewed"
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "bad.yaml"
            path.write_text(fixture, encoding="utf-8")
            report = validate_path(path)
        self.assertFalse(report.valid)
        self.assertTrue(any(f.code == "claim.include_not_approved" for f in report.findings))


class DraftGenerationTests(unittest.TestCase):
    def test_confirmed_uc_fixture_drafts_connection_section(self):
        path = FIXTURES / "confirmed-uc-connection.yaml"
        draft = draft_profile(load_package(path), path)
        rendered = render_draft_markdown(draft)
        self.assertIn("## Connection to UC", rendered)
        self.assertIn("Bachelor of Engineering with Honours at UC", rendered)

    def test_no_confirmed_uc_wording_is_drafted(self):
        path = FIXTURES / "no-confirmed-uc-connection.yaml"
        draft = draft_profile(load_package(path), path)
        rendered = render_draft_markdown(draft)
        self.assertIn("## Confirmed UC Connection", rendered)
        self.assertIn("No confirmed UC connection identified in the material reviewed.", rendered)

    def test_ambiguous_identity_claims_do_not_draft(self):
        path = FIXTURES / "ambiguous-identity.yaml"
        draft = draft_profile(load_package(path), path)
        rendered = render_draft_markdown(draft)
        self.assertEqual(draft.sections, [])
        self.assertIn("No claims are currently eligible for draft output.", rendered)
        self.assertIn("clm_001", draft.omitted_claim_ids)

    def test_excluded_capacity_claim_does_not_draft(self):
        path = FIXTURES / "unsupported-capacity-claim.yaml"
        draft = draft_profile(load_package(path), path)
        rendered = render_draft_markdown(draft)
        self.assertNotIn("likely a major donor prospect", rendered)
        self.assertIn("clm_001", draft.omitted_claim_ids)

    def test_softened_sector_relevance_is_labelled(self):
        path = FIXTURES / "organisation-sector-relevance-no-uc.yaml"
        draft = draft_profile(load_package(path), path)
        rendered = render_draft_markdown(draft)
        self.assertIn("## Sector Position and Partnership Relevance", rendered)
        self.assertIn("Softened: The organisation has sector relevance", rendered)
        self.assertIn("do not imply UC connection", rendered)

    def test_output_writer_creates_review_and_draft_files(self):
        path = FIXTURES / "confirmed-uc-connection.yaml"
        report = validate_path(path)
        draft = draft_profile(load_package(path), path)
        with tempfile.TemporaryDirectory() as temp_dir:
            write_outputs(Path(temp_dir), path, report, draft)
            output_dir = Path(temp_dir) / "confirmed-uc-connection"
            self.assertTrue((output_dir / "review-report.json").exists())
            self.assertTrue((output_dir / "draft-profile.md").exists())
            self.assertIn("Draft Profile", (output_dir / "draft-profile.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

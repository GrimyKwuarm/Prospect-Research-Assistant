---
name: source-quality-checker
description: Assess source reliability, recency, subject match, privacy risk, sensitivity risk, and claim eligibility for prospect research profiles. Use when Codex is reviewing supplied notes, public sources, internal references, source registers, or structured claims before drafting individual or organisation advancement profiles.
---

# Source Quality Checker

## Goal

Classify sources and claims before any profile drafting. Make unsafe or unsupported claims hard to pass into final prose.

## Required Inputs

- The subject name or organisation name.
- Source material or source references.
- Any user instruction about source scope.
- Draft claims if already extracted.

## Workflow

1. Confirm the subject and identity risk.
2. Create or update a source register.
3. Classify each source by type, visibility, reliability, recency, and subject match.
4. Extract or review atomic claims.
5. Assign evidence strength and confidence.
6. Check privacy and sensitivity.
7. Set inclusion status.
8. Return a concise review summary and any required changes.

## Source Classification

Use these fields:

- `source_type`: official, public_web, user_provided, internal, registry, news, social, database, other.
- `source_visibility`: public, internal, confidential, unknown.
- `reliability_tier`: primary, strong_secondary, secondary, weak, unknown.
- `recency_status`: current, recent, dated, stale, unknown.
- `subject_match`: direct, probable, ambiguous, no_match.

For detailed rules, read `references/source-quality-rubric.md`.

## Claim Review

Set these fields for each claim:

- `evidence_strength`: strong, adequate, limited, weak, none.
- `confidence`: high, medium, low, excluded.
- `identity_link`: direct, probable, ambiguous, not_established.
- `sensitivity.level`: none, low, medium, high, restricted.
- `privacy.final_output_allowed`: true or false.
- `inclusion.status`: include, include_softened, internal_only, exclude, needs_review.
- `review_status`: approved, rejected, challenged, or needs_review.

## Hard Stops

Mark the claim `exclude`, `internal_only`, or `needs_review` when:

- the subject match is ambiguous,
- the source does not support the claim,
- the claim infers a UC connection,
- the claim infers wealth, giving capacity, donor likelihood, or intent,
- the claim contains donor-level or raw private data,
- the claim is sensitive but not necessary,
- the claim relies on stale or weak evidence for a current status.

## Output Format

Return:

```yaml
source_quality_review:
  subject_identity_status: "confirmed / probable / ambiguous / unconfirmed"
  source_summary:
    total_sources: 0
    high_quality_sources: 0
    sources_needing_review: []
  claim_summary:
    include: 0
    include_softened: 0
    internal_only: 0
    exclude: 0
    needs_review: 0
  required_changes:
    - "Describe required change."
  reviewer_note: "Short plain-language assessment."
```

Then provide the updated source and claim records when requested.

## Final Reminder

Never approve a claim for final output just because it sounds plausible. Approve it only when identity, source support, confidence, privacy, sensitivity, and inclusion status all support use.

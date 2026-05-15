# Minimal Prototype Schema

## Purpose

This schema is the smallest practical version of the full internal claim and evidence model. It is designed for the first prototype workflow: turn supplied source material into reviewed claims, then draft a profile only from claims that pass review.

The full model lives in `docs/data-model.md`. This file defines what version one must actually capture.

## Prototype Data Package

Each profile run should produce one data package with:

- `profile_request`
- `subject`
- `sources`
- `claims`
- `reviews`
- `profile_output`

## Required Structure

```yaml
profile_request:
  request_id: "req_001"
  requested_at: "2026-05-15T09:00:00+12:00"
  profile_type: "individual"
  output_length: "standard"
  source_scope: "user_provided_only"
  final_output_rules:
    include_recommendations: false
    include_source_notes: false
    include_confidence_labels: false

subject:
  subject_id: "subj_001"
  subject_type: "individual"
  display_name: "Example Person"
  identity_status: "confirmed"
  identity_risk:
    level: "low"
    notes: "Identity directly tied to supplied source material."
  uc_connection_status: "not_confirmed"

sources:
  - source_id: "src_001"
    source_type: "user_provided"
    title: "User supplied notes"
    url_or_reference: "Pasted notes"
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
    text: "Example Person is chief executive of Example Organisation."
    source_ids: ["src_001"]
    evidence_strength: "adequate"
    confidence: "high"
    confidence_reason: "Directly stated in supplied notes."
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
    review_status: "approved"

reviews:
  - review_id: "rev_001"
    review_type: "evidence"
    reviewer: "Evidence / Source Agent"
    reviewed_object_type: "claim"
    reviewed_object_id: "clm_001"
    result: "approved"
    findings:
      - "Claim is directly supported by source material."
    required_changes: []

profile_output:
  output_id: "out_001"
  request_id: "req_001"
  subject_id: "subj_001"
  profile_type: "individual"
  output_length: "standard"
  sections: []
  omitted_sections: []
  final_checks:
    no_recommendations_unless_requested: true
    no_unsupported_uc_connection: true
    no_unsupported_capacity_claims: true
    no_donor_level_data: true
    no_low_confidence_claims: true
    no_empty_sections: true
    nz_english: true
```

## Controlled Values

### `profile_type`

- `individual`
- `organisation`

### `output_length`

- `short`
- `standard`
- `detailed`
- `comprehensive`

Use `detailed` for individuals and `comprehensive` for organisations when deeper evidence notes or due diligence are requested.

### `source_scope`

- `user_provided_only`
- `public_web_allowed`
- `internal_sources_allowed`

### `identity_status`

- `confirmed`
- `probable`
- `ambiguous`
- `unconfirmed`

### `uc_connection_status`

- `confirmed`
- `not_confirmed`
- `contradicted`
- `unknown`

### `source_type`

- `official`
- `public_web`
- `user_provided`
- `internal`
- `registry`
- `news`
- `social`
- `database`
- `other`

### `reliability_tier`

- `primary`
- `strong_secondary`
- `secondary`
- `weak`
- `unknown`

### `recency_status`

- `current`
- `recent`
- `dated`
- `stale`
- `unknown`

### `subject_match`

- `direct`
- `probable`
- `ambiguous`
- `no_match`

### `topic`

- `identity`
- `current_role`
- `career_background`
- `organisation_overview`
- `leadership`
- `uc_connection`
- `philanthropy`
- `community_activity`
- `capacity_indicator`
- `interest_alignment`
- `sensitivity`
- `source_limitation`
- `absence`
- `contradiction`

### `claim_type`

- `fact`
- `inference`
- `absence`
- `contradiction`
- `limitation`

### `evidence_strength`

- `strong`
- `adequate`
- `limited`
- `weak`
- `none`

### `confidence`

- `high`
- `medium`
- `low`
- `excluded`

### `inclusion.status`

- `include`
- `include_softened`
- `internal_only`
- `exclude`
- `needs_review`

### `review_status`

- `unreviewed`
- `reviewed`
- `challenged`
- `approved`
- `rejected`

## Required Validation Rules

The first prototype should reject or flag a data package when:

- a claim has no `source_ids`,
- a claim has `confidence: high` but `evidence_strength` is `weak` or `none`,
- a claim has `inclusion.status: include` but `review_status` is not `approved`,
- a claim has `inclusion.status: include` and `privacy.final_output_allowed` is `false`,
- a claim has `topic: uc_connection` and is based on inference only,
- a capacity claim includes unsupported wealth, donor likelihood, or giving intent language,
- a final profile section references a claim marked `exclude`, `internal_only`, or `needs_review`,
- final checks are missing or false.

## Recommended File Format

Use YAML for early fixtures and human review. It is readable enough for development and strict enough to convert later into JSON Schema, Pydantic, TypeScript types, or another implementation format.

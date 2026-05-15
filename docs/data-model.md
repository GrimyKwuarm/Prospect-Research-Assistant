# Data Model

## Status

This is the proposed internal claim and evidence model for the first prototype. It is intentionally more detailed than the final profile output. The model exists to make unsafe, unsupported, stale, ambiguous, or private claims easier to detect before drafting.

No model can guarantee that mistakes will never happen. This model is designed to reduce risk by requiring every claim to carry source support, confidence, sensitivity, identity checks, inclusion decisions, and review history.

## Design Principles

- Evidence first, prose second.
- Every substantive profile statement should trace back to one or more claims.
- A claim is not eligible for final output just because it is interesting.
- Low-confidence claims are internal working material unless specifically reviewed and softened.
- Sensitive claims need a stronger evidence threshold than ordinary biographical claims.
- UC connections must be confirmed, not inferred.
- Wealth, giving capacity, philanthropy, and intent must not be overstated.
- Final profiles should be clean; internal confidence scaffolding belongs behind the scenes unless requested.

## Core Objects

The model has six core objects:

- `profile_request`: what the user asked for.
- `subject`: the person or organisation being profiled.
- `source`: a discrete piece of supporting material.
- `claim`: a specific assertion extracted from one or more sources.
- `review`: an agent or human assessment of a claim or output.
- `profile_output`: the final or draft profile generated from approved claims.

## Profile Request

```yaml
profile_request:
  request_id: "req_2026_05_15_001"
  requested_at: "2026-05-15T09:00:00+12:00"
  requested_by: "user"
  profile_type: "individual / organisation"
  output_length: "short / standard / detailed / comprehensive"
  intended_audience: "internal UC Development"
  requested_sections:
    - "snapshot"
    - "current_roles"
    - "confirmed_uc_connection"
  excluded_sections:
    - "recommendations"
    - "engagement_strategy"
  special_instructions:
    - "Do not include recommendations unless explicitly requested."
  source_scope: "user-provided only / public web allowed / internal sources allowed"
  final_output_rules:
    include_recommendations: false
    include_source_notes: false
    include_confidence_labels: false
```

### Profile Request Rules

- `profile_type` determines whether the individual or organisation template is used.
- `source_scope` must be respected. If the user asks for user-provided material only, do not add public-web claims.
- `final_output_rules.include_recommendations` defaults to `false`.
- `final_output_rules.include_confidence_labels` defaults to `false`; confidence is primarily internal.
- Any request for major architecture, database, authentication, deployment, payment, or public API work must be treated as a separate decision.

## Subject

```yaml
subject:
  subject_id: "subj_001"
  subject_type: "individual / organisation"
  display_name: "Example Person"
  known_aliases:
    - "E. Person"
  identifiers:
    organisation_number: null
    public_profile_url: null
    internal_record_reference: null
  location_context:
    country: "New Zealand"
    region: "Canterbury"
    city: "Christchurch"
  identity_status: "confirmed / probable / ambiguous / unconfirmed"
  identity_risk:
    level: "low / medium / high"
    notes: "Common name; multiple public profiles found."
  uc_connection_status: "confirmed / not_confirmed / contradicted / unknown"
```

### Subject Rules

- `identity_status` must be `confirmed` before strong claims are included in a final profile.
- If `identity_status` is `ambiguous`, the final profile should either pause for clarification or use only claims that are clearly tied to the intended subject.
- `uc_connection_status` must not be set to `confirmed` from sector, geography, shared interests, likely alumni status, or plausible relevance.
- For organisations, do not imply institutional UC connection merely because a leader has a UC link unless the source explicitly connects the organisation to UC.

## Source

```yaml
source:
  source_id: "src_001"
  source_type: "official / public_web / user_provided / internal / registry / news / social / database / other"
  title: "Example source title"
  author_or_publisher: "Example publisher"
  url_or_reference: "https://example.org/profile"
  access_date: "2026-05-15"
  publication_date: "2025-11-03"
  supplied_by_user: false
  source_visibility: "public / internal / confidential / unknown"
  reliability_tier: "primary / strong_secondary / secondary / weak / unknown"
  recency_status: "current / recent / dated / stale / unknown"
  subject_match: "direct / probable / ambiguous / no_match"
  contains_private_data: false
  contains_sensitive_data: false
  notes: "Official staff bio; current role confirmed."
```

### Source Types

- `official`: official biography, organisational website, UC page, annual report, regulatory filing, public register, or direct institutional source.
- `public_web`: ordinary public webpages not controlled by the subject or institution.
- `user_provided`: notes, pasted material, documents, or instructions supplied by the user.
- `internal`: internal CRM, internal notes, internal emails, donor records, or non-public institutional records.
- `registry`: Companies Office, charities register, public filings, public procurement records, or equivalent.
- `news`: reputable news, trade media, press releases, or media interviews.
- `social`: LinkedIn or other public social profiles.
- `database`: subscribed or structured database sources.
- `other`: anything that does not fit the above and needs explanation.

### Reliability Tiers

- `primary`: official source, public registry, direct institutional record, annual report, court/regulatory filing, or user-supplied source of record.
- `strong_secondary`: reputable news, established sector publication, credible interview, or well-maintained organisational profile.
- `secondary`: ordinary public web profile, directory, event listing, or third-party summary.
- `weak`: unattributed pages, scraped directories, outdated aggregators, promotional fragments, or unsourced claims.
- `unknown`: source cannot be assessed.

### Recency Rules

- `current`: source directly describes present status or has been updated within the last 12 months.
- `recent`: source is 1-3 years old and still plausibly relevant.
- `dated`: source is 3-5 years old; use cautiously.
- `stale`: source is more than 5 years old or clearly superseded.
- `unknown`: no date is available.

Current roles, directorships, employment, leadership, and sensitivities require special care when sources are dated, stale, or unknown.

## Claim

```yaml
claim:
  claim_id: "clm_001"
  subject_id: "subj_001"
  topic: "uc_connection"
  claim_type: "fact / inference / absence / contradiction / limitation"
  text: "No confirmed UC connection identified in the material reviewed."
  normalized_text: "No confirmed UC connection identified."
  source_ids:
    - "src_001"
    - "src_002"
  source_summary: "Reviewed official biography and UC search results; no confirmed connection located."
  evidence_quotes:
    - source_id: "src_001"
      excerpt: "Short supporting excerpt, if appropriate and allowed."
  evidence_strength: "strong / adequate / limited / weak / none"
  confidence: "high / medium / low / excluded"
  confidence_reason: "Multiple relevant sources reviewed; no source confirmed a UC link."
  identity_link: "direct / probable / ambiguous / not_established"
  source_recency: "current / recent / dated / stale / mixed / unknown"
  sensitivity:
    level: "none / low / medium / high / restricted"
    categories: []
  privacy:
    contains_private_data: false
    donor_level_data: false
    final_output_allowed: true
  inclusion:
    status: "include / include_softened / internal_only / exclude / needs_review"
    profile_section: "confirmed_uc_connection"
    wording_guidance: "Use exact standard wording."
    exclusion_reason: null
  review_status: "unreviewed / reviewed / challenged / approved / rejected"
  reviewers:
    - "Evidence / Source Agent"
  created_at: "2026-05-15T09:10:00+12:00"
  updated_at: "2026-05-15T09:20:00+12:00"
```

## Claim Topics

Use controlled topics so agents can review claims consistently.

- `identity`: subject identity, aliases, disambiguation, and subject match.
- `current_role`: current employment, leadership, governance, trusteeship, or public role.
- `career_background`: prior roles, education, achievements, career history.
- `organisation_overview`: purpose, sector, structure, operating model, scale.
- `leadership`: leaders, directors, founders, owners, trustees, decision-makers.
- `uc_connection`: alumni, staff, faculty, research, event, governance, giving, partnership, recruitment, or known relationship links.
- `philanthropy`: confirmed giving, foundation/trust activity, nonprofit roles, public campaign involvement.
- `community_activity`: volunteering, sponsorship, civic activity, mentoring, community initiatives.
- `capacity_indicator`: public indicators of scale, seniority, ownership, revenue bands, assets, filings, investment, contracts, or resourcing.
- `interest_alignment`: supported public interests mapped cautiously to UC themes.
- `sensitivity`: legal, reputational, ethical, regulatory, environmental, governance, financial, or personal matters.
- `source_limitation`: source gaps, uncertainty, stale information, name ambiguity, or unavailable evidence.
- `absence`: explicitly checked but not confirmed, such as no confirmed UC connection.
- `contradiction`: source conflict that requires review.

## Claim Types

- `fact`: directly supported by one or more sources.
- `inference`: reasoned interpretation from evidence; not a direct source statement.
- `absence`: a checked item was not found or not confirmed.
- `contradiction`: sources conflict.
- `limitation`: evidence boundary, uncertainty, or caveat.

### Claim Type Rules

- `fact` may be included if evidence and review gates are satisfied.
- `inference` is internal by default and must be softened if included.
- `absence` may be included where useful, especially for UC connection.
- `contradiction` is not final-output ready until resolved or clearly framed.
- `limitation` is usually internal, except in detailed profiles or source notes.

## Evidence Strength

- `strong`: direct primary source, multiple mutually reinforcing sources, or user-provided source of record.
- `adequate`: credible source support, but not as strong as a primary source.
- `limited`: one plausible source, dated source, or indirect support.
- `weak`: unreliable, vague, unattributed, stale, or ambiguous support.
- `none`: no source support.

## Confidence Levels

### High Confidence

Use `high` only when:

- the identity match is direct or otherwise clearly confirmed,
- evidence strength is strong or adequate,
- sources are current, recent, or still authoritative,
- no unresolved contradiction exists,
- the claim is not an unsupported inference,
- privacy and sensitivity rules allow use.

### Medium Confidence

Use `medium` when:

- evidence is plausible but not definitive,
- source recency is dated or mixed,
- identity match is probable rather than direct,
- only one credible source supports the claim,
- wording must be cautious,
- the claim should be checked before prominent inclusion.

Medium-confidence claims are not automatically final-output ready. They require review and usually softened wording.

### Low Confidence

Use `low` when:

- source support is weak,
- identity match is ambiguous,
- source date is stale or unknown for time-sensitive information,
- the claim relies on inference,
- source quality is uncertain,
- another source partly conflicts with it.

Low-confidence claims are internal-only by default.

### Excluded

Use `excluded` when:

- no evidence supports the claim,
- the claim is contradicted by stronger evidence,
- the claim exposes private or donor-level data not suitable for final output,
- the claim is sensitive but not necessary,
- the identity match is not established,
- the claim would overstate UC connection, wealth, philanthropy, capacity, or intent.

## Sensitivity Model

```yaml
sensitivity:
  level: "none / low / medium / high / restricted"
  categories:
    - "legal"
    - "reputational"
    - "financial"
    - "regulatory"
    - "ethical"
    - "environmental"
    - "governance"
    - "personal"
    - "health"
    - "family"
    - "political"
    - "religious"
    - "cultural"
    - "ambiguous_identity"
  necessity: "not_needed / useful_context / necessary_for_briefing"
  wording_constraint: "omit / neutral_summary / careful_context / internal_only"
```

### Sensitivity Rules

- Sensitive claims require stronger evidence than ordinary profile claims.
- Sensitive claims must be directly relevant and necessary to include.
- Personal, health, family, political, religious, cultural, and similar sensitive information should usually be omitted unless the user has explicitly provided it for a legitimate briefing purpose.
- Legal, reputational, regulatory, ethical, environmental, governance, or financial issues require reliable source support and neutral wording.
- If sensitivity is `high` or `restricted`, the default inclusion status is `internal_only` or `exclude`.

## Privacy Model

```yaml
privacy:
  contains_private_data: false
  donor_level_data: false
  internal_only_data: false
  personal_contact_data: false
  raw_identifier_data: false
  final_output_allowed: true
  handling_note: "No private or donor-level data present."
```

### Privacy Rules

Do not include in final profiles by default:

- donor IDs,
- CRM record IDs,
- raw internal notes,
- private contact details,
- personal addresses,
- private giving records,
- private relationship notes,
- unsupported sensitive personal details,
- material marked confidential or internal-only.

Internal sources may support a final statement, but the final wording must not expose raw private data unless the user explicitly asks and it is appropriate.

## Inclusion Status

```yaml
inclusion:
  status: "include / include_softened / internal_only / exclude / needs_review"
  profile_section: "snapshot"
  final_wording: "Optional approved wording."
  wording_guidance: "Use cautious language; do not imply giving capacity."
  exclusion_reason: null
```

### Inclusion Rules

- `include`: claim is approved for final output.
- `include_softened`: claim may appear only with cautious wording.
- `internal_only`: claim may guide internal reasoning but must not appear in final output.
- `exclude`: claim must not appear in final output or guide the profile.
- `needs_review`: claim cannot be used until reviewed.

### Automatic Exclusion Triggers

Set `inclusion.status` to `exclude` or `internal_only` if:

- identity is ambiguous,
- evidence strength is weak or none,
- confidence is low,
- source subject match is ambiguous,
- the claim contains donor-level data,
- the claim contains private data not suitable for output,
- the claim implies a UC connection without confirmation,
- the claim implies wealth or giving capacity without direct support,
- the claim is sensitive but not necessary,
- the claim conflicts with stronger evidence.

## UC Connection Rules

UC connection claims require explicit support. Acceptable support may include:

- official UC source,
- user-provided internal confirmation,
- public alumni biography,
- event record,
- research collaboration page,
- governance record,
- confirmed partnership record,
- confirmed recruitment, sponsorship, giving, or programme relationship.

Do not use as evidence by itself:

- living in Canterbury,
- working in a relevant sector,
- attending a local event without a stated UC link,
- likely alumni status,
- family connection unless explicit,
- similar research interests,
- plausible partnership relevance,
- a leader's UC history as proof of organisational connection.

If no connection is confirmed, use:

> No confirmed UC connection identified in the material reviewed.

## Capacity and Wealth Rules

Capacity claims must be based on supportable public or user-provided indicators. Acceptable indicators may include:

- senior role or ownership,
- public directorship,
- company scale,
- public filings,
- annual report figures,
- assets under management,
- public contracts,
- credible published lists,
- known foundation or trust role,
- significant public gift announcement.

Do not translate these into unsupported wealth estimates, donor likelihood, giving capacity, or intent. Use cautious wording such as:

- "Public indicators of capacity include..."
- "The available material suggests senior professional responsibility..."
- "No specific wealth estimate is included because the reviewed material does not provide a credible basis for one."

Avoid terms such as "high-net-worth", "major donor prospect", "strong affinity", or "likely donor" unless explicitly supported and requested.

## Philanthropy Rules

Philanthropy claims should distinguish between:

- confirmed personal giving,
- corporate giving,
- foundation/trust activity,
- sponsorship,
- volunteering,
- board or trustee service,
- community involvement,
- in-kind support,
- public advocacy.

Do not treat community involvement, seniority, or wealth indicators as proof of philanthropic intent.

## Absence Claims

Absence claims record what was checked but not found.

```yaml
claim:
  topic: "absence"
  claim_type: "absence"
  text: "No confirmed UC connection identified in the material reviewed."
  source_ids:
    - "src_001"
    - "src_002"
  evidence_strength: "adequate"
  confidence: "high"
  inclusion:
    status: "include"
    profile_section: "confirmed_uc_connection"
```

Absence claims should be used carefully. They mean "not confirmed in reviewed material", not "does not exist".

## Contradictions

```yaml
contradiction:
  contradiction_id: "con_001"
  subject_id: "subj_001"
  claim_ids:
    - "clm_004"
    - "clm_009"
  issue: "Two sources list different current roles."
  severity: "low / medium / high"
  resolution_status: "unresolved / resolved / needs_user_input"
  resolution_note: "Use the more recent official biography; mention prior role only if relevant."
```

### Contradiction Rules

- Do not resolve contradictions by guessing.
- Prefer current official sources over older secondary sources for current roles.
- If the contradiction affects identity, UC connection, sensitivity, or capacity, pause or mark for review.
- Final output should avoid contradicted claims unless the uncertainty is explicitly and appropriately framed.

## Review Object

```yaml
review:
  review_id: "rev_001"
  review_type: "source_quality / evidence / due_diligence / privacy / final_polish"
  reviewer: "Evidence / Source Agent"
  reviewed_object_type: "claim"
  reviewed_object_id: "clm_001"
  result: "approved / approved_with_changes / rejected / needs_review"
  findings:
    - "Source is official and current."
  required_changes:
    - "Remove inferred affinity language."
  reviewed_at: "2026-05-15T09:30:00+12:00"
```

## Profile Output

```yaml
profile_output:
  output_id: "out_001"
  request_id: "req_2026_05_15_001"
  subject_id: "subj_001"
  profile_type: "individual"
  output_length: "standard"
  sections:
    - section_id: "snapshot"
      heading: "Snapshot"
      text: "Final polished prose."
      supporting_claim_ids:
        - "clm_001"
        - "clm_002"
  omitted_sections:
    - section_id: "interests_alignment"
      reason: "Not requested and not required for standard profile."
  final_checks:
    no_recommendations_unless_requested: true
    no_unsupported_uc_connection: true
    no_unsupported_capacity_claims: true
    no_donor_level_data: true
    no_empty_sections: true
    nz_english: true
```

## Final Output Gate

Before a profile is delivered, every final-output section must pass these checks:

- Each substantive statement maps to approved supporting claims.
- No claim marked `exclude`, `internal_only`, or `needs_review` appears in final prose.
- No low-confidence claim appears in final prose.
- Medium-confidence claims are either omitted or softened and approved.
- UC connection language is confirmed or uses the standard no-confirmed-connection wording.
- Capacity and wealth language is evidence-backed and cautious.
- Sensitive material is necessary, well-supported, and neutrally phrased.
- Donor-level, private, confidential, or raw internal data is excluded.
- No recommendations, next steps, action items, or engagement strategy appear unless requested.
- No empty headings or filler sections remain.
- The final profile uses NZ English and restrained advancement language.

## Minimal Prototype Schema

The first prototype does not need every field above, but it should not drop the safety-critical ones.

Required for prototype:

```yaml
claim:
  claim_id: "clm_001"
  subject_id: "subj_001"
  topic: "current_role"
  claim_type: "fact"
  text: "Example Person is chief executive of Example Organisation."
  source_ids:
    - "src_001"
  evidence_strength: "strong"
  confidence: "high"
  identity_link: "direct"
  source_recency: "current"
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
  review_status: "approved"
```

Required source fields:

```yaml
source:
  source_id: "src_001"
  source_type: "official"
  title: "Example Organisation leadership page"
  url_or_reference: "https://example.org/leadership"
  access_date: "2026-05-15"
  publication_date: "unknown"
  source_visibility: "public"
  reliability_tier: "primary"
  recency_status: "current"
  subject_match: "direct"
```

## Example Claim Set

```yaml
subject:
  subject_id: "subj_001"
  subject_type: "individual"
  display_name: "Dr Eleanor Marsh"
  identity_status: "confirmed"
  identity_risk:
    level: "low"
    notes: "Fictional test subject."
  uc_connection_status: "confirmed"

sources:
  - source_id: "src_001"
    source_type: "user_provided"
    title: "Fictional test notes"
    url_or_reference: "template example"
    access_date: "2026-05-15"
    publication_date: "2026-05-13"
    source_visibility: "internal"
    reliability_tier: "primary"
    recency_status: "current"
    subject_match: "direct"

claims:
  - claim_id: "clm_001"
    subject_id: "subj_001"
    topic: "current_role"
    claim_type: "fact"
    text: "Dr Eleanor Marsh is founder and chief executive of Koru Diagnostics."
    source_ids: ["src_001"]
    evidence_strength: "strong"
    confidence: "high"
    identity_link: "direct"
    source_recency: "current"
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
      wording_guidance: "State as fictional example only."
    review_status: "approved"

  - claim_id: "clm_002"
    subject_id: "subj_001"
    topic: "capacity_indicator"
    claim_type: "inference"
    text: "Company ownership and senior executive responsibility are public capacity indicators."
    source_ids: ["src_001"]
    evidence_strength: "adequate"
    confidence: "medium"
    identity_link: "direct"
    source_recency: "current"
    sensitivity:
      level: "low"
      categories: ["financial"]
    privacy:
      contains_private_data: false
      donor_level_data: false
      final_output_allowed: true
    inclusion:
      status: "include_softened"
      profile_section: "professional_and_wealth_indicators"
      wording_guidance: "Do not estimate wealth or imply donor capacity."
    review_status: "approved"
```

## Open Decisions

- Whether source references should appear in standard profiles, comprehensive profiles only, or internal notes only.
- Whether excluded claims should be retained for audit during prototype work.
- Whether internal source references need a redaction layer before storage.
- Whether the first implementation should use YAML, JSON, or typed Python/TypeScript objects.
- Whether confidence labels should ever appear in final user-facing profiles.

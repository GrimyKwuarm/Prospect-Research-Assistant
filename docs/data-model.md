# Data Model

## Status

The internal data model is not final. This document captures the starting point for discussion.

## Suggested Internal Claim Object

```yaml
claim:
  topic: "UC connection"
  text: "Completed a Bachelor of Commerce at UC in 2008."
  source_type: "user-provided notes / public web / internal CRM / official page"
  source_reference: "Short source label or URL where appropriate"
  source_date: "2026-05-13 or unknown"
  confidence: "high / medium / low"
  include_in_profile: true
  sensitivity: "none / personal / reputational / financial / ambiguous"
  verification_note: "Confirmed by alumni notes and public speaker bio."
```

## Candidate Fields

- `topic`: the type of claim, such as current role, UC connection, philanthropy, leadership, capacity, sensitivity, or source limitation.
- `text`: the claim in plain language.
- `source_type`: broad category of supporting source.
- `source_reference`: specific source label, URL, document name, or user-provided note reference.
- `source_date`: publication, access, or supplied date where known.
- `confidence`: high, medium, or low.
- `include_in_profile`: whether the claim survives review for the final profile.
- `sensitivity`: whether the claim contains personal, reputational, financial, ambiguous, or other sensitive context.
- `verification_note`: short internal explanation of why the claim is accepted, softened, or excluded.

## Open Questions

- Should source references appear in final profiles, internal notes only, or both depending on profile type?
- Should confidence be visible to the user in comprehensive profiles?
- Should the workflow preserve excluded claims for audit purposes?
- How should internal-only source material be marked?
- How should conflicting source material be represented?

# Workflows

## Intended Profile Workflow

1. User supplies a prospect name, organisation name, and/or source material.
2. Research material is gathered or organised into notes.
3. Notes are converted into structured claims.
4. Evidence and source review checks confidence, recency, ambiguity, and support.
5. Profile writer drafts from approved claims only.
6. Due diligence and quality review checks sensitivities, private-data exposure, unsupported claims, and overstatement.
7. Final polish produces a concise profile in NZ English.

## Claim Review Gates

Before drafting, each claim should pass through the model in `docs/data-model.md`.

Minimum gates:

- identity match is direct or explicitly handled,
- source support is recorded,
- evidence strength is assessed,
- confidence is assigned,
- sensitivity and privacy status are checked,
- inclusion status is set,
- UC connection and capacity claims receive extra scrutiny.

The profile writer should only draft from claims marked `include` or `include_softened`.

## Individual Profile Workflow

Use the individual template when the subject is a person. Focus on:

- snapshot,
- current roles and public profile,
- confirmed UC connection,
- philanthropy and community involvement,
- professional and capacity indicators,
- sensitivities where necessary.

Do not treat likely sector relevance or geography as a UC connection.

## Organisation Profile Workflow

Use the organisation template when the subject is a company, trust, foundation, partner, or other institution. Focus on:

- snapshot,
- organisation overview,
- leadership and key people,
- confirmed UC connection,
- philanthropy, sponsorship, and community activity,
- sector position and partnership relevance,
- capacity and resourcing indicators for comprehensive profiles,
- sensitivities where necessary.

Do not treat organisation profiles as individual profiles with a different name.

## Final Profile Defaults

Omit by default:

- recommendations,
- suggested next steps,
- action items,
- engagement strategy,
- unsupported UC connections,
- unsupported wealth estimates,
- donor IDs,
- raw private data,
- unnecessary methodology,
- alignment/caveat sections unless comprehensive or requested.

## Final Output Gate

Before delivery, the final profile should be checked against these rules:

- no unsupported UC connection,
- no unsupported wealth or capacity claim,
- no low-confidence claim,
- no claim marked `exclude`, `internal_only`, or `needs_review`,
- no donor-level or raw private data,
- no recommendations unless requested,
- no empty headings or filler sections,
- NZ English and restrained advancement language.

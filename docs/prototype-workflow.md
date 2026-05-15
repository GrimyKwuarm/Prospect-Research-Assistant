# Prototype Workflow

## Purpose

The first prototype should prove that the project can produce safe profiles from reviewed evidence without building a full application too early.

The prototype should work with manually supplied source material first. Public-web research, automation, and richer tooling can come later.

## Inputs

Required:

- subject name or organisation name,
- profile type: individual or organisation,
- desired length: short, standard, detailed, or comprehensive,
- source material supplied by the user,
- any explicit section requests or exclusions.

Optional:

- known UC connection,
- internal notes approved for use,
- public source URLs,
- specific audience or meeting context,
- request for source notes or confidence labels.

## Workflow Stages

### 1. Intake

Capture the user request as `profile_request`.

Check:

- whether the subject is an individual or organisation,
- whether source scope is user-provided only or allows public research,
- whether recommendations or next steps were explicitly requested,
- whether source notes or confidence labels were requested.

Default to no recommendations, no engagement strategy, no confidence labels, and no source notes in final output.

### 2. Subject Setup

Create a `subject` record.

For individuals, check:

- display name,
- aliases,
- current role if supplied,
- identity risk,
- UC connection status.

For organisations, check:

- legal or trading name,
- aliases,
- organisation type,
- sector,
- leadership or ownership ambiguity,
- confirmed institutional UC connection.

If identity is ambiguous, stop or proceed only with claims clearly tied to the intended subject.

### 3. Source Register

Create one `source` record per source.

Each source must receive:

- source type,
- title or reference,
- access date,
- publication date or `unknown`,
- visibility,
- reliability tier,
- recency status,
- subject match,
- private-data flag,
- sensitive-data flag.

Sources with ambiguous subject match cannot support final-output claims without further review.

### 4. Claim Extraction

Extract short, atomic claims from the sources.

Good claims:

- make one assertion,
- use neutral wording,
- identify the topic,
- cite one or more source IDs,
- avoid combining fact and inference.

Poor claims:

- bundle multiple unsupported statements,
- imply motive or affinity,
- convert seniority into wealth,
- imply a UC connection from plausibility,
- include raw private data.

### 5. Evidence Review

For each claim, assess:

- evidence strength,
- confidence,
- identity link,
- source recency,
- sensitivity,
- privacy,
- inclusion status,
- wording guidance,
- review status.

The reviewer should mark claims as:

- `include` when approved for final prose,
- `include_softened` when allowed only with cautious wording,
- `internal_only` when useful for reasoning but not final output,
- `exclude` when unsafe or unsupported,
- `needs_review` when unresolved.

### 6. Drafting

Draft only from claims marked `include` or `include_softened`.

Use:

- `templates/individual-prospect-profile.md` for people,
- `templates/organisation-prospect-profile.md` for organisations.

Omit unsupported sections. Do not leave empty headings.

### 7. Due Diligence Review

Run a final review before polishing.

Check:

- no unsupported UC connection,
- no unsupported capacity or wealth claim,
- no low-confidence claim,
- no private or donor-level data,
- no unnecessary sensitive material,
- no recommendations unless requested,
- no overclaiming,
- no empty or filler sections.

### 8. Final Polish

Produce the final profile in NZ English.

Use restrained advancement language. Keep methodology, confidence scaffolding, and source analysis out of the final profile unless requested.

## Prototype Outputs

Each run should produce:

- structured YAML claim package,
- draft profile,
- final profile,
- short review summary listing excluded or softened claim categories.

The final profile should not expose the internal claim package unless the user asks for the working notes.

## Runner

Use the dependency-free prototype runner to validate fixture packages:

```powershell
python scripts/prototype_runner.py fixtures
```

For machine-readable output:

```powershell
python scripts/prototype_runner.py fixtures --json
```

The runner checks the safety-critical rules in `docs/minimal-prototype-schema.md` and reports claim counts by inclusion status.

To include structured draft profiles in the console output:

```powershell
python scripts/prototype_runner.py fixtures --draft
```

To write local outputs:

```powershell
python scripts/prototype_runner.py fixtures --output-dir outputs
```

Each fixture output directory contains:

- `review-report.json`
- `draft-profile.md`

Generated `outputs/` are local working files and are ignored by Git.

## Definition of Done

A prototype run is done only when:

- all sources are registered,
- every claim has a source,
- every claim has confidence and inclusion status,
- final prose maps to approved claims,
- final checks are true,
- unsupported sections are omitted,
- `STATUS.md` is updated after meaningful workflow changes.

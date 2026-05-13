# AGENTS.md

## Project Purpose

Prospect Research Profiles is a Codex-assisted project for producing safe, professional advancement research profiles for the University of Canterbury. The system will use reusable Skills, structured evidence handling, and specialist agent roles to create individual and organisation profiles that are concise, conservative, and suitable for internal development use.

The project must not invent or imply UC connections, philanthropic intent, wealth, capacity, or sensitivities where the evidence does not support them.

## Current Stack

- Source materials: DOCX templates and plain-text handoff notes.
- Working documentation: Markdown.
- Future implementation: to be decided after the documentation and template foundation is complete.
- Intended execution model: Codex workflows using Skills and multiple specialised agents.

## Core Commands

No application commands exist yet.

Useful project checks for now:

- Review docs and templates manually.
- Open DOCX templates in Word for visual verification.
- Keep Markdown templates aligned with the DOCX references.

Future commands should be documented here when implementation begins.

## Conventions

- Use NZ English.
- Keep advancement writing discreet, neutral, concise, and specific.
- Prefer factual phrasing:
  - "Public sources describe..."
  - "The material provided indicates..."
  - "Internal notes record..."
  - "No confirmed UC connection identified in the material reviewed."
- Separate facts from inference.
- Omit unsupported sections rather than filling them with speculation.
- Do not include recommendations, suggested next steps, action items, engagement strategy, or recommended approaches in final profiles unless explicitly requested.
- Alignment and caveats are not default final-profile sections except for comprehensive profiles or explicit user requests.

## Safety Rules

- Never assume a UC connection from geography, sector, interests, likely alumni status, relationship possibility, or plausible relevance.
- Never present unsupported wealth estimates, philanthropic capacity, giving history, or donor intent.
- Never expose donor IDs, raw private data, internal-only notes, or unnecessary sensitive details in final user-facing outputs.
- Include legal, reputational, ethical, regulatory, environmental, financial, or governance sensitivities only when they are well-supported, directly relevant, and necessary.
- Treat name ambiguity as a material risk. If identity cannot be confirmed, say so internally and avoid unsupported claims.
- Prefer omission or cautious wording over overclaiming.

## Suggested Agent Roles

Use these roles for complex profile workflows, not for small documentation edits.

- Research Agent: gathers and structures source material into evidence-backed notes.
- Evidence / Source Agent: checks source quality, recency, confidence, and name ambiguity.
- Profile Writer Agent: drafts a clean profile from approved claims.
- Due Diligence / Quality Agent: reviews claims, sensitivities, privacy, and overstatement risk.
- Final Polish Agent: applies NZ English, concise formatting, and final-profile rules.
- Documentation Maintainer: keeps project docs, templates, decisions, and status current.

## Review Guidelines

Before accepting a profile or workflow change, check:

- Are all UC connections explicitly supported?
- Are facts separated from inference?
- Are low- or medium-confidence claims softened, removed, or marked for internal review?
- Are donor-level details and private data excluded from final outputs?
- Are empty or unsupported final-profile sections omitted?
- Are final profiles free of recommendations unless requested?
- Does the output use neutral advancement-appropriate language?
- Does the change preserve separate handling for individual and organisation profiles?

## Before Change Checklist

- Read the relevant templates and docs first.
- Check `STATUS.md` and `DECISIONS.md` for current direction.
- Identify whether the work affects safety, data handling, public output, or future architecture.
- Ask before major architecture, database, authentication, deployment, payment, or public API decisions.
- Prefer small reversible changes.

## After Change Checklist

- Update `STATUS.md` after meaningful work.
- Update `DECISIONS.md` when a durable project choice is made.
- Update `CHANGELOG.md` for user-visible or structural changes.
- Add or update docs when behaviour, workflow, setup, or safety expectations change.
- Summarise changed files, checks run, test results, risks, and next steps.

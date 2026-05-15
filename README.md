# Prospect Research Profiles

This project is a foundation for a Codex-assisted prospect research tool for University of Canterbury advancement work. It is intended to produce individual and organisation prospect profiles using reusable Skills, structured evidence review, and specialist agent roles.

The project is currently in documentation and workflow-design stage. No app or automated profile workflow has been implemented yet. The first deterministic prototype runner now validates fictional claim packages against the minimal safety schema.

## Goals

- Produce concise, professional prospect profiles.
- Support both individual and organisation profile formats.
- Use evidence-backed claims with explicit confidence handling behind the scenes.
- Prevent invented UC connections, unsupported capacity claims, and overstatement.
- Keep final profiles clean, neutral, and appropriate for advancement use.

## Current Repository Contents

- `templates/`: Markdown versions of the profile templates for agent and workflow use.
- `docs/`: project architecture, setup, testing, security, data model, prototype workflow, and schema notes.
- `skills/`: reusable Skill specs for project workflows.
- `fixtures/`: fictional test cases for safety and workflow validation.
- Root operating files: project instructions, roadmap, status, decisions, changelog, and contribution guidance.

## Local Reference Materials

The initial local workspace also contains:

- `prospect_research_tool_handoff_summary.txt`: handoff context from earlier planning work.
- `Prospect Research Profile Template and Example.docx`: individual profile reference template.
- `Organisation Prospect Profile Template and Example.docx`: organisation profile reference template.

The Markdown templates in `templates/` are the working source for future Skills and workflows. The DOCX files remain polished local reference documents unless we decide to store them in the repository as binary assets.

## Recommended Starting Point

1. Read `AGENTS.md`.
2. Review `docs/architecture.md` and `docs/data-model.md`.
3. Review `docs/minimal-prototype-schema.md` and `docs/prototype-workflow.md`.
4. Use the Markdown templates in `templates/` as the working source for future Skills.
5. Keep the DOCX files as polished reference documents.

## Prototype Runner

Validate all fictional fixtures:

```powershell
python scripts/prototype_runner.py fixtures
```

Run tests:

```powershell
python -m unittest discover -s tests
```

## Important Output Rules

Final profiles should not include recommendations, suggested next steps, action items, engagement strategy, unsupported UC connections, unsupported wealth estimates, donor IDs, raw private data, or unnecessary methodology unless the user explicitly asks for that type of output.

## Status

See `STATUS.md` for the current project state and next steps.

# DECISIONS.md

## Decisions

### 2026-05-13: Use Markdown Templates as Working Sources

The DOCX templates remain polished reference documents. Markdown versions in `templates/` are the working sources for future Skills and orchestration.

Reason: Markdown is easier for agents to read, diff, update, and embed in workflows.

### 2026-05-13: Separate Individual and Organisation Profile Logic

Individual and organisation profiles will use separate templates and workflow expectations.

Reason: Organisation profiles require different emphasis: structure, leadership, activity, capacity, partnership relevance, and confirmed institutional relationship.

### 2026-05-13: Keep Final Profiles Conservative by Default

Final profiles will omit recommendations, next steps, engagement strategy, unsupported UC connections, donor-level private data, and unsupported capacity claims unless explicitly requested.

Reason: The project is intended for safe advancement research outputs, where overstatement and private-data leakage are material risks.

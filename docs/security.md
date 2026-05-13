# Security and Privacy

## Purpose

This project handles advancement research workflows. It must treat private, sensitive, donor-level, and unsupported information with care.

## Data Handling Rules

- Do not expose donor IDs in final outputs.
- Do not expose raw private notes unless explicitly requested and appropriate.
- Do not include unnecessary personal details.
- Do not include unsupported legal, reputational, financial, or ethical claims.
- Do not infer sensitive attributes.
- Use public and user-provided source material carefully and with attribution awareness.

## Final Output Rules

Final profiles should include only material that is:

- relevant,
- supported,
- appropriately phrased,
- safe for the intended internal audience.

## Risk Areas

- Name ambiguity.
- Confusing an individual with another person of the same name.
- Inferring alumni or institutional links from geography or sector.
- Treating public business success as direct philanthropic capacity.
- Repeating sensitive material that is not necessary for the briefing.

## Future Security Work

Before any app, database, authentication, deployment, or public API is added, pause and decide:

- where source material is stored,
- whether private data is persisted,
- how outputs are logged,
- who can access generated profiles,
- how deletion and retention should work.

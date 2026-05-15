# Testing

## Current Testing

The prototype runner has automated tests using fictional fixtures.

Run:

```powershell
python -m unittest discover -s tests
```

The test suite covers:

- fixture parsing,
- schema validation,
- blocked ambiguous-identity claims,
- blocked unsupported capacity claims,
- softened sector-relevance claims,
- no-confirmed-UC wording,
- local output file generation.

Current manual checks:

- Confirm the DOCX templates open correctly in Word.
- Confirm Markdown templates preserve the intended sections and safety rules.
- Confirm docs are aligned with the handoff summary.

## Future Test Areas

The first automated tests should focus on safety and output rules:

- no invented UC connection,
- no recommendations unless requested,
- no unsupported wealth or capacity claim,
- no donor IDs or raw private data in final output,
- omission of unsupported sections,
- separation of individual and organisation profile templates,
- correct handling of low- and medium-confidence claims.

## Suggested Fixtures

Use fictional prospects and organisations only. Test cases should include:

- confirmed UC connection,
- no confirmed UC connection,
- ambiguous identity,
- outdated source material,
- unsupported wealth inference,
- public philanthropy evidence,
- reputational sensitivity requiring careful wording.

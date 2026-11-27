# Reproduce the reported counts

Use Python 3.10 or newer. The script uses only Python's standard library: no installation, API key, LLM, network access, HDD or original working directory is needed.

From the package root:

```sh
python3 Reproduce/rebuild_tables.py
```

It verifies release checksums, regenerates six CSV tables in a temporary directory, compares every row with the released reference tables, and prints a PASS result. Temporary output is then removed. To keep it:

```sh
python3 Reproduce/rebuild_tables.py --output _reproduced
```

The released `Data/Results` is not overwritten. A mismatch raises an error rather than being silently accepted. `--skip-checksums` exists for package construction; normal users should not use it.

## What is reproduced

- 296 symptom rows: 74 categories, two original selection rules, two wording rules.
- 24 combination rows: six fixed combinations under the same four settings.
- 26 treatment-name-group rows, including zero results.
- The eight record-type totals, five original-classification totals and 23 symptom rows used in the readable results.

SQLite independently groups coded observations using the retained author roles, account-link basis and unit attribution. It does not trust an exported final account total. Treatment counting starts from the preserved name-group membership decisions, not source prose.

`non_excluded` corresponds to the historical `wider` rule; `qualified_comparison` corresponds to `stricter`. These are readable aliases for existing rules, not new classifications. The reading documents use the non-excluded descriptive figures. Both original rules remain available for audit.

## Scope

A successful check means that this released input produces the released counts. It does not confirm author identity, diagnoses, the truth of a testimony, the appropriateness of each AI annotation, or identical results from a fresh LLM run. Source text is not redistributed here; source-level interpretation review requires the separate archive.

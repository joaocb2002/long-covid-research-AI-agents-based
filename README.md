# Long COVID research: AI-agent-led evidence processing

This project collected and organised online illness accounts with features overlapping one patient's clinical history. It provides **supporting material for a clinician-written case report**, not a diagnosis, a clinical study of verified patients, or the case report itself. The medical team intends to follow the [CARE case-report guidelines](https://www.care-statement.org/checklist).

**Most of the collection, extraction, reconciliation, and technical verification was performed by AI agents** under the direction of the patient, a Research Scholar at the Institute for Systems and Robotics (ISR) and a PhD candidate in Artificial Intelligence and Robotics at Instituto Superior Técnico, University of Lisbon. The patient selected the initial links and supplied clinical information. Doctors remain responsible for clinical interpretation, validation and writing.

## Start with these documents

1. [Study overview](Reading/Study_Overview.pdf): how to understand the terms and counts.
2. [Collection and analysis methods](Reading/Data_Collection_and_Analysis.pdf): a short explanation of the procedure.
3. [Descriptive results](Reading/Descriptive_Results.pdf): the main findings and their limitations.
4. [Clinical history and treatment course](Clinical_Case/Long%20Covid%20-%20Clinical%20History%20and%20Treatment%20Course%20-%20Jo%C3%A3o%20CB.pdf): the patient-provided reference for case-report writing.

For an ordinary browser view, open [START_HERE.html](START_HERE.html). GitHub displays this README directly.

## What was collected

The initial list contained **159 unique Reddit posts**, mainly from r/covidlonghaulers. Further searches added **65**, giving **224 collected posts**, with accessible comments. Some capture was partial. Retained material includes partial matches and useful contrasts, not 224 identical clinical presentations.

The numerical analysis uses 211 unique posts; 13 calibration posts were kept outside it. The structured dataset contains **14,961 coded statements or events**, not people. Twenty-two records were excluded from analysis, but are retained with their original labels. At least 248 identifiable posts were considered during discovery; some early irrelevant search hits were not individually recorded, so the complete screening denominator is unknown.

## Seven execution stages

| Stage | What was done |
| --- | --- |
| 1. Preserve | Check and freeze the collected sources, replies and access notes. |
| 2. Define | Write categories and rules for recording information. |
| 3. Organise | Separate posts and comments, attribute their authors locally and retain source links. |
| 4. Extract | Run separate AI extractions, reconcile differences and audit the outputs. |
| 5. Check | Examine the combined data for inconsistencies, duplicates and restrictions. |
| 6. Analyse | Count reported features and combinations, and compare them with the clinical description. |
| 7. Present | Produce readable documents, tables and supporting records. |

Medical review was historically called Stage 8. It is outside these seven processing stages and is not replaced by an AI agreement or a passing computation check.

## What this package can reproduce

Run `python3 Reproduce/rebuild_tables.py` with Python 3.10 or newer. No API key, Internet access or external Python package is required. It independently recounts the released annotations and checks them against the saved result tables. See [reproduction instructions](Reproduce/README.md).

Fresh LLM extraction may produce different annotations. Reproducing the calculations does not independently confirm the meaning or truth of the online reports. The compact dataset omits third-party narrative text; full source-level review requires the separate historical archive.

## Important limits

- Selection deliberately sought symptom overlap. These are not representative prevalence estimates.
- AI agents made interpretative decisions. Separate passes reduce some errors but can share the same biases. Clinical validation remains separate.
- Accounts were anonymised within posts. Documented cross-post links are used, but complete global account matching is not established. Account reports are not a verified number of distinct patients.
- The effort was substantial relative to the concise, descriptive findings. Repeated audit packages enlarged storage without adding independent testimonies. No benchmark establishes that this workflow outperforms a simpler one.

The included clinical PDF was supplied later for case writing. Earlier extraction used Clinical Picture v3.1; the final analytical comparison used v4.0. The later PDF was not retrospectively substituted as their original input. [Clinical-reference roles](Provenance/clinical_reference_roles.json) records this distinction.

## Where to find things

`Sources/` contains the initial and complete URL catalogues in CSV and JSON. `Data/` contains the coded projection, categories and results. `Methods/` explains the process and AI limitations. `Reproduce/` contains the small recount script. `Provenance/` records origins and integrity checks.

This is a compact release, **below 1 GB unpacked**. It does not contain the much larger historical processing archive. The clinical PDF identifies the project owner and contains health information, included at his explicit request. Source URLs are traceable links, not anonymous data. See [reuse and data boundaries](REUSE.md).

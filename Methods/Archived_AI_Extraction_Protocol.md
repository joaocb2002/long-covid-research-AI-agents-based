# Stage 4 AI-assisted clinical extraction protocol

**Protocol version:** 1.0.0  
**Effective date:** 2026-09-28  
**Output status:** `PROVISIONAL_AI_EXTRACTED_PENDING_CLINICIAN_VERIFICATION`  
**Governing schema:** frozen Step 2 codebook v1.0.0  
**Current patient anchor:** Clinical Picture v3.1

## 1. Purpose and boundary

This protocol converts the frozen testimony corpus into source-attributed,
machine-readable clinical propositions. It is an evidence-organization process,
not diagnosis, causal inference, prevalence estimation, treatment evaluation, or
clinical advice. Reddit accounts remain unverified testimony. Similarity to the
patient anchor is descriptive and cannot establish a shared disease or mechanism.

The extraction is AI-led so that clinician participation is not a processing
blocker. AI agreement does not become human or clinical verification. Every
released record remains provisional until the medical team decides whether it
needs and receives source-level verification.

## 2. Immutable inputs

The exact input paths and SHA-256 values are recorded in `INPUTS.json`.

- Step 1 raw/source evidence is never edited by this stage.
- Step 2 schema, concepts, controlled vocabularies, and coding manual control all
  meanings and allowed values.
- Step 3 sources, units, actors, relationships, and locators are consumed
  read-only.
- Clinical Picture v3.1 is the sole current patient comparison anchor. The older
  frozen summary remains in the audit chain but is not independent corroboration.

No prior narrative synthesis is a coding source. Every extracted proposition must
trace to the frozen source or the separately versioned current-anchor overlay.

## 3. Three text views

Every Step 3 unit has three distinct representations in
`data/text_view/units_text_v1.jsonl`:

1. `raw_span_text`: exact frozen locator span, including structural metadata;
2. `structural_display_text`: the exact text normalized by the Step 3 parser and
   used to reproduce its stored hash;
3. `clinical_payload_text`: the gated text presented for clinical extraction,
   with capture metadata and structural headings removed.

The raw and structural views are audit surfaces. Only a non-empty clinical
payload with `effective_eligible_for_substantive_clinical_coding=yes` may generate
clinical records. The 318 retained controls must generate none. One hundred of
those controls correct upstream placeholder rows reading `[No retrievable text]`;
the correction is an overlay and does not mutate Step 3.

## 4. Unit of extraction and attribution

The smallest valid record is one attributed proposition concerning one actor,
one concept or event, and one applicable time period. Split a record whenever any
of these changes:

- actor or subject;
- source or unit;
- concept/phenomenon;
- episode or time period;
- presence versus denial;
- subjective symptom versus measurement;
- intervention target, outcome direction, or adverse effect;
- diagnosis label versus supporting phenomenology;
- observation versus explanation or mechanism.

Never merge an original poster and commenter, several commenters, several
accounts, or several sources into a synthetic patient. Cross-source identity is
unknown unless separately documented. Comment counts are not person counts.

## 5. Required outputs

Stage 4 retains the frozen 14-table model:

- structural: `sources`, `units`, `actors`, `relationships`;
- atomic clinical: `observations`, `timeline_events`, `modifiers`,
  `investigations`, `treatments`, `function_safety`, `diagnosis_claims`,
  `hypotheses`;
- appraisal and decisions: `evidence_grades`, `adjudication`.

Step 3 structural rows are reused without alteration. Clinical Picture v3.1 is
represented in a separate C002 overlay. Clinical-table column order must exactly
match the frozen Step 2 templates.

Required companion files are:

- `batch_manifest.csv` for input, protocol, run, and row-count provenance;
- `unmapped_assertions.csv` for clinically relevant wording that cannot be
  represented faithfully in codebook v1;
- `clinician_verification_queue.csv` for claims requiring records or medical
  review before publication use;
- `qc_findings.csv` for automated and semantic quality findings;
- `decision_log.md` for protocol-wide decisions that do not modify frozen
  semantics.

## 6. Extraction sequence

Each source is processed independently and persisted before the next source.

1. Verify the source SHA-256 and load its eligible units, actors, and relations.
2. Read the full source-local context, including title, post, and comment tree.
3. Exclude controls, metadata, deleted/removed text, and unavailable content.
4. Identify attributed candidate propositions with their smallest sufficient
   supporting text and exact locator.
5. Classify each proposition into its proper table before selecting a concept.
6. Complete provenance and subject fields before semantic qualifiers.
7. Apply polarity/direction and temporal, severity, frequency, measurement,
   insight, and causal-language fields only when supported.
8. Add an evidence-grade record for every entity admitted to comparative or
   synthesis use.
9. Run source-level referential, vocabulary, provenance, and non-inference checks.
10. Persist a complete per-source state atomically. A partial aggregate does not
    establish that a source is complete.

## 7. Non-inference rules

The extractor must never:

- turn non-mention into absence;
- treat inaccessible, deleted, metadata-only, or placeholder content as evidence;
- infer diagnosis, etiology, anatomy, mechanism, or COVID causation from
  similarity or timing;
- infer measured tachycardia from a tachycardia sensation;
- infer normal physiology from air hunger or a nonspecific normal workup;
- infer symptom resolution from distraction, masking, sedation, blunting, or
  preserved function;
- infer psychosis from phrases such as “going crazy,” thought acceleration, or
  unusual bodily sensations;
- infer absence of psychosis, mania, dissociation, suicidality, trauma, OCD,
  akathisia, fatigue, or PEM from silence;
- infer a psychiatric or neurological cause from body-first ordering;
- turn a self-reported clinician statement into a verified primary record;
- use medication response or nonresponse as a diagnostic test;
- upgrade repeated selected narratives into independent corroboration;
- normalize uncertain dates, doses, tests, or products beyond the source;
- invent a composite severity, credibility, or similarity score.

Allowed normalization must be narrow, reversible, and documented. Raw wording is
retained. `present_inferred_limited` is reserved for a close but not explicit
mapping and normally cannot support a direct anchor match.

## 8. Psychiatric–neurological boundary safeguards

Phenomenology, function/safety, diagnosis labels, and mechanisms are separate
evidentiary layers.

- Code body-first activation, secondary distress, fear of losing control with
  insight, hallucination/delusion/disorganization content, reality testing, mood
  elevation, and sleep need separately.
- A psychiatric label without defining phenomena is a diagnosis claim, not a
  substitute for observations.
- “Physical anxiety,” “adrenaline,” or “wired” language does not determine cause.
- Calm cognition during bodily alarm supports only the reported ordering.
- Explicit denials remain patient-account denials unless a primary clinical
  examination is present.
- Affirmative psychosis, suicidality, self-harm, dangerous behavior, or serious
  medication effects receive high-priority independent review.
- The patient's stable rational/emotional identity and preserved self-recognition
  are retained without treating them as proof of anatomical localization or as a
  complete psychiatric exclusion.

## 9. Measurements, modifiers, treatments, and function

### Measurements

Symptoms and measurements are separate rows. A direct symptom–measurement
mismatch requires contemporaneous pairing. Broad “normal tests” remain scoped to
the named or reported domain; `nondiagnostic` is not `normal`.

### Modifiers

State, awareness, distress, function, and recall are distinct. Engagement that
redirects attention is `masks_awareness` unless the source explicitly reports a
change in the underlying symptom state. Quiet-state prominence does not by itself
mean worsening physiology.

### Treatments

Create one intervention × target-domain × outcome-period row. Separate desired
effects, adverse effects, sedation/blunting, and function. Record dose, duration,
cointerventions, dechallenge/rechallenge, and adequacy only when reported.
“Helped” is a self-reported temporal outcome, not proof of efficacy or mechanism.

### Function and safety

Preserved performance and severe internal burden can coexist and must be coded as
separate propositions. Work/study, self-care, exercise, social participation,
driving, and safety domains are not interchangeable.

## 10. Clinical Picture v3.1 overlay

The current anchor receives source ID `C002`; `C001` remains the historical
frozen summary. C002 is a polished secondary summary, not a verbatim interview,
chart, laboratory report, or clinician letter.

- Patient-attributed statements use secondary-summary provenance.
- Clinician-attributed statements remain unverified without the original note.
- Named tests use secondary-summary-reported result provenance.
- Author interpretations belong in `hypotheses`, not `observations`.
- Quotation marks in the summary do not automatically make a phrase an original
  verbatim patient quotation.
- C002 may `supersede` C001 values but does not independently corroborate them.

The anchor map in `reviews/clinical_anchor_alignment_review_2026-09-28.md`
controls later comparison and preserves unresolved domains as unknown.

## 11. Comparison layer

Comparison occurs only after actor-local extraction. Each patient-anchor feature
receives one status:

- `direct_similarity`;
- `partial_similarity`;
- `contradiction_or_opposite_direction`;
- `explicit_absence_or_denial`;
- `not_mentioned`;
- `unknown_due_capture_or_attribution`;
- `conflicting_within_person`;
- `not_applicable`.

Whole-person overlap is a non-numeric configuration tier (`high_direct`,
`moderate_incomplete`, `low_component_only`, `non_convergent`, or `unassessable`)
and must be accompanied by named direct domains, missing domains, explicit
contradictions, and source limitations. Treatment response, psychiatric-boundary
evidence, and mechanistic language remain separate tracks and do not increase the
phenotype tier.

## 12. Independent AI review and adjudication

For the pilot and all high-risk material:

1. Pass A extracts without seeing Pass B.
2. Pass B independently extracts from the same frozen context and protocol.
3. A separate reconciliation pass compares records field by field against the
   source text; it must not choose A merely because A is earlier.
4. Agreements are retained with their provenance. Disagreements are either
   resolved with a source-grounded rationale or marked `deferred`.
5. Unresolved claims are restricted from analysis where appropriate and entered
   in the verification queue.

Mandatory second review covers core discriminators, explicit denials,
symptom–measurement mismatch, treatment outcomes, diagnosis and mechanisms,
psychiatric-boundary material, safety content, and every proposed high-overlap
classification. Ordinary low-risk records may use stratified audit sampling after
the pilot demonstrates acceptable precision.

AI review is quality control, not clinician validation. The final human-facing
package must clearly distinguish `single_coded`, AI-agreed/adjudicated material,
and clinician-verified records.

## 13. Pilot and release gates

The pilot must include the C002 anchor plus a deliberately diverse Reddit sample:
direct core phenomenology, treatment narratives, measurement claims,
psychiatric-boundary language, sparse/partial capture, attachments or indexed
summaries, multi-actor threads, denials, and explicit contradictions.

Before scaling, the pilot must pass:

- exact source/unit/actor referential integrity;
- exact controlled-vocabulary validation;
- zero records sourced from controls;
- non-empty locators and sufficient evidence spans;
- no actor leakage across units;
- no unsupported direct mismatch, diagnosis, mechanism, or negative finding;
- all high-risk records independently reviewed;
- every disagreement preserved or adjudicated;
- source-level outputs resumable and aggregate counts reproducible.

Full-corpus release additionally requires 225/225 terminal source states, zero
unexplained schema errors, duplicate/dependency handling, a documented review
sample, a complete verification queue, input/output checksums, and a frozen Stage
4 checkpoint. Downstream analysis must not begin from an incomplete aggregate.

## 14. Human verification boundary

Clinicians ultimately decide how any result may support a case report. Primary
records are especially important for the patient's infection dates, medication
reconciliation, psychiatric assessments, investigations, procedures, safety
issues, and any diagnostic or mechanistic statement. The retained raw corpus and
all intermediate layers allow them to inspect, correct, exclude, or rerun the
processing without recollecting the web data.


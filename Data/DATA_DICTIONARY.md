# Data guide

All CSV files use UTF-8, one header row and one record per row. Counts are integers. Identifiers are text. A blank field is not a denial or a zero: it can be inapplicable to that type of record or unrecorded. No table is a verified patient register.

## Input tables

**annotated_records.csv** contains all 14,961 records from the final analytical master, projected without narrative excerpts or notes. No row was newly extracted, regraded or removed during packaging.

| Fields | Meaning |
| --- | --- |
| `source_id` | Internal thread identifier: S for a supplied source, E for an additional source. Look up the post in `Sources/all_posts.csv`. |
| `table_name`, `entity_type`, `entity_id` | Kind of coded statement and its original stable identifier. |
| `unit_id`, `actor_id` | Source-local message and author identifiers. They do not establish global patient identity. |
| `evidence_grade_id` | Original appraisal record identifier; the complete narrative rationale remains in the archive. |
| `capture_provenance`, `corpus`, `access_class` | How the source was captured, which collection it belongs to and coverage limitations. |
| `directness`, `measurement_support`, `clinical_relevance`, `safety_sensitivity` | Original coded appraisal fields, not independent medical verification. |
| `stage4_use_restriction` | Original intended-use class. See the five classes below. |
| `stage5_restriction_codes`, `eligibility_boundary` | Additional preserved limits on use. |
| `descriptive_pattern_eligibility` | Anything other than `no` passes the original non-excluded descriptive rule. |
| `cross_source_pattern_eligibility` | `yes_dependency_adjusted_qualified` passes the account analysis's original comparison rule. |
| `independent_source_weight`, `independent_unit_corroboration_weight` | Original technical dependency weights, not probabilities or numbers of independent patients. |
| `clinical_validation_status` | Saved validation status, not upgraded by this release. |
| `concept_id`, `polarity`, `first_person_status` | Symptom category, explicit/inferred presence or denial, and attribution to personal experience. |
| `temporal_pattern`, `frequency`, `body_thought_order`, `insight_status`, `objective_pairing_status`, `coding_status` | Original observation qualifiers. Persistent and episodic accounts remain distinguishable. |
| `domain_code`, `record_type`, `status`, `crisis_immediacy` | Function/safety classification fields. |
| `hypothesis_level`, `proponent_type` | Type and attribution of an explanation, not a verified mechanism. |
| `test_code`, `result_category` | Coded investigation and reported result category. Raw result text is omitted. |
| `factor_code`, `direction`, `target_concept_id` | Coded symptom modifier, its direction and target category. |
| `event_type`, `date_precision`, `infection_relation`, `event_certainty` | Timeline qualifiers. Source dates and narrative chronology are omitted here. |
| `intervention_class`, `outcome_direction`, `trial_adequacy`, `attribution_strength` | Reported treatment qualifiers, not efficacy or safety estimates. |

`field_values.json` lists the actual non-empty values in these classification columns. `category_definitions.csv` supplies all 74 concept definitions and the original case-feature mapping. The mapping belongs to Clinical Picture v4.0, not automatically to the later supplied clinical PDF.

**author_links.csv** retains source ID, local author ID, role and the platform/OP basis for linkage within a post. **text_units.csv** links a message to its local author and identifies post/comment type. **known_account_links.csv** contains only the already documented cross-post clusters; missing links do not prove different people.

**treatment_group_membership.csv** links a coded treatment record to a previously matched name group. Aliases are in `Methods/treatment_name_groups.json`. No new name matching or treatment interpretation was performed during packaging.

## Original intended-use classes

| Class | Intended meaning |
| --- | --- |
| `qualified_comparative_use` | Suitable for limited descriptive comparison, subject to other restrictions. |
| `descriptive_use` | Retain the reported experience without admitting it to that comparison rule. |
| `context_only` | Retain background, explanation or retrieval context. It is not necessarily personal symptom evidence. |
| `requires_adjudication` | A use/interpretation decision remains open; it is not approved comparative evidence. |
| `exclude_from_analysis` | Retain for provenance but exclude from analysis. |

These are qualitative AI-assigned classes, not a validated numerical scale. Original labels and additional eligibility fields are separate and must both be respected.

## Results

`symptom_counts.csv` includes original post counts, countable personal-author post counts, account reports within posts, account reports after known cross-post links, and observation counts. More than one observation can come from one account. Unknown or third-person reports may contribute to a post total but not a countable personal account.

`symptom_combinations.csv` requires all component categories for the same account in the same post. `same_message_account_reports` is a subset, not an additional sample. The reading document uses within-post combination counts and known-link-adjusted symptom counts, matching the historical presentation.

`reported_symptoms.csv` is the easy-to-read subset shown in the results PDF. `treatment_mentions.csv` counts posts with retained coded treatment-name matches. `record_inventory.csv` counts statements/events by kind. `original_classifications.csv` counts the five saved intended-use classes.

The source catalogues distinguish initial/additional origin, partial capture and whether a source contributes records to the numerical analysis. Their URLs are traceable, not anonymous. The unmodified original supplied-link file in `Provenance/` contains one repeated entry; the professional catalogues deduplicate it to 159 initial posts.

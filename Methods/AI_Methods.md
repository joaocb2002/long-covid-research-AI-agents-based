# AI agents, effort and limitations

## What the agents did

An AI agent is a software assistant given a task and instructions. It can read material, use tools and save results, rather than only answer a question. Here, separate agent tasks extracted information, compared outputs and checked files. Agents are not people, and different tasks can use the same AI model. This plain-language explanation follows the [official OpenAI glossary](https://learn.chatgpt.com/docs/glossary).

This project was mainly executed by AI agents, with a patient directing the objective and supplying the initial links and clinical information. Agents searched and collected material, organised records, extracted coded statements, reconciled disagreements, wrote checking scripts and prepared documents. Separate tasks were used for extraction, reconciliation, audits and corrections. Role separation is not independent human validation.

Stage 4 used separate Pass A and blind Pass B extraction, followed by reconciliation and audits. Corrections and rejected outputs were retained in the historical archive. High agent activity or repeated technical checks do not themselves demonstrate clinical accuracy.

## Models and instructions

The historical records indicate predominantly the **Sol model family with high reasoning effort** during Stage 4. Earlier records refer to GPT-5.6 Sol/High; later identifiers explicitly reference GPT-6.1 Sol. There is no reliable per-call inventory establishing the exact model for every task or subagent. Luna and Terra were discussed as possible optimisations, but the saved evidence does not establish that they were used throughout any completed stage.

[The dated extraction protocol](Archived_AI_Extraction_Protocol.md), the category definitions and the workflow summary describe the instructions and boundaries. A complete export of all prompts, model snapshots, reasoning settings, sampling parameters and API requests was not retained. This package does not invent missing settings or promise an exact stochastic rerun.

The release/counting code requires no LLM. It processes preserved annotations with deterministic rules.

## Effort: recorded observations, not GPU measurements

The historical effort review covered **25 August–11 November 2026**, not the later document revisions or this packaging task:

| Recorded metric | Value | Meaning |
| --- | ---: | --- |
| Calendar span | 77.47 days | Includes pauses, access restrictions and credit interruptions. |
| Main-agent accumulated task duration | 293.51 hours | Includes waiting, I/O and overlapping agent work; not inference/GPU-hours. |
| Distinct subagent task identities | 1,213 | Technical task identities, not people, simultaneous workers or separate models. |

There is no complete billing/token export or measured total GPU time. Earlier token estimates were highly uncertain and are not presented here as measured usage. The historical observation counts are not updated totals for the whole project.

## Effort versus findings

Stage 4 dominated the processing effort and storage through separate extractions, reconciliation, corrections and repeated audits. Preserved working copies account for much of the archive's size; they are not extra testimonies. A precise stage-by-stage share of total time and storage is unavailable.

The substantial processing effort produced a concise set of descriptive results from a small selected online corpus. The number of coded records is larger than the number of source messages or contributors because one message can yield several statements. Revisions, copied dependencies and repeated audits greatly increased storage without creating additional independent evidence.

The full pipeline archive is kept on an external HDD (hard disk drive), the large-capacity storage disk. NVMe refers here to the computer's fast internal solid-state storage used for current work. After verified archiving, bulky intermediate copies were removed from the internal drive; working essentials were retained. This repository leaves out most of the historical archive, but those omitted materials remain preserved on the HDD. No archive deletion is part of this documentation update.

For historical context, a saved storage snapshot was approximately 66 GB internally and 632 GB on the external disk; the full main analytical table was about 36 MB. These are earlier measurements, not current sizes or measurements of this compact repository.

Broad symptom reports are more numerous than closely matching same-account combinations. For example, the readable results contain four account reports with the three selected alarm-related features; these are not four clinically confirmed matches to the complete case. There is no comparison showing that the extra agent work improved validity, speed or cost-effectiveness over a simpler workflow.

## Limits of AI-led execution

Agents can misread context, attribute a statement to the wrong author, split or combine records inconsistently, or infer more than the text supports. The same model family can repeat the same error across nominally separate passes. Agreement, checksums and successful recounts do not establish clinical truth.

Source selection was guided by the patient's symptoms and included subjective relevance judgments. Some replies were unavailable. Author labels were primarily source-local. Independent clinical adjudication and statistical validation of extraction accuracy are not established by this release.

The compact package supports exact checking of the counting layer and inspection of coded categories. Without the separately preserved narrative archive, it does not support a new source-by-source audit of every extraction decision. Medical interpretation, diagnosis, causal claims and treatment conclusions require separate evidence and clinician responsibility.

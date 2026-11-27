# Provenance and integrity

- `file_manifest.json`: each delivered file's purpose, byte size and SHA-256; CSV record counts where applicable. It omits itself and the checksum file to avoid circular hashes.
- `checksums.sha256`: checks every delivered file except itself, including the manifest. The recount script verifies it before calculation.
- `archive_input_bindings.json`: the original relative archive paths and hashes used to build the compact projection. These paths explain origin; the reproduction script does not require those files.
- `source_bindings.json`: source identifiers, Reddit post IDs, saved-record hashes and the original archive locations. No narrative source text is included.
- `original_supplied_links.txt`: the unmodified original link list. One repeated entry is collapsed in the professional 159-post catalogue.
- `public_projection.json`: which original columns were retained, renamed or omitted. The original 14,961 rows and classifications are preserved; sensitive/free-text fields are not redistributed.
- `clinical_reference_roles.json`: identifies the written clinical descriptions used at different steps. They concern the same patient and core clinical case; documentation was expanded and clarified over time.
- `reading_document_updates.json`: records editorial changes, old and new PDF hashes, and checks that numerical results were preserved. Later clarifications are in `subsequent_updates`; `current_reading_documents` identifies the current files.
- `release_metadata.json`: scope, counts, package date and the unpacked-size limit.
- `VALIDATION.json`: the bounded packaging checks and independent recount result. A technical PASS is not medical validation or ethics approval.

The reading PDFs were edited for this package: clearer terminology, current document titles and references, and no visible dates or version labels. Their displayed numerical results are unchanged. The clinical-history PDF remains the unchanged patient-supplied file. Historical source material, rejected attempts, original appraisal rationales and complete processing logs remain in the separate archive. They are not silently deleted or represented as part of this compact release.

No new Reddit acquisition, AI extraction, regrading, global identity reconstruction or clinical reanalysis was performed to assemble or editorially update this package. Dates and version identifiers remain in the technical provenance where they are needed to identify historical inputs accurately.

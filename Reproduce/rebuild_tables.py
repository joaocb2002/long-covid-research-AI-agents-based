#!/usr/bin/env python3
"""Recount released coded data with SQLite; no LLM, network or archive required."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import sqlite3
import tempfile
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write(path, records, fields):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def verify_checksums():
    checksum_file = ROOT / "Provenance/checksums.sha256"
    if not checksum_file.exists():
        raise RuntimeError("Missing release checksums")
    checked = 0
    for line in checksum_file.read_text().splitlines():
        expected, relative = line.split("  ", 1)
        target = (ROOT / relative).resolve()
        if not target.is_relative_to(ROOT):
            raise RuntimeError("Unsafe checksum path")
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError("Checksum mismatch: " + relative)
        checked += 1
    return checked


def reproduce(output):
    output.mkdir(parents=True, exist_ok=True)
    if output.resolve().is_relative_to((ROOT / "Data").resolve()):
        raise RuntimeError("Use a separate output directory, not released Data")
    annotations = rows(ROOT / "Data/annotated_records.csv")
    actors = {(r["source_id"], r["actor_id"]): r for r in rows(ROOT / "Data/author_links.csv")}
    unit_author = {(r["source_id"], r["unit_id"]): r["actor_id"] for r in rows(ROOT / "Data/text_units.csv")}
    clusters = {(r["source_id"], r["actor_id"]): r["cluster_id"] for r in rows(ROOT / "Data/known_account_links.csv")}
    categories = rows(ROOT / "Data/category_definitions.csv")
    db = sqlite3.connect(":memory:")
    db.execute("create table obs(sid, aid, uid, code, polarity, qualified, included, countable, link)")
    for r in annotations:
        if r["table_name"] != "observations":
            continue
        key = (r["source_id"], r["actor_id"])
        actor = actors.get(key, {})
        countable = int(
            r["first_person_status"] == "first_person"
            and actor.get("actor_role") in ("original_poster", "commenter")
            and actor.get("account_link_basis") in ("platform_account_within_source", "op_role_within_source")
            and unit_author.get((r["source_id"], r["unit_id"])) == r["actor_id"]
        )
        link = "XL-" + clusters[key] if key in clusters else "|".join(key)
        db.execute("insert into obs values(?,?,?,?,?,?,?,?,?)", (
            r["source_id"], r["actor_id"], r["unit_id"], r["concept_id"], r["polarity"],
            int(r["cross_source_pattern_eligibility"] == "yes_dependency_adjusted_qualified"),
            int(r["descriptive_pattern_eligibility"] != "no"), countable, link))
    symptoms = []
    combinations = []
    combination_rules = json.loads((ROOT / "Methods/counting_rules.json").read_text())["combinations"]
    for selection, column in [("qualified_comparison", "qualified"), ("non_excluded", "included")]:
        for wording in ["explicit_and_limited_inference", "explicit_only"]:
            clause = f"{column}=1 and polarity in ('present_explicit','present_inferred_limited')"
            if wording == "explicit_only":
                clause += " and polarity='present_explicit'"
            for category in categories:
                code = category["concept_id"]
                posts, observations = db.execute(
                    f"select count(distinct sid),count(*) from obs where {clause} and code=?", [code]).fetchone()
                personal = db.execute(
                    f"select count(distinct sid),count(distinct sid||char(31)||aid),count(distinct link),count(*) "
                    f"from obs where {clause} and code=? and countable=1", [code]).fetchone()
                symptoms.append(dict(zip(SYMPTOM_FIELDS, [selection, wording, code, category["label"],
                    posts, *personal[:3], observations, personal[3]])))
            for combination in combination_rules:
                codes = combination["concepts"]
                placeholders = ",".join("?" for _ in codes)
                where = f"{clause} and countable=1 and code in ({placeholders})"
                matches = db.execute(f"select sid,aid,link from obs where {where} "
                    "group by sid,aid having count(distinct code)=?", codes + [len(codes)]).fetchall()
                same = db.execute(f"select sid,aid,uid from obs where {where} "
                    "group by sid,aid,uid having count(distinct code)=?", codes + [len(codes)]).fetchall()
                combinations.append(dict(zip(COMBINATION_FIELDS, [selection, wording,
                    combination["combination_id"], "+".join(codes), len(matches),
                    len({x[0] for x in matches}), len({x[2] for x in matches}),
                    len({(x[0], x[1]) for x in same})])))
    write(output / "symptom_counts.csv", symptoms, SYMPTOM_FIELDS)
    write(output / "symptom_combinations.csv", combinations, COMBINATION_FIELDS)
    inventory = Counter(r["table_name"] for r in annotations)
    write(output / "record_inventory.csv", [{"record_type": k, "records": v}
        for k, v in sorted(inventory.items())], ["record_type", "records"])
    grades = Counter(r["stage4_use_restriction"] for r in annotations)
    write(output / "original_classifications.csv", [{"classification": k, "records": v}
        for k, v in sorted(grades.items())], ["classification", "records"])
    by_id = {r["entity_id"]: r for r in annotations}
    groups = json.loads((ROOT / "Methods/treatment_name_groups.json").read_text())
    memberships = rows(ROOT / "Data/treatment_group_membership.csv")
    treatment_results = []
    for group in sorted(groups, key=lambda g: g["label"].casefold()):
        selected = [by_id[m["entity_id"]] for m in memberships
            if m["treatment_group"] == group["group"]
            and by_id[m["entity_id"]]["descriptive_pattern_eligibility"] != "no"]
        weights = {r["source_id"]: max(int(r["independent_source_weight"]), 0) for r in selected}
        treatment_results.append({"treatment_group": group["group"], "label": group["label"],
            "matching_records": len(selected), "posts": sum(weights.values())})
    write(output / "treatment_mentions.csv", treatment_results,
        ["treatment_group", "label", "matching_records", "posts"])
    look = {(r["selection_rule"], r["wording_rule"], r["concept_id"]): r for r in symptoms}
    reported = []
    for item in json.loads((ROOT / "Methods/counting_rules.json").read_text())["reported_symptoms"]:
        count = look[("non_excluded", "explicit_and_limited_inference", item["concept_id"])]
        explicit = look[("non_excluded", "explicit_only", item["concept_id"])]
        reported.append({"section": item["section"], "concept_id": item["concept_id"],
            "label": item["label"], "posts": count["posts_with_reports"],
            "account_reports": count["account_reports_after_known_links"],
            "explicit_only_account_reports": explicit["account_reports_after_known_links"]})
    write(output / "reported_symptoms.csv", reported,
        ["section", "concept_id", "label", "posts", "account_reports", "explicit_only_account_reports"])
    files = ["symptom_counts.csv", "symptom_combinations.csv", "record_inventory.csv",
        "original_classifications.csv", "treatment_mentions.csv", "reported_symptoms.csv"]
    verified_rows = {}
    for name in files:
        regenerated = rows(output / name)
        reference = rows(ROOT / "Data/Results" / name)
        if regenerated != reference:
            raise RuntimeError("Reproduction differs from released table: " + name)
        verified_rows[name] = len(reference)
    assert len(annotations) == 14961
    assert len(categories) == 74
    assert len(rows(ROOT / "Sources/all_posts.csv")) == 224
    assert len(rows(ROOT / "Sources/initial_posts.csv")) == 159
    assert grades["exclude_from_analysis"] == 22
    result = {"result": "PASS", "annotated_records": len(annotations), "categories": len(categories),
        "verified_rows": verified_rows, "network_required": False, "LLM_required": False,
        "scope": "Recounts released annotations; does not independently validate their interpretation."}
    (output / "REPRODUCTION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


SYMPTOM_FIELDS = ["selection_rule", "wording_rule", "concept_id", "label", "posts_with_reports",
    "posts_with_countable_accounts", "within_post_account_reports", "account_reports_after_known_links",
    "positive_observations", "countable_observations"]
COMBINATION_FIELDS = ["selection_rule", "wording_rule", "combination_id", "concepts",
    "within_post_account_reports", "posts", "account_reports_after_known_links", "same_message_account_reports"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Separate directory for regenerated tables")
    parser.add_argument("--skip-checksums", action="store_true", help="For packaging verification only")
    args = parser.parse_args()
    checked = 0 if args.skip_checksums else verify_checksums()
    if args.output:
        result = reproduce(args.output)
    else:
        with tempfile.TemporaryDirectory(prefix="long-covid-recount-") as folder:
            result = reproduce(Path(folder))
    result["files_checksum_verified"] = checked
    print(json.dumps(result, indent=2))

#!/usr/bin/env python3
# debug_union.py

import sys
from pathlib import Path
import re

def read_values(filename):
    """Reads file with 'i, value' lines -> {index: value}"""
    values = {}
    p = Path(filename)
    if not p.exists():
        print(f"[ERROR] File not found: {filename}")
        return values
    with p.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            if "," in line:
                left, right = line.split(",", 1)
            else:
                print(f"[WARN] line {lineno} in {filename} doesn't contain a comma: '{line}' (skipping)")
                continue
            try:
                idx = int(left.strip())
            except ValueError:
                print(f"[WARN] invalid index at {filename}:{lineno}: '{left.strip()}' (skipping)")
                continue
            values[idx] = right.strip()
    return values

def read_subtests(filename):
    """Reads subtest file like 'T1:2,4,6,...' -> { 'T1': [2,4,6,...] }"""
    subtests = {}
    p = Path(filename)
    if not p.exists():
        print(f"[ERROR] File not found: {filename}")
        return subtests
    with p.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            if ":" not in line:
                print(f"[WARN] line {lineno} in {filename} missing ':' -> '{line}' (skipping)")
                continue
            label, nums = line.split(":", 1)
            label = label.strip()
            if not label:
                print(f"[WARN] empty label at {filename}:{lineno}")
                continue
            nums_list = []
            if nums.strip():
                for token in nums.split(","):
                    tok = token.strip()
                    if not tok:
                        continue
                    try:
                        nums_list.append(int(tok))
                    except ValueError:
                        print(f"[WARN] invalid number '{tok}' at {filename}:{lineno} (ignoring)")
            subtests[label] = sorted(set(nums_list))
    return subtests

def pretty_set(s):
    return ", ".join(str(x) for x in sorted(s))

def main():
    # Filenames
    R_file = "R4.txt"
    P_file = "base.txt"
    subtest_file = "SubsetTests.txt"
    union_out = "partial_R4.txt"
    debug_out = "debug_report.txt"

    log_lines = []

    def log(*parts, sep=" ", end="\n"):
        text = sep.join(str(p) for p in parts) + end
        print(text, end="")
        log_lines.append(text)

    # Step 1: Read R and P
    log("=== Step 1: Read R and P files ===")
    R4 = read_values(R_file)
    P = read_values(P_file)
    log(f"Read {len(R4)} entries from {R_file}")
    if len(R4) > 0:
        sample_keys = sorted(list(R4.keys()))[:6]
        log("R sample:", ", ".join(f"{k}: {R4[k]}" for k in sample_keys))
    log(f"Read {len(P)} entries from {P_file}")
    if len(P) > 0:
        sample_keys = sorted(list(P.keys()))[:6]
        log("P sample:", ", ".join(f"{k}: {P[k]}" for k in sample_keys))
    log()

    # Step 2: Domains
    log("=== Step 2: Domains ===")
    dom_R4 = set(R4.keys())
    dom_P = set(range(13, 133))  # as you specified
    log(f"dom(R4) size: {len(dom_R4)} (min={min(dom_R4) if dom_R4 else 'N/A'} max={max(dom_R4) if dom_R4 else 'N/A'})")
    log(f"dom(P) (13..132) size: {len(dom_P)}")
    log()

    # Step 3: dom(R4 ∩ P)
    log("=== Step 3: dom(R4 ∩ P) ===")
    dom_R4capP = {i for i in dom_P if i in R4 and i in P and R4[i] == P[i]}
    log(f"dom(R4 ∩ P) size: {len(dom_R4capP)}")
    if len(dom_R4capP) <= 50:
        log("dom(R4 ∩ P):", pretty_set(dom_R4capP))
    else:
        ls = sorted(dom_R4capP)
        log("dom(R4 ∩ P) sample (first 20):", ", ".join(str(x) for x in ls[:20]))
        log("dom(R4 ∩ P) sample (last 20):", ", ".join(str(x) for x in ls[-20:]))
    log()

    # Step 4: complement of dom(R4 ∩ P)
    log("=== Step 4: complement of dom(R4 ∩ P) ===")
    complement_dom_R4capP = sorted(list(dom_R4 - dom_R4capP))
    log(f"complement size: {len(complement_dom_R4capP)}")
    log("complement:", ", ".join(str(x) for x in complement_dom_R4capP))
    log()

    # Step 5: detector set of P wrt R4
    log("=== Step 5: detector set of P wrt R4 ===")
    detector_set = sorted(list(dom_R4 & dom_P & set(complement_dom_R4capP)))
    log(f"detector set size: {len(detector_set)}")
    log("detector set:", ", ".join(str(x) for x in detector_set))
    log()

    # Step 6: complement of detector set
    log("=== Step 6: complement of detector set ===")
    complement_detector_set = sorted(list(dom_R4 - set(detector_set)))
    log(f"complement of detector set size: {len(complement_detector_set)}")
    log("complement of detector set:", ", ".join(str(x) for x in complement_detector_set))
    log()

    # Step 7: Read subtests (T1..T20)
    log("=== Step 7: Read subtest file ===")
    subtests = read_subtests(subtest_file)
    if not subtests:
        log(f"[ERROR] No subtests read from {subtest_file}. Exiting.")
        Path(debug_out).write_text("".join(log_lines), encoding="utf-8")
        return
    log(f"Read {len(subtests)} subtest labels from {subtest_file}: {', '.join(sorted(subtests.keys()))}")
    for label in sorted(subtests.keys()):
        s = subtests[label]
        log(f"{label}: size={len(s)}; sample(first 30) = {', '.join(str(x) for x in s[:30])}")
    log()

    # Step 8: Union each Ti with complement_detector_set
    log("=== Step 8: Compute unions Ti ∪ complement_detector_set ===")
    unions = {}
    for label in sorted(subtests.keys()):
        tset = set(subtests[label])
        union_set = sorted(tset | set(complement_detector_set))
        unions[label] = union_set
        log(f"{label} union size = {len(union_set)}")
        extras = sorted(set(union_set) - set(complement_detector_set))
        if extras:
            log(f"  extras added by {label} (count={len(extras)}): {', '.join(str(x) for x in extras)}")
        else:
            log(f"  no extras; union equals complement.")
    log()

    # Step 9: Are all unions identical?
    log("=== Step 9: Are all union results identical? ===")
    unique_unions = {}
    for label, u in unions.items():
        key = tuple(u)
        unique_unions.setdefault(key, []).append(label)
    log(f"Number of distinct union sets: {len(unique_unions)}")
    if len(unique_unions) == 1:
        log("✅ All unions are IDENTICAL.")
    else:
        log("❌ Unions are NOT identical. Distinct groups:")
        for idx, (key, labels) in enumerate(unique_unions.items(), 1):
            log(f"Group {idx}: labels = {', '.join(labels)} ; size = {len(key)}")
            s = list(key)
            log("  sample (first 40):", ", ".join(str(x) for x in s[:40]))
    log()

    # Step 10: Pairwise differences (optional)
    log("=== Step 10: Pairwise differences summary (counts) ===")
    labels = sorted(unions.keys())
    for i, a in enumerate(labels):
        for b in labels[i+1:]:
            sa = set(unions[a])
            sb = set(unions[b])
            sym = sa.symmetric_difference(sb)
            if sym:
                log(f"{a} vs {b}: sym-diff size = {len(sym)}")
    log()

    # Step 11: Write union_results.txt
    log("=== Step 11: Writing union results to file ===")

    def sort_key(label):
        m = re.match(r'[Tt](\d+)', label)
        return int(m.group(1)) if m else float('inf')

    with open(union_out, "w", encoding="utf-8") as out:
        for label in sorted(unions.keys(), key=sort_key):
            sorted_list = sorted(unions[label])
            out.write(f"{label}: " + ", ".join(str(x) for x in sorted_list) + "\n")

    log(f"Written: {union_out}")
    log()

    # Step 12: Write debug report file
    Path(debug_out).write_text("".join(log_lines), encoding="utf-8")
    log(f"Full debug report saved to {debug_out}")
    log("=== DONE ===")


if __name__ == "__main__":
    main()

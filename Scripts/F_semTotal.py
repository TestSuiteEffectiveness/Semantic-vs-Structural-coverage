#!/usr/bin/env python3
# total_union.py

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
        for line in f:
            line = line.strip()
            if not line or "," not in line:
                continue
            left, right = line.split(",", 1)
            try:
                idx = int(left.strip())
            except ValueError:
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
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            label, nums = line.split(":", 1)
            nums_list = []
            for tok in nums.split(","):
                tok = tok.strip()
                if not tok:
                    continue
                try:
                    nums_list.append(int(tok))
                except ValueError:
                    continue
            subtests[label.strip()] = sorted(set(nums_list))
    return subtests

def union_with_complement(subtests, complement_set):
    """Compute Ti ∪ complement_set for all subtests"""
    unions = {}
    for label, tset in subtests.items():
        union_set = sorted(set(tset) | set(complement_set))
        unions[label] = union_set
    return unions

def write_union_file(filename, unions):
    """Write unions to a file"""
    def sort_key(label):
        m = re.match(r'[Tt](\d+)', label)
        return int(m.group(1)) if m else float('inf')
    with open(filename, "w", encoding="utf-8") as out:
        for label in sorted(unions.keys(), key=sort_key):
            out.write(f"{label}: " + ", ".join(str(x) for x in sorted(unions[label])) + "\n")

def main():
    # Filenames
    R_file = "R4.txt"
    P_file = "base.txt"
    subtest_file = "SubsetTests.txt"
    total_file = "total_R4.txt"

    # Read inputs
    R4 = read_values(R_file)
    P = read_values(P_file)
    subtests = read_subtests(subtest_file)
    if not subtests:
        print("[ERROR] No subtests found. Exiting.")
        return

    # Domains
    dom_R4 = set(R4.keys())

    # dom(R4 ∩ P)
    dom_R4capP = {i for i in dom_R4 if i in P and R4[i] == P[i]}

    # Complement of dom(R4 ∩ P)
    complement_dom_R4capP = sorted(list(dom_R4 - dom_R4capP))

    # Detector set
    detector_set = sorted(list(dom_R4 & set(complement_dom_R4capP)))

    # Complement of detector set (for total correctness)
    complement_detector_set = sorted(list(dom_R4 - set(detector_set)))

    # Total correctness union
    total_unions = union_with_complement(subtests, complement_detector_set)
    write_union_file(total_file, total_unions)
    print(f"Total correctness unions written to {total_file}")

if __name__ == "__main__":
    main()

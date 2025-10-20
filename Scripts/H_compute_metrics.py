import csv
import os
import subprocess

# =====================================================
# Compute Precision, Recall, Jaccard, and F-score
# =====================================================

def loadTests(F):
    """Load semantic coverage graph from file."""
    data = {}
    with open(F) as file:
        for line in file:
            line = line.strip().split(":")
            if len(line) < 2:
                continue
            test_suite = line[0].strip()
            tests = [t.strip() for t in line[1].split(',') if t.strip()]
            data[test_suite] = tests
    return data


def compute_semantic_inclusions(data):
    """Compute semantic coverage arcs (FC)."""
    inclusions = []
    for t1 in data:
        for t2 in data:
            if t1 == t2:
                continue
            if all(x in data[t2] for x in data[t1]):
                inclusions.append((t1, t2))
    return inclusions


def compute_metric_agreements(inclusions, metric_dict):
    """Compute CM (metric inequalities) and FC∩CM (overlap with semantic arcs)."""
    CM = 0
    FC_and_CM = 0
    tests = list(metric_dict.keys())

    for i in range(len(tests)):
        for j in range(len(tests)):
            if i == j:
                continue
            t1, t2 = tests[i], tests[j]
            if metric_dict[t1] < metric_dict[t2]:  # strict inequality
                CM += 1
                if (t1, t2) in inclusions:
                    FC_and_CM += 1
    return CM, FC_and_CM


def compute_scores(FC_and_CM, FC, CM):
    """Compute metrics with professor's definitions."""
    precision = FC_and_CM / 190  # fixed denominator
    recall = FC_and_CM / FC if FC > 0 else 0
    jaccard = FC_and_CM / (FC + CM - FC_and_CM) if (FC + CM - FC_and_CM) > 0 else 0
    fscore = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, jaccard, fscore


# =====================================================
# Dataset paths
# =====================================================
datasets = {
    "Partial R4": "UnionTotal_R4.txt",
    "Total R4": "UnionPartial_R4.txt",
    "Partial R6": "Unionpartial_R6.txt",
    "Total R6": "UnionTotal_R6.txt",
    "Partial R7": "Union_partial_R7.txt",
    "Total R7": "Uniontotal_R7.txt"
}

# =====================================================
# Metric dictionaries
# =====================================================

Branch = {
     'T1': 0.69, 'T2': 0.66, 'T3': 0.63, 'T4': 0.72, 'T5': 0.75,
    'T6': 0.66, 'T7': 0.75, 'T8': 0.83, 'T9': 0.66, 'T10': 0.80, 'T11': 0.77,
    'T12': 0.80, 'T13': 0.69, 'T14': 0.77, 'T15': 0.83, 'T16': 0.75, 'T17': 0.80,
    'T18': 0.80, 'T19': 0.86, 'T20': 0.80
}

RMS = {
    'T1': 0.23, 'T2': 0.25, 'T3': 0.16, 'T4': 0.24, 'T5': 0.24, 'T6': 0.24,
    'T7': 0.24, 'T8': 0.25, 'T9': 0.25, 'T10': 0.25, 'T11': 0.25, 'T12': 0.24,
    'T13': 0.24, 'T14': 0.24, 'T15': 0.24, 'T16': 0.25, 'T17': 0.25, 'T18': 0.25,
    'T19': 0.24, 'T20': 0.25
}

LineCov = {
    'T1': 0.93, 'T2': 0.93, 'T3': 0.91, 'T4': 0.91, 'T5': 0.91, 'T6': 0.93,
    'T7': 0.93, 'T8': 0.93, 'T9': 0.91, 'T10': 0.91, 'T11': 0.93, 'T12': 0.93,
    'T13': 0.93, 'T14': 0.91, 'T15': 0.93, 'T16': 0.91, 'T17': 0.91, 'T18': 0.91,
    'T19': 0.93, 'T20': 0.91
}

InstrCov = {
    'T1': 0.96, 'T2': 0.97, 'T3': 0.96, 'T4': 0.96, 'T5': 0.96, 'T6': 0.97,
    'T7': 0.97, 'T8': 0.97, 'T9': 0.96, 'T10': 0.96, 'T11': 0.97, 'T12': 0.97,
    'T13': 0.97, 'T14': 0.96, 'T15': 0.97, 'T16': 0.96, 'T17': 0.96, 'T18': 0.96,
    'T19': 0.97, 'T20': 0.96
}


metrics = {
    "Branch Coverage": Branch,
    "RMS": RMS,
    "Line Coverage": LineCov,
    "Instruction Coverage": InstrCov
}


# =====================================================
# Run evaluation and save to CSV
# =====================================================

results = []
csv_file = os.path.join(os.getcwd(), "results.csv")

for ds_name, ds_file in datasets.items():
    data = loadTests(ds_file)
    FC_arcs = compute_semantic_inclusions(data)
    FC = len(FC_arcs)
    print(f"=== {ds_name} (FC arcs = {FC}) ===")

    for metric_name, metric_dict in metrics.items():
        CM, FC_and_CM = compute_metric_agreements(FC_arcs, metric_dict)
        precision, recall, jaccard, fscore = compute_scores(FC_and_CM, FC, CM)

        print(f"{metric_name}:")
        print(f"  CM = {CM}, FC∩CM = {FC_and_CM}")
        print(f"  Precision = {precision:.4f}, Recall = {recall:.4f}, "
              f"Jaccard = {jaccard:.4f}, F-score = {fscore:.4f}")

        # Save to results list
        results.append({
            "Dataset": ds_name,
            "Metric": metric_name,
            "FC": FC,
            "CM": CM,
            "FC∩CM": FC_and_CM,
            "Precision": precision,
            "Recall": recall,
            "Jaccard": jaccard,
            "F-score": fscore
        })

    print("============================================\n")

# Write results to CSV with UTF-8 encoding
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Dataset", "Metric", "FC", "CM", "FC∩CM", "Precision", "Recall", "Jaccard", "F-score"])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Results have been saved to '{csv_file}' successfully.")

# Automatically open the CSV file in Excel (Windows only)
try:
    subprocess.Popen(["start", csv_file], shell=True)
    print("📂 Opening results.csv in Excel...")
except Exception as e:
    print(f"⚠️ Could not open Excel automatically: {e}")

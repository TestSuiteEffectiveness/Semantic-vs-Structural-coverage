# Semantic vs Structural Coverage

This repository contains the data, code, and results for experiments comparing **semantic coverage** (based on specification relations) and **structural coverage** (statement, branch, line, and mutation metrics) using the function `tanhA` from Apache Commons Math (`FastMath` package).  
All scripts, data, and results are provided for research reproducibility.

---

## 📘 Overview

This work studies how structural coverage metrics (instruction, branch, line, and mutation) relate to **semantic coverage** measures derived from formal specifications (R4, R6, R7).  
The goal is to evaluate how well traditional structural metrics capture the semantic behavior of test suites.

---

## ⚙️ Experimental Setup

### Function Under Test
- Original function: `FastMath.tanh()` from **Apache Commons Math 3.6.1**  
- Modified version: `FastMathAA.tanhA()` — introduces controlled divergences (throws exceptions) for certain inputs.

### Test Classes
- **FastMathTest.java** contains two test functions:
  - `test01_tanhFailureCases`: 12 test cases causing exceptions (divergent behavior)
  - `test02_tanhAccuracyAA`: 120 valid test cases (total 132)
- **T0**: full set of 132 tests  
- **T1–T20**: subsets generated randomly (30–70% of T0)

### Test Suite Generation
- Script: `A_GenerateRandomTestSuites.py`  
- Output: `SubsetTest.txt` — defines which inputs belong to each test class.

---

## 🧪 Coverage Analysis

### 1. Structural Coverage
- **Tool:** [JaCoCo](https://www.jacoco.org/jacoco/) integrated via `pom.xml`  
- **Metrics:** Instruction coverage, Branch coverage, Line coverage  
- **Output files:**  
  - `code_coverage/Branch.txt`  
  - `code_coverage/InstructionStat.txt`  
  - `code_coverage/Line.txt`

### 2. Mutation Coverage
- **Tool:** [LittleDarwin](https://github.com/alipour/littledarwin)  
- 124 mutants generated for `tanhA()`  
- Scripts:
  - `B_FindOutputMutanta.py`
  - `C_GetKilledMutant.py`
  - `D_ComputeKilledMutantsByEveryTi.py`
- **Output:** `RMS.txt` = Killed/Total mutants per test class

---

## 🧭 Semantic Coverage

Semantic coverage is computed for specifications **R4**, **R6**, and **R7**.

Scripts:
- `E_SemPartial.py` — partial correctness coverage  
- `F_SemTotal.py` — total correctness coverage  
- `G_ExtractStrictInclusion.py` — computes strict inclusion among test suites  

Outputs:
- `GraphsInputTotal_Partial_StrictInclusion/`  
  - Files: `PR4.txt`, `TR4.txt`, `PR6.txt`, `TR6.txt`, `PR7.txt`, `TR7.txt`  
- `SemanticCoverageOutput/`  
  - Files: `Union_partial_R4.txt`, `Union_total_R4.txt`, etc.

---

## 📊 Metric Comparison

Script: `H_Compute_Metrics.py`

Computes precision, recall, jaccard, and F-score between **structural** and **semantic** coverage graphs.

Definitions:

- **FC:** number of arcs in the semantic coverage graph  
- **CM:** number of strict inequalities in the structural metric  
- **FC ∩ CM:** number of matching inequalities between both graphs  

Formulas:
Precision = |FC ∩ CM| / 190
Recall = |FC ∩ CM| / |FC|
Jaccard = |FC ∩ CM| / (|FC| + |CM| - |FC ∩ CM|)
F-score = 2 * (Precision * Recall) / (Precision + Recall)

## 📂 Repository Structure
```
semantic-vs-structural-coverage/
Data/
code_coverage/
Branch.txt
InstructionStat.txt
Line.txt
RMS.txt
GraphsInputTotal_Partial_StrictInclusion/
PR4.txt
TR4.txt
PR6.txt
TR6.txt
PR7.txt
TR7.txt
Mutants_LittleDarwin/
M125.txt
M126.txt
...
M248.txt
SemanticCoverageOutput/
Union_partial_R4.txt
Union_total_R4.txt
Union_partial_R6.txt
Union_total_R6.txt
Union_partial_R7.txt
Union_total_R7.txt
Scripts/
A_GenerateRandomTestSuites.py
B_FindOutputMutanta.py
C_GetKilledMutant.py
D_ComputeKilledMutantsByEveryTi.py
E_SemPartial.py
F_SemTotal.py
G_ExtractStrictInclusion.py
H_Compute_Metrics.py
Specification/
R4.txt
R6.txt
R7.txt
src/
main/java/org/apache/commons/math3/util/FastMathAA.java
test/java/org/apache/commons/math3/util/FastMathTest.java
Results.xlsx
README.md
LICENSE

```

## 📈 Results Summary

At the end of the experiments, the precision, recall, jaccard, and F-score were computed for each structural metric  
(statement, branch, line, RMS) with respect to semantic coverage for R4, R6, and R7.

These results are available in `Results.xlsx`.

---

## 📜 License

This project uses a dual-license structure:

- **Code and Scripts** — released under the [MIT License](./LICENSE)  
- **Data, Results, and Figures** — released under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

© 2025 Anonymous. All rights reserved where applicable.

---

## 💬 Citation

If you reference this repository in a publication, please cite it as:

Anonymous, "Semantic vs Structural Coverage," GitHub, 2025.
Available at: https://github.com/anonymous/semantic-vs-structural-coverage
---

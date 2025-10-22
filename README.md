## 📘 Semantic vs Structural Coverage

This repository contains the data, code, and results for experiments comparing **failure coverage (also known as semantic coverage)** and structural coverage (statement, branch, line, and mutation metrics) using the function `tanhA` from Apache Commons Math (FastMath package).
All scripts, data, and results are provided for research reproducibility.

---

### 📘 Overview

This work studies how structural coverage metrics (instruction, branch, line, and mutation) relate to **failure coverage** measures derived from formal specifications (R4, R6, and R7 — *renamed as R5 in the paper*).
The goal is to evaluate how well traditional structural metrics capture the failure behavior of test suites.

---

### ⚙️ System / Environment Setup

**Environment Used:**

* Operating System: Windows 10 (64-bit)
* Java Version: 1.8.0_144 (Oracle Corporation)
* Maven Version: 3.9.5
* JUnit Version: 4.x

**Repository-specific Maven configurations:**

* `pomJacoco.xml` – configuration for JaCoCo code coverage
* `pomPitest.xml` – configuration for PIT mutation testing

---

### 🧮 Function Under Test

* **Original function:** `FastMath.tanh()` from Apache Commons Math 3.6.1
* **Modified version:** `FastMathAA.tanhA()` — introduces controlled divergences (throws exceptions) for certain inputs.

---

### 🧪 Test Classes

`FastMathTest.java` contains two test functions:

* `test01_tanhFailureCases`: 12 test cases causing exceptions (divergent behavior)

* `test02_tanhAccuracyAA`: 120 valid test cases (total 132)

* **T0:** full set of 132 tests

* **T1–T20:** subsets generated randomly (30–70% of T0)

**Test Suite Generation:**

* Script: `A_GenerateRandomTestSuites.py`
* Output: `SubsetTestsT1_T20.txt` — defines which inputs belong to each test class.

---

### 🧪 Coverage Analysis

#### 1. Structural Coverage

**Tools:**

* [JaCoCo](https://www.jacoco.org/jacoco/) integrated via `pom.xml`
* [PiTest](https://pitest.org) for line coverage

**Metrics:** Instruction coverage, Branch coverage, Line coverage

**Output files:**

* `Data/code_coverage/Branch.txt`
* `Data/code_coverage/InstructionStat.txt`
* `Data/code_coverage/Line.txt` (from PiTest)
* `Data/code_coverage/RMS.txt`

---

#### 2. Mutation Coverage

**Tool:** [LittleDarwin](https://github.com/aliparsai/LittleDarwin)

* 124 mutants generated for `tanhA()`

**Scripts:**

* `B_FindOutputMutanta.py`
* `C_GetKilledMutant.py`
* `D_ComputeKilledMutantsByEveryTi.py`

**Output:**

* `Data/code_coverage/RMS.txt` = Killed / Total mutants per test class

---

#### 3. Failure Coverage

Failure coverage is computed for specifications **R4**, **R6**, and **R7 (renamed as R5 in the paper)**.

**Scripts:**

* `E_SemPartial.py` — partial correctness coverage
* `F_SemTotal.py` — total correctness coverage
* `G_ExtractStrictInclusion.py` — computes strict inclusion among test suites

**Outputs:**

* `Data/GraphsInputTotal_Partial_StrictInclusion/` (e.g., `PR4.txt`, `TR4.txt`, `PR6.txt`, `TR6.txt`, etc.)
* `Data/SemanticCoverageOutput/` (e.g., `Union_partial_R4.txt`, `Union_total_R4.txt`, etc.)

---

### 📊 Metric Comparison

**Script:** `H_Compute_Metrics.py`

Computes precision, recall, jaccard, and F-score between structural and failure coverage graphs.

**Definitions:**

* **FC:** number of arcs in the failure coverage graph
* **CM:** number of strict inequalities in the structural metric
* **FC ∩ CM:** number of matching inequalities between both graphs

**Formulas:**

```
Precision = |FC ∩ CM| / 190  
Recall = |FC ∩ CM| / |FC|  
Jaccard = |FC ∩ CM| / (|FC| + |CM| - |FC ∩ CM|)  
F-score = 2 * (Precision * Recall) / (Precision + Recall)
```

---

### 📂 Repository Structure

```
semantic-vs-structural-coverage/
│
├── Data/
│   ├── code_coverage/
│   │   ├── Branch.txt
│   │   ├── InstructionStat.txt
│   │   ├── Line.txt
│   │   └── RMS.txt
│   │
│   ├── GraphsInputTotal_Partial_StrictInclusion/
│   │   ├── PR4.txt
│   │   ├── TR4.txt
│   │   ├── PR6.txt
│   │   ├── TR6.txt
│   │   ├── PR7.txt
│   │   └── TR7.txt
│   │
│   ├── Mutants_LittleDarwin/
│   │   ├── M125.txt ... M248.txt
│   │
│   ├── SemanticCoverageOutput/
│   │   ├── Union_partial_R4.txt ... Union_total_R7.txt
│   │
│   ├── Test_Classes/
│   │   ├── FastMathTestT0.java ... FastMathTestT20.java
│   │
│   └── SubsetTestsT1_T20.txt
│
├── Scripts/
│   ├── A_GenerateRandomTestSuites.py ... H_Compute_Metrics.py
│
├── Specification/
│   ├── R0.txt
│   ├── R4.txt
│   ├── R6.txt
│   └── R7.txt
│
├── src/
│   ├── main/java/org/apache/commons/math3/util/FastMathAA.java
│   └── test/java/org/apache/commons/math3/util/FastMathTest.java
│
├── Results.xlsx
├── strictprecision.xlsx
├── README.md
├── LICENSE
├── pomJacoco.xml
└── pomPitest.xml
```

---

### 📈 Results Summary

At the end of the experiments, the precision, recall, jaccard, and F-score were computed for each structural metric
(statement, branch, line, RMS) with respect to **failure coverage** for R4, R6, and R5 (formerly R7).

These results are available in **Results.xlsx**.

Additionally, the file **strictprecision.xlsx** contains a summary of all the data used for the **first experiment**, including the data used to find the combined formula of adequacy metrics.
The first experiment follows the same process as the second experiment in terms of generating test suites.

---

### 📜 License

This project uses a dual-license structure:

* **Code and Scripts:** MIT License
* **Data, Results, and Figures:** Creative Commons Attribution 4.0 International (CC BY 4.0)

© 2025 Anonymous. All rights reserved where applicable.

---

### 📝 Brief Usage Instructions

Install Java 1.8 and Maven 3.9.5 on your system.

**Run code coverage:**

```bash
mvn test -Dtest="FastMathTest"
```

**Run mutation testing / PiTest:**

```bash
mvn test-compile org.pitest:pitest-maven:mutationCoverage
```

**Run mutation testing / LittleDarwin:**

```bash
py -m littledarwin -m -b -p src\main\java -t . -c "mvn,clean,test" --timeout=600
```

---

### 💬 Citation

If you reference this repository in a publication, please cite it as:

> Anonymous, *"Semantic vs Structural Coverage,"* GitHub, 2025.
> Available at: [https://github.com/TestSuiteEffectiveness/Semantic-vs-Structural-coverage](https://github.com/TestSuiteEffectiveness/Semantic-vs-Structural-coverage)

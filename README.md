# BrainHack Final Project: fNIRS Brain–Behavior Analysis in Children With and Without Dyslexia

## Overview
This project investigates the neural correlates of reading development in children using functional near-infrared spectroscopy (fNIRS), comparing typically developing (TD) children and children with developmental dyslexia (DD). Building on a previous MATLAB-based fNIRS preprocessing and localization framework, this project further implements a Python-based brain–behavior correlation and matrix visualization engine.

---

## Research Questions

### 1. Group-Level Neural Differences
Which specific brain regions show differential activation during a Morphological Awareness (MA) task between the TD and DD groups?

### 2. Brain–Behavior Relationships
Are individual neural activation patterns within these key functional regions associated with literacy-related behavioral performance across a comprehensive battery of 9 behavioral measures?

---

## Repository Structure

| File | Description |
|--------|--------|
| `BrainHack_Final_Project.ipynb` | Main Python analysis notebook |
| `Beta_TD.csv` | First-level GLM beta values for TD participants |
| `Beta_DD.csv` | First-level GLM beta values for DD participants |
| `TD_for_project.xlsx` | Behavioral data for TD participants |
| `DD_for_project.xlsx` | Behavioral data for DD participants |
| `All_Subjects_60_Correlation_Results.xlsx` | **[New]** Exported 3 channels × 9 behaviors Pearson correlation table (N=60) |
| `target_3ch_9behav_heatmap.png` | **[New]** Generated 3×9 brain-behavior correlation heatmap matrix |
| `.gitignore` | Excludes raw/private data files |

---

## Behavioral Measures (9 Dimensions)
To achieve a comprehensive profile of individual reading-related cognitive abilities, we expanded our analysis to encompass **9 distinct behavioral variables** from the raw participant files:
- `C_MC`: Morphological Construction (Measures morphological awareness)
- `Character_recog (PR)`: Chinese Character Recognition percentile rank (Measures reading ability); PR is used to avoid the confounding of age.
- `C_CTOPP`: Comprehensive Test of Phonological Processing
- `C_RAN`: Rapid Automatized Naming
- `C_CR`: Character Reading
- `C_WR`: Word Reading
- `C_PIC` & `C_PIC (52)`: Picture-Naming measures
- `C_RF`: Reading Fluency

---

## Analysis Pipeline

### [Phase 1: Previous MATLAB Pipeline & Channel Selection]
*The following initial steps were fully completed in MATLAB prior to the Python integration, establishing our region-driven framework:*

#### Step 1 — Preprocessing (MATLAB, NIRS Brain AnalyzIR Toolbox)
Raw fNIRS signals were acquired at 3.91 Hz using a NIRScout system. The raw time-series were preprocessed using a robust pipeline including baseline trimming, optical density conversion, and short-separation channel regression.

#### Step 2 — First-Level GLM (Subject-Level Activation)
A first-level general linear model (GLM) using AR-IRLS (Autoregressive-Iteratively Reweighted Least Squares) was fitted for each participant to generate localized HbO beta estimates for each participant × channel × condition.

#### Step 3 — Beta Value Extraction & Group LME Analysis
HbO beta values under the Morphological Awareness (`MA`) task condition were extracted. A Group-level Linear Mixed-Effects (LME) model was applied to screen for channels with significant group differences (`Group:cond`).
- **MATLAB Phase Result**: **Channel 6, 16, and 21** were successfully selected as our primary regions of interest. Anatomically, these channels correspond to the **dorsal Inferior Frontal Gyrus (dIFG)** and **Middle Temporal Gyrus (MTG)**, both firmly established in reading literature as critical brain regions for reading comprehension and development.

---

### [Phase 2: Current Python Brain–Behavior Pipeline]
*Building on the 3 target channels identified in the MATLAB phase, Python was utilized here to conduct an advanced behavioral mapping, automated missing-data cleaning, and matrix visualization:*

#### Step 4 — Targeted Brain–Behavior Correlation (Python)
Using the pooled dataset of **all 60 participants** to maximize statistical power, Python was implemented to run Pearson correlation coefficients matching the 3 functional channels against **all 9 linguistic and literacy behavioral measures** simultaneously.

#### Step 5 — Heatmap Matrix Visualization (Python)
Instead of plotting multiple independent, cluttered scatterplots, Python's `seaborn` and `matplotlib` were utilized to condense the 27 statistical pairs (`3 channels × 9 behaviors`) into a unified, publication-ready **Correlation Heatmap Matrix** (`target_3ch_9behav_heatmap.png`) to deliver maximum visual clarity for the project pitch.

##### Python Statistical Findings:
- **Raw Significance**: Before multi-comparison correction, **Channel 16 paired with `C_PIC (52)`** displayed a nominal positive correlation ($r = 0.402$, uncorrected $p = 0.0275$).
- **FDR Correction**: After globally applying the Benjamini-Hochberg FDR correction across the 27 tests in Python, **no correlation survived** ($p_{FDR} = 0.7412$). This demonstrates that the localized linear coupling does not withstand strict multi-comparison control. The full 27-row summary dataset was successfully exported directly to `All_Subjects_60_Correlation_Results.xlsx` for transparency.

---

## Methodological Discussion

The analytical strategy of this project centers on a deliberate, theory-motivated choice:

- **Discarding Unguided Whole-Brain Exploration**: This project discarded the initial whole brain analysis because previous studies have found a significant relationship between dIFG and MTG with reading development.
- **Literature-Driven Focus**: Instead, we prioritized strong prior empirical literature showing robust associations between neural activation within the dIFG and MTG during morphological processing and later reading outcomes. 
- **Scientific Interpretation**: Focusing on these 3 functional channels allowed a hypothesis-driven test of the relationship between core reading networks and our expanded behavioral battery. The absence of surviving stars in our final 3×9 heatmap may suggest that task-evoked fNIRS hemodynamics in developing children do not map onto complex behavioral phenotypes via simplistic 1-to-1 linear frameworks, pointing toward the need for more complex, non-linear modeling in future directions.

---

## How to Run Locally

### Requirements
- Python 3.x
- Jupyter Notebook
- pandas, numpy, scipy, matplotlib, seaborn, statsmodels

### Steps
1. Clone this repository.
2. Place `DD_for_project.xlsx`, `TD_for_project.xlsx`, `Beta_TD.csv`, and `Beta_DD.csv` in the directory.
3. Launch Jupyter Notebook and run `BrainHack_Final_Project.ipynb`.

## Acknowledgements

Special thanks to the BrainHack instructors and TAs for feedback and methodological discussions regarding:

- double dipping
- whole-brain analysis
- statistical interpretation

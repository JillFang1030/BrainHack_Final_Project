# BrainHack Final Project: fNIRS Brain-Behavior Analysis

## Description

This project investigates neural correlates of reading development in children, comparing **typically developing (TD)** children and children with **developmental dyslexia (DD)** using functional near-infrared spectroscopy (fNIRS).

The study aims to:
- Identify brain regions showing differential activation during a Morphological Awareness (MA) task between TD and DD groups
- Examine whether task-evoked neural responses can explain individual differences in reading ability (Chinese Character Recognition)

---

## Repository Structure

- `BrainHack_Final_Project.ipynb` — Main analysis script (brain-behavior correlation, plots)
- `Beta_TD.csv` — Extracted first-level GLM beta values for the TD group (per participant × channel × condition)
- `Beta_DD.csv` — Extracted first-level GLM beta values for the DD group (per participant × channel × condition)
- `TD_for_project.xlsx` — Behavioral data for the TD group
- `DD_for_project.xlsx` — Behavioral data for the DD group
- `.gitignore` — Configured to exclude all raw data files (.xlsx, .csv) to ensure data privacy

---

## Behavioral Measures

| Variable | Description |
|---|---|
| `C_MC` | Morphological Construction — measures morphological awareness |
| `Character_recog (PR)` | Chinese Character Recognition percentile rank — measures reading ability |

---

## fNIRS Task Conditions

| Condition | Description |
|---|---|
| MA | Morphological Awareness task |
| PA | Phonological Awareness task |
| Control | Baseline control task |

---

## Analysis Pipeline

### Step 1 — fNIRS Preprocessing (MATLAB, NIRS Brain AnalyzIR Toolbox)

Raw fNIRS signals were preprocessed in the following order:

1. Stimulus renaming — relabeled task channels to `MA`, `PA`, `Control`
2. Short-separation channel labeling — for noise regression
3. Resampling — downsampled to **2 Hz**
4. Optical Density conversion
5. Beer-Lambert Law — converted to HbO/HbR concentration changes
6. Baseline trimming — first and last **5 seconds** cropped (temporal cropping, not averaging)

### Step 2 — First-Level GLM (Subject-Level)

A GLM was fitted on the preprocessed time series for each participant individually.

- Method: AR-IRLS (handles motion artifacts and autocorrelation)
- HRF: Canonical hemodynamic response function, peak time = 6 seconds
- Short-separation regressors included
- Output: `SubjStats` — one beta estimate per participant × channel × condition

### Step 3 — Beta Value Extraction

Individual beta values were extracted from `SubjStats` and saved as `Beta_TD.csv` and `Beta_DD.csv` (one row per participant × channel × condition, HbO only).

### Step 4 — Group-Level LME (Channel Selection)

A linear mixed effects model was fitted on the extracted betas:

```
beta ~ -1 + Group:cond + (1|Subject)
```

Contrasts (TD MA vs. DD MA) were used to identify channels with significant group differences (FDR-corrected and uncorrected). This step determined which channels to use in the correlation analysis:

- **CH6** — significant at FDR < .05 (TD MA − DD MA contrast)
- **CH16, CH21** — significant at uncorrected p < .05

### Step 5 — Brain-Behavior Correlation (Python)

For each selected channel, Pearson correlations were computed between:
- MA beta values (from `Beta_TD.csv` / `Beta_DD.csv`)
- Behavioral scores (`C_MC`, `Character_recog (PR)`)

Analyses were run separately for the TD and DD groups.

---

## How to Run Locally

1. Clone this repository
2. Place the required data files (`DD_for_project.xlsx`, `TD_for_project.xlsx`, `Beta_TD.csv`, `Beta_DD.csv`) into the same directory
3. Run the notebook using Jupyter or VS Code

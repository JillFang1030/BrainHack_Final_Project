# BrainHack Final Project: fNIRS Brain–Behavior Analysis in Children With and Without Dyslexia

## Overview

This project investigates neural correlates of reading development in children using functional near-infrared spectroscopy (fNIRS), comparing typically developing (TD) children and children with developmental dyslexia (DD).

The project combines MATLAB-based fNIRS preprocessing and mixed-effects modeling with Python-based brain–behavior analysis and visualization.

In addition to examining group differences in neural activation, this project also explores whether task-evoked brain responses are associated with literacy-related behavioral performance.

## Research Questions

### 1. Group-Level Neural Differences

Which brain regions show differential activation during a Morphological Awareness (MA) task between TD and DD groups?

### 2. Brain–Behavior Relationships

Are neural activation patterns associated with individual differences in literacy performance?

Behavioral measures include:

- Chinese Character Recognition percentile rank (`Character_recog (PR)`)
- Morphological Construction (`C_MC`)

## Repository Structure

| File | Description |
|--------|--------|
| `BrainHack_Final_Project.ipynb` | Main Python analysis notebook |
| `Beta_TD.csv` | First-level GLM beta values for TD participants |
| `Beta_DD.csv` | First-level GLM beta values for DD participants |
| `TD_for_project.xlsx` | Behavioral data for TD participants |
| `DD_for_project.xlsx` | Behavioral data for DD participants |
| `.gitignore` | Excludes raw/private data files |

## Behavioral Measures

| Variable | Description |
|--------|--------|
| `C_MC` | Morphological Construction — measures morphological awareness |
| `Character_recog (PR)` | Chinese Character Recognition percentile rank — measures reading ability |

## fNIRS Task Conditions

| Condition | Description |
|--------|--------|
| `MA` | Morphological Awareness task |
| `PA` | Phonological Awareness task |
| `Control` | Baseline control condition |

## Analysis Pipeline

### Step 1 — fNIRS Preprocessing (MATLAB, NIRS Brain AnalyzIR Toolbox)

#### Data Acquisition

fNIRS data were acquired using a NIRScout 1624 system (15 sources, 16 detectors, 38 channels) with dual wavelengths of 760 nm and 850 nm. The original signals were sampled at 3.91 Hz.

#### Preprocessing Pipeline

Raw fNIRS signals were preprocessed using the following pipeline:

- Stimulus relabeling (`MA`, `PA`, `Control`)
- Short-separation channel labeling
- Resampling from 3.91 Hz to 2 Hz
- Optical Density conversion
- Beer–Lambert Law conversion to HbO/HbR concentration changes
- Baseline trimming (first and last 5 seconds cropped)

It is important to note that the subsequent analyses were not performed on the raw fNIRS time-series signals directly. Instead, the preprocessed signals were entered into a first-level GLM, and the resulting HbO beta estimates were used for all downstream statistical analyses.

### Step 2 — First-Level GLM (Subject-Level)

A first-level GLM was fitted separately for each participant.

#### Method

- AR-IRLS (autoregressive iteratively reweighted least squares)
- Canonical HRF (peak = 6 seconds)
- Short-separation regressors included

#### Output

`SubjStats`

One HbO beta estimate was generated for each **participant × channel × condition.**

### Step 3 — Beta Value Extraction

HbO beta values were extracted from `SubjStats` and exported as:

- `Beta_TD.csv`
- `Beta_DD.csv`

Each row corresponds to:

- one participant × one channel × one condition

### Step 4 — Group-Level LME Analysis (Initial Channel Selection)

A linear mixed-effects model (LME) was applied to identify channels showing group differences.

#### Model

```r
beta ~ -1 + Group:cond + (1|Subject)
```

#### Purpose

- Compare neural activation between TD and DD groups
- Control for repeated measurements and individual variability

#### Initial Findings

| Channel | Result |
|--------|--------|
| CH6 | Significant after FDR correction |
| CH16 | Significant at uncorrected p < .05 |
| CH21 | Significant at uncorrected p < .05 |

Initially, these channels were selected for downstream brain–behavior correlation analysis.

### Step 5 — Brain–Behavior Correlation Analysis (Python)

Python was used to perform exploratory brain–behavior analyses.

#### Skills Applied From BrainHack

- Interactive visualization (Plotly)
- Pearson correlation analysis
- Whole-brain exploratory visualization
- Statistical pipeline evaluation
- Multiple-comparison correction (FDR)

#### Initial Correlation Analysis

Pearson correlations were computed between:

- HbO beta estimates from the MA condition
- Behavioral scores (`C_MC`, `Character_recog (PR)`)

For selected channels **CH6. CH16, CH21**, no significant correlations were observed.

### Step 6 — Exploratory Whole-Brain Analysis

Following feedback from TA, lab members and the BrainHack pitch discussion, the analysis strategy was revised to reduce potential selection bias ("double dipping").

#### Motivation

Selecting channels based on prior group differences may bias downstream correlation analyses and overlook meaningful associations in other channels.

#### Updated Analysis

- All 32 channels were analyzed
- Pearson correlations computed for every channel
- An 8×4 scatterplot matrix was generated in Python
- FDR correction applied across all 32 correlation tests

#### Result

- No channel survived FDR correction
- Most scatterplots showed weak, cloud-like distributions
- No robust linear brain–behavior relationship was observed

## Key Methodological Insight

This project highlighted an important distinction between:

- Group-level effects (LME)
- Brain–behavior associations (Pearson correlation)

A channel showing significant TD vs. DD differences does not necessarily entail a significant relationship with independent behavioral measures, and vice versa.

## Future Directions

Potential future improvements include:

- Expanding the sample size to improve statistical power
- Testing additional behavioral measures
- Examining theoretically motivated brain–behavior relationships
- Integrating behavioral predictors within a unified modeling framework

## How to Run Locally

### Requirements

- Python 3.x
- Jupyter Notebook
- pandas
- numpy
- scipy
- matplotlib
- plotly
- statsmodels

### Steps

1. Clone this repository

2. Place the following files in the project directory:

- `DD_for_project.xlsx`
- `TD_for_project.xlsx`
- `Beta_TD.csv`
- `Beta_DD.csv`

3. Run:

```bash
jupyter notebook
```

4. Open:

```text
BrainHack_Final_Project.ipynb
```

## Acknowledgements

Special thanks to the BrainHack instructors and TAs for feedback and methodological discussions regarding:

- double dipping
- whole-brain analysis
- statistical interpretation

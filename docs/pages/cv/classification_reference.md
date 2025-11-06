---
layout: page
title: "Metrics – Classification Reference"
permalink: /metrics/classification
---

*Standardized semantic categories for PSI-MS quality control metrics.*

## Overview

Each QC metric in the [PSI-MS Controlled Vocabulary (CV)](https://github.com/HUPO-PSI/psi-ms-CV) is annotated using **seven independent classification dimensions**.
First, the **analytical dimension** defines *what kind of metric it is* and is encoded as **inheritance** using `is_a`.
The other six are **typed relationships** that describe *where the metric applies, what it depends on, how to interpret it,* and *how to serialize it in mzQC*.

**At a glance**

| Dimension                       | Encoded as     | Purpose                                                             |
| ------------------------------- | -------------- | ------------------------------------------------------------------- |
| **Analytical dimension**        | `is_a`         | Defines the metric subtype (what kind of QC metric it *is*)         |
| **Workflow stage**              | relationship   | Where in the experimental/computational pipeline the metric applies |
| **Information dependency type** | relationship   | What type of input data the metric needs                            |
| **Measurement scope**           | relationship   | At what aggregation level the metric summarizes data                |
| **Acquisition strategy**        | relationship   | Which acquisition/mode or platform it applies to                    |
| **Quality interpretation type** | relationship   | How to interpret higher/lower/targeted values                       |
| **Metric value type**           | relationship   | How the values are structurally represented (single, tuple, etc.)   |

**Rule of thumb:**
Every QC metric has exactly one `is_a` (analytical dimension) and one value from each of the other six relationship dimensions.

## Part 1 — Inheritance: Analytical dimension

**What it is:**
The analytical dimension defines the *type of QC metric*.
This is the only dimension expressed via **inheritance** (`is_a`) because it establishes the metric's place in the taxonomy.

**How to use it:**
Choose exactly one of the following as the metric's `is_a` parent:

#### Subclasses

- **Acquisition coverage metric:** how comprehensively data were collected (e.g., scan counts, sampling density).
- **Mass accuracy metric:** deviation between observed and theoretical _m_/_z_.
- **Intensity stability metric:** variation of signal intensity over time.
- **Chromatographic performance metric:** separation performance (e.g., eak width, symmetry, RT reproducibility).
- **Ionization quality metric:** properties of the precursor ion population (e.g., charge-state distribution, adduct prevalence).
- **Ion mobility metric:** IMS resolution, drift-time/CCS accuracy and reproducibility.
- **Spectral quality metric:** quality of individual spectra (e.g., peak density, S/N, completeness).
- **Fragmentation efficiency metric:** effectiveness of precursor ion fragmentation to produce interpretable spectra.
- **Isolation purity metric:** precursor isolation selectivity or co-isolation of interfering species.
- **Identification confidence metric:** reliability of identifications (e.g., FDR, ID rate).
- **Quantification precision metric:** reproducibility or variability of quantitative results.
- **Contamination metric:** unwanted signal from contaminants, carryover, or background.
- **Instrument operational performance metric:** general indicators of instrument health (e.g., vacuum, detector voltage, temperature).
- **Missingness/completeness metric:** data absence or completeness across features, runs, or studies.

#### CV example (inheritance only)

```obo
is_a: MS:4000XXX ! chromatographic performance metric
```

## Part 2 — Typed relationships

The remaining six dimensions are not types; they are **properties** of a metric.
They must be encoded using the specified **relationship** predicates (one value per dimension).

### 1. Workflow stage — `part_of_workflow_stage`

**Definition:**
The experimental or computational stage of the workflow to which a QC metric applies.

This tells *where* in the process the metric is relevant — from sample preparation through acquisition and analysis.

#### Subclasses

**Experimental workflow stage**

Metrics describing quality at the laboratory or instrument level.

* **Sample preparation stage:** metrics describing sample handling, labeling, digestion, or storage quality.
  *Example:* peptide recovery yield.
* **Chromatography stage:** metrics about LC separation performance.
  *Example:* retention-time reproducibility, peak width.
* **Ionization stage:** metrics about ion generation and charge distribution.
  *Example:* precursor charge-state fractions.
* **Ion mobility separation stage:** metrics describing the performance of gas-phase separation devices.
  *Example:* ion-mobility resolution, CCS reproducibility.
* **Mass spectrometry acquisition stage:** metrics referring to scanning, detection, or data acquisition processes.
  *Examples:* number of MS1 scans, duty-cycle stability.

  * **MS1 acquisition stage:** metrics that use or summarize MS1 data.
  * **MS2 acquisition stage:** metrics that use or summarize MS2 data.
  * **MSn acquisition stage:** metrics for higher-order fragmentation (MS³, etc.).
* **Instrument performance monitoring stage:** general metrics of instrument health and stability.
  *Example:* mass-accuracy drift, spray stability.
* **Instrument calibration stage:** metrics derived from calibration routines or control samples.

**Data analysis workflow stage**

Metrics evaluating computational processing and interpretation steps.

* **Data preprocessing stage:** metrics about baseline correction, noise removal, or peak picking.
* **Identification stage:** metrics assessing identification quality.
  *Example:* PSM-level FDR, peptide identification rate.
* **Quantification stage:** metrics describing quantitative accuracy or precision.
  *Example:* CV of peptide intensities, ratio reproducibility.
* **Integration stage:** metrics related to alignment, normalization, or data integration across runs.

**Environmental condition monitoring**

Metrics about environmental conditions that can indirectly affect results.
*Example:* laboratory temperature, humidity, power fluctuations.

#### CV example

```obo
relationship: part_of_workflow_stage MS:4000XXX ! chromatography stage
```

### 2. Information dependency type — `depends_on_data_type`

**Definition:**
Specifies which type of data input the metric requires to be computed.

#### Subclasses

* **Raw acquisition data:** metrics that can be calculated directly from the raw MS data, without identifications.
  *Example:* total ion current stability, scan count.
* **Identification results:** metrics that depend on identified peptides, compounds, or spectra.
  *Example:* PSM-level FDR, peptide coverage.
* **Quantification results:** metrics derived from quantitative data matrices.
  *Example:* CV of peptide intensities.
* **Hybrid:** metrics combining multiple data types (e.g., identification and quantification).
* **Reference data:** metrics requiring comparison to external standards or reference files.
  *Example:* RT deviation vs. iRT peptides, calibration QC.*

#### CV example

```obo
relationship: depends_on_data_type MS:4000XXX ! raw acquisition data
```

### 3. Measurement scope — `has_measurement_scope`

**Definition:**
Indicates the level of data aggregation the metric summarizes.

#### Subclasses

* **Spectrum level:** per-spectrum metrics (e.g., number of peaks, S/N ratio).
* **Pixel/voxel level:** per-pixel metrics in imaging or spatial omics.
* **Feature level:** per feature (e.g., peptide, compound, or chromatographic peak).
* **Run level:** aggregated per LC–MS run.
* **Batch level:** aggregated across multiple related runs.
* **Study level:** aggregated across an entire experiment or project.

#### CV example

```obo
relationship: has_measurement_scope MS:4000XXX ! run level
```

### 4. Acquisition strategy — `applies_to_acquisition_mode`

**Definition:**
Specifies which acquisition mode or instrument configuration the metric is relevant for.

#### Subclasses

**Acquisition mode**

* **Acquisition mode independent:** metrics valid for any acquisition method.
* **Data-dependent acquisition (DDA):** metrics specific to stochastic precursor selection workflows.
  *Example:* number of MS2 spectra per precursor.
* **Data-independent acquisition (DIA):** metrics for window-based fragmentation strategies.
  *Example:* precursor window purity.
* **Targeted acquisition:** metrics for SRM, PRM, or other targeted workflows.
  *Example:* transition reproducibility.
* **Ion-mobility-coupled metric:** metrics derived from acquisition methods that include gas-phase ion mobility separation.
  *Example:* TIMS mobility resolution (Δ1/K₀) per run.
* **Imaging acquisition:** metrics for spatially resolved mass spectrometry experiments such as MALDI, DESI, or SIMS.
  *Example:* pixel-to-pixel intensity variation across a tissue section.
* **Other specialized mode:** metrics for advanced or hybrid acquisition modes such as BoxCar, MSⁿ, or multiplexed scanning.
  *Example:* BoxCar intensity uniformity across boxes.

**Instrument platform specificity**

* **Orbitrap-specific:** metrics only applicable to Orbitrap instruments.
  *Example:* Orbitrap transient length stability.
* **TOF-specific:** metrics relevant to time-of-flight instruments.
  *Example:* TOF detector voltage stability.
* **Ion-trap-specific:** metrics specific to trap-based systems.
  *Example:* Ion trap fill time distribution.
* **Other platform-specific:** for quadrupoles, FT-ICR, or hybrid systems.

#### CV example

```obo
relationship: applies_to_acquisition_mode MS:4000XXX ! acquisition mode independent
```

### 5. Quality interpretation type — `has_quality_directionality`

**Definition:**
Describes how a metric's numeric value relates to overall quality.
This enables automatic reasoning about whether "higher," "lower," or "targeted" values represent better data.

#### Subclasses

* **Higher is better:** increasing values indicate improved quality.
  *Example:* identification rate, mass accuracy score.
* **Lower is better:** decreasing values indicate improved quality.
  *Example:* FDR, mass error.
* **Context dependent:** interpretation varies depending on method or range.
  *Example:* precursor charge-state fractions, peak density.
* **Target range:** optimal quality corresponds to values within a defined interval.
  *Example:* temperature, pressure, retention-time drift.
* **Categorical:** quality expressed as discrete categories (e.g., pass/fail, OK/warning/error).
* **Trend:** metrics intended for temporal monitoring rather than direct ranking (e.g., instrument drift over time).

#### CV example

```obo
relationship: has_quality_directionality MS:4000XXX ! lower is better
```

### 6. Metric value type — `has_value_type`

**Definition:**
Specifies the structural format of the metric's reported value(s).
This defines how the metric must be represented in mzQC.

#### Subclasses

| Type             | Structure         | Description                                                   | Example                       |
| ---------------- | ----------------- | ------------------------------------------------------------- | ----------------------------- |
| **Single value** | Scalar            | A single numeric or categorical value.                        | Number of MS1 spectra         |
| **Tuple**        | Ordered list      | Several ordered values of the same kind (e.g., quantiles).    | XIC-FWHM quantiles            |
| **Table**        | Named columns     | Parallel lists of equal length; each column has its own unit. | MS2 charge fractions          |
| **Matrix**       | Rectangular array | 2D array of homogeneous numeric values.                       | Ion-mobility intensity matrix |

See the [CV Term Usage Guide](/metrics/use) for details on how each type is encoded in mzQC.

---

## Worked examples

### XIC-FWHM quantiles (tuple)

* **Analytical dimension (`is_a`)**: *chromatographic performance metric*
* **Workflow**: *chromatography stage*
* **Data type**: *raw acquisition data*
* **Scope**: *run level*
* **Acquisition**: *mode independent*
* **Directionality**: *lower is better*
* **Value type**: *tuple*

```obo
is_a: MS:4000XXX ! chromatographic performance metric
relationship: part_of_workflow_stage MS:4000XXX ! chromatography stage
relationship: depends_on_data_type MS:4000XXX ! raw acquisition data
relationship: has_measurement_scope MS:4000XXX ! run level
relationship: applies_to_acquisition_mode MS:4000XXX ! acquisition mode independent
relationship: has_quality_directionality MS:4000XXX ! lower is better
relationship: has_value_type MS:4000XXX ! tuple
```

### MS2 known precursor charge fractions (table)

* **Analytical dimension (`is_a`)**: *ionization quality metric*
* **Workflow**: *ionization stage*
* **Data type**: *raw acquisition data*
* **Scope**: *run level*
* **Acquisition**: *mode independent*
* **Directionality**: *context dependent*
* **Value type**: *table*

```obo
is_a: MS:4000XXX ! ionization quality metric
relationship: part_of_workflow_stage MS:4000XXX ! ionization stage
relationship: depends_on_data_type MS:4000XXX ! raw acquisition data
relationship: has_measurement_scope MS:4000XXX ! run level
relationship: applies_to_acquisition_mode MS:4000XXX ! acquisition mode independent
relationship: has_quality_directionality MS:4000XXX ! context dependent
relationship: has_value_type MS:4000XXX ! table
```

## Summary

* Use **`is_a`** for the **analytical dimension** (the metric's type).
* Use **typed relationships** (one each) for the six **orthogonal facets**: workflow stage, data dependency, scope, acquisition strategy, quality interpretation, and value type.

These relationships together provide a complete, machine-readable semantic description of any QC metric.

For how to serialize each **metric value type** in mzQC (single, tuple, table, matrix), see the **[CV Term Usage Guide](/metrics/use)**.

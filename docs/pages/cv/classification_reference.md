---
layout: page
title: "Metrics – Classification Reference"
permalink: /metrics/classification
---

# QC Metric Classification Reference

*Standardized semantic categories for PSI-MS quality control metrics*

## Overview

Each QC metric in the PSI-MS Controlled Vocabulary (CV) is annotated using **seven independent classification dimensions**.
Together, these describe *what a metric measures*, *where it applies in the workflow*, and *how it should be interpreted*.

Every metric must define **exactly one relationship** from each dimension.
This ensures complete, machine-interpretable semantics across all QC terms used in mzQC and related standards.

| Dimension                       | Describes                                                              |
| ------------------------------- | ---------------------------------------------------------------------- |
| **Workflow stage**              | Where in the experimental or computational pipeline the metric applies |
| **Analytical dimension**        | What fundamental property the metric measures                          |
| **Information dependency type** | What type of data the metric depends on                                |
| **Measurement scope**           | At what aggregation level the metric summarizes data                   |
| **Acquisition strategy**        | Which acquisition or instrument configuration it applies to            |
| **Quality interpretation type** | How metric values relate to data quality                               |
| **Metric value type**           | How metric values are structurally represented (single, tuple, etc.)   |

## Workflow Stage

**Definition:**
The experimental or computational stage of the workflow to which a QC metric applies.

This tells *where* in the process the metric is relevant — from sample preparation through acquisition and analysis.

### Subclasses

#### Experimental workflow stage

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

#### Data analysis workflow stage

Metrics evaluating computational processing and interpretation steps.

* **Data preprocessing stage:** metrics about baseline correction, noise removal, or peak picking.
* **Identification stage:** metrics assessing identification quality.
  *Example:* PSM-level FDR, peptide identification rate.
* **Quantification stage:** metrics describing quantitative accuracy or precision.
  *Example:* CV of peptide intensities, ratio reproducibility.
* **Integration stage:** metrics related to alignment, normalization, or data integration across runs.

#### Environmental condition monitoring

Metrics about environmental conditions that can indirectly affect results.
*Example:* laboratory temperature, humidity, power fluctuations.

## Analytical Dimension

**Definition:**
The fundamental property or aspect of data quality that the metric quantifies.

Think of this as *what kind of problem the metric detects or describes*.

### Subclasses

* **Acquisition coverage metric:** evaluates how comprehensively data were collected (e.g., scan counts, sampling density).
* **Mass accuracy metric:** measures deviation between observed and theoretical m/z values.
* **Intensity stability metric:** assesses signal intensity variation over time.
* **Chromatographic performance metric:** evaluates separation performance such as peak width, symmetry, or retention reproducibility.
* **Ionization quality metric:** evaluates properties of the ion population generated during ionization, such as charge-state distribution or adduct prevalence.
* **Ion mobility metric:** describes resolution, drift-time accuracy, or reproducibility in ion-mobility separations.
* **Spectral quality metric:** quantifies quality of individual spectra (e.g., peak density, signal-to-noise, completeness).
* **Fragmentation efficiency metric:** measures how efficiently precursor ions fragment to produce interpretable spectra.
* **Isolation purity metric:** evaluates precursor isolation selectivity or co-isolation of interfering species.
* **Identification confidence metric:** quantifies reliability of peptide or compound identifications (e.g., FDR, number of identified analytes).
* **Quantification precision metric:** measures reproducibility or variability of quantitative results.
* **Contamination metric:** detects unwanted signal from contaminants, carryover, or background.
* **Instrument operational performance metric:** general indicators of instrument health (e.g., vacuum level, temperature, detector voltage).
* **Missingness/completeness metric:** measures data absence or completeness across features, runs, or studies.

## Information Dependency Type

**Definition:**
Specifies which type of data input the metric requires to be computed.

### Subclasses

* **Raw acquisition data:** metrics that can be calculated directly from the raw MS data, without identifications.
  *Example:* total ion current stability, scan count.
* **Identification results:** metrics that depend on identified peptides, compounds, or spectra.
  *Example:* PSM-level FDR, peptide coverage.
* **Quantification results:** metrics derived from quantitative data matrices.
  *Example:* CV of peptide intensities.
* **Hybrid:** metrics combining multiple data types (e.g., identification and quantification).
* **Reference data:** metrics requiring comparison to external standards or reference files.
  *Example:* RT deviation vs. iRT peptides, calibration QC.*

## Measurement Scope

**Definition:**
Indicates the level of data aggregation the metric summarizes.

### Subclasses

* **Spectrum level:** per-spectrum metrics (e.g., number of peaks, S/N ratio).
* **Pixel/voxel level:** per-pixel metrics in imaging or spatial omics.
* **Feature level:** per feature (e.g., peptide, compound, or chromatographic peak).
* **Run level:** aggregated per LC–MS run.
* **Batch level:** aggregated across multiple related runs.
* **Study level:** aggregated across an entire experiment or project.

## Acquisition Strategy

**Definition:**
Specifies which acquisition mode or instrument configuration the metric is relevant for.

### Subclasses

#### Acquisition mode

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

#### Instrument platform specificity

* **Orbitrap-specific:** metrics only applicable to Orbitrap instruments.
  *Example:* Orbitrap transient length stability.
* **TOF-specific:** metrics relevant to time-of-flight instruments.
  *Example:* TOF detector voltage stability.
* **Ion-trap-specific:** metrics specific to trap-based systems.
  *Example:* Ion trap fill time distribution.
* **Other platform-specific:** for quadrupoles, FT-ICR, or hybrid systems.

## Quality Interpretation Type

**Definition:**
Describes how a metric's numeric value relates to overall quality.
This enables automatic reasoning about whether "higher," "lower," or "targeted" values represent better data.

### Subclasses

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

## Metric Value Type

**Definition:**
Specifies the structural format of the metric's reported value(s).
This defines how the metric must be represented in mzQC.

### Subclasses

| Type             | Structure         | Description                                                   | Example                       |
| ---------------- | ----------------- | ------------------------------------------------------------- | ----------------------------- |
| **Single value** | Scalar            | A single numeric or categorical value.                        | Number of MS1 spectra         |
| **Tuple**        | Ordered list      | Several ordered values of the same kind (e.g., quantiles).    | XIC-FWHM quantiles            |
| **Table**        | Named columns     | Parallel lists of equal length; each column has its own unit. | MS2 charge fractions          |
| **Matrix**       | Rectangular array | 2D array of homogeneous numeric values.                       | Ion-mobility intensity matrix |

See the [CV Term Usage Guide](TODO:link) for details on how each type is encoded in mzQC.

---

## Putting It All Together

Each QC metric term in the PSI-MS CV will therefore include seven semantic relationships:

| Relationship                  | Refers to              | Example value                      |
| ----------------------------- | ---------------------- | ---------------------------------- |
| `part_of_workflow_stage`      | Workflow stage         | chromatography stage               |
| `measures_property`           | Analytical dimension   | chromatographic performance metric |
| `depends_on_data_type`        | Information dependency | raw acquisition data               |
| `has_measurement_scope`       | Aggregation level      | run level                          |
| `applies_to_acquisition_mode` | Acquisition strategy   | acquisition mode independent       |
| `has_quality_directionality`  | Interpretation         | lower is better                    |
| `has_value_type`              | Value structure        | tuple                              |

These relationships together provide a complete, machine-readable semantic description of any QC metric.

In conclusion:

* Each dimension describes a different facet of a QC metric.
* Together they make the CV complete, consistent, and queryable.
* Contributors defining new metrics should select one subclass from each dimension.
* Developers can use these relationships to automatically filter, group, and interpret QC results.

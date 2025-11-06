---
layout: page
title: "Metrics – Term Creation Guide"
permalink: /metrics/create
---

*How to define and request new QC metrics for the PSI-MS Controlled Vocabulary.*

## What this guide is for

This document explains how to **request new QC metric terms** or **update existing ones** in the [PSI-MS Controlled Vocabulary](https://github.com/HUPO-PSI/psi-ms-CV).
It shows:

* what information to include,
* how to write clear definitions, and
* how to classify metrics in line with the QC metric ontology used in mzQC.

These guidelines ensure that all QC metrics:

* are **semantically consistent** and **machine-readable**,
* fit naturally into mzQC and related PSI formats, and
* remain **traceable** to their scientific or software origin.

This guide applies to QC metrics from **proteomics**, **metabolomics**, and related mass spectrometry workflows.

## How to request a new QC metric

All new terms are proposed through GitHub:

1. Go to the [PSI-MS-CV repository](https://github.com/HUPO-PSI/psi-ms-CV).
2. Create a new issue using the **"New QC Term"** template.
3. Fill in the required fields (see below).
4. Discuss the proposal with maintainers in the issue comments.
5. Once approved, curators assign an accession number (`MS:4000XXX`) and add the term to the next CV release.

If you're refining or updating an existing term, just open an issue referencing its ID.

> [!NOTE]
> Expect some discussion — the maintainers help ensure consistency and alignment with existing terms.

## Before you start

Check first:

* Search the CV (e.g., via [OLS](https://www.ebi.ac.uk/ols/ontologies/ms)) to make sure that your metric doesn't already exist.
* Verify that your metric is not just a variant or combination of an existing one.
* Gather supporting documentation (publications, software references, mzQC examples).

If you find something close but not identical, note that in your request — it helps curators decide whether to extend or merge existing terms.

## What information you'll need

Each new QC metric request must contain:

| **Element** | **What to provide** |
| --- | --- |
| **Name** | Short, descriptive title for the metric. Example: `XIC-FWHM quantiles`. |
| **Definition** | One or two sentences explaining what the metric measures, how it is summarized, and what its values mean. |
| **Comment** | *(Optional)* Additional details about computation, conventions, or interpretation. |
| **Units** | Physical or statistical unit (e.g., `UO:0000010 ! second`, `UO:0000187 ! percent`). |
| **Value type** | Structural type of the metric value: single value, tuple, table, or matrix. |
| **Semantic classification** | Seven relationships that describe what kind of metric this is (see below). |
| **Provenance** | The origin of the metric (software or publication), e.g. `xref: QuaMeter:XIC-FWHM-Q1 [PMID:24494671]`. |

> [!TIP]
> Keep names short and specific.
> Avoid tool names in the title — use `xref` for that.

## Example of a complete metric definition

Here's what a complete metric definition looks like:

```obo
[Term]
id: MS:4000051
name: XIC-FWHM quantiles
def: "Summarizes the distribution of chromatographic peak widths, expressed as the full width at half maximum (FWHM) of extracted ion chromatograms (XICs). Reports an ordered tuple of the first through (n-1)-th quantiles (Q1, ..., Qn-1) of the FWHM distribution within a single run. Lower values indicate narrower peaks and therefore better chromatographic performance."
comment: "Values are reported as an (n-1)-element tuple of floating-point numbers in seconds, representing the first to (n-1)-th quantiles of the FWHM distribution. The final quantile (100th percentile) is omitted because it corresponds to the maximum observed peak width, which is a boundary value that does not convey additional information about distribution shape or variability and is sensitive to outliers. The tuple length implicitly specifies how many quantiles are reported and thus the resolution of the summary."

! --- Ontology classification ---
is_a: MS:4000XXX ! chromatographic performance metric
relationship: part_of_workflow_stage MS:XXXXXXX ! chromatography stage
relationship: depends_on_data_type MS:XXXXXXX ! raw acquisition data
relationship: has_measurement_scope MS:XXXXXXX ! run level
relationship: applies_to_acquisition_mode MS:XXXXXXX ! acquisition mode independent
relationship: has_quality_directionality MS:XXXXXXX ! lower is better
relationship: has_value_type MS:XXXXXXX ! tuple

! --- Quantitative semantics ---
relationship: has_value_concept MS:1000086 ! full width at half-maximum
relationship: has_value_concept STATO:0000291 ! quantile
relationship: has_units UO:0000010 ! second
relationship: has_value_type xsd:float

! --- Provenance ---
xref: QuaMeter:XIC-FWHM-Q1 [PMID:24494671]
xref: QuaMeter:XIC-FWHM-Q2 [PMID:24494671]
xref: QuaMeter:XIC-FWHM-Q3 [PMID:24494671]
```

## How QC metrics are classified

QC metrics can be categorized according to several classification dimensions.
These specify *what kind of metric it is*, *where it belongs in the workflow*, *what data it uses*, and *how its values behave*.

### Analytical dimension: inheritance via `is_a`

This dimension defines **what kind of metric** you are creating — it represents the metric's *type*.

**Syntax:**

```obo
is_a: MS:XXXXXXX ! chromatographic performance metric
```

**Examples:**
`chromatographic performance metric`, `mass accuracy metric`, `spectral quality metric`, `ionization quality metric`, `quantification precision metric`, etc.

This is the **only dimension** that uses `is_a`.
It places your metric correctly within the ontology's QC metric hierarchy.

### Typed relationships: contextual and structural properties

All other dimensions use a `relationship:` field.

| **Dimension**                   | **Relationship**              | **Example value**              | **Meaning**                                                          |
| ------------------------------- | ----------------------------- | ------------------------------ | -------------------------------------------------------------------- |
| **Workflow stage**              | `part_of_workflow_stage`      | `chromatography stage`         | Where in the experimental/computational workflow the metric applies. |
| **Information dependency type** | `depends_on_data_type`        | `raw acquisition data`         | What kind of data the metric depends on (raw, ID, quant, hybrid).    |
| **Measurement scope**           | `has_measurement_scope`       | `run level`                    | Level of aggregation (spectrum, run, batch, study).                  |
| **Acquisition strategy**        | `applies_to_acquisition_mode` | `acquisition mode independent` | Which acquisition mode/instrument the metric applies to.             |
| **Quality interpretation type** | `has_quality_directionality`  | `lower is better`              | How values relate to data quality.                                   |
| **Metric value type**           | `has_value_type`              | `tuple`                        | Structure of the metric value (single value, tuple, table, matrix).  |

Each dimension has predefined subclasses described in the [QC Metric Classification Reference](/metrics/classification). Use that reference when selecting the appropriate classification terms for your new metric.

## Quantitative details: what the numbers mean

Add relationships describing what the metric's numeric values represent:

| **Relationship**    | **Purpose**                                                                                           | **Example**                                                           |
| ------------------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `has_value_concept` | Defines what the values represent                                                                     | `MS:1000086 ! full width at half-maximum`, `STATO:0000291 ! quantile` |
| `has_units`         | Defines the physical/statistical unit (preferably from [UO](https://www.ebi.ac.uk/ols/ontologies/uo)) | `UO:0000010 ! second`, `UO:0000187 ! percent`                         |
| `has_value_type`    | Defines the data type (XML schema literal)                                                            | `xsd:float`, `xsd:int`                                                |

These fields help mzQC readers and validation tools understand how to process the data.

## Writing clear definitions and comments

**Good definitions:**

* Start with what the metric summarizes — **don't** begin with "A QC metric that..."
* Mention the data type or entity, and the summary statistic.
* End with an interpretation if relevant ("Lower values indicate better performance").

**Comments:**

Use `comment:` only to clarify:

* Implementation details (e.g., number of values, normalization).
* Context or rationale (e.g., why a value is omitted).

Avoid repeating the definition.

## Provenance and references

Always record where the metric originates:

```obo
xref: QuaMeter:XIC-FWHM-Q1 [PMID:24494671]
```

* Use PMIDs or DOIs when available.
* If multiple related metrics exist (e.g. Q1, Q2, Q3), include multiple `xref:` lines.

## Updating or extending metrics

If you want to improve an existing term (e.g., clearer definition, missing relationships):

* Open an issue referencing the metric ID.
* Explain what should change and why.
* Curators will review and update or merge as appropriate.

Deprecated metrics are marked with:

```obo
is_obsolete: true
replaced_by: MS:XXXXXXX
```

## Quick reference

**When defining new metrics:**

* ✅ Use `is_a` for the analytical dimension (metric type).
* ✅ Add one `relationship:` for each of the six other classification dimensions.
* ✅ Include quantitative metadata (`has_value_concept`, `has_units`, `has_value_type`).
* ✅ Add provenance (`xref:`).
* ✅ Ensure that the metric name and definition are unique.

**Avoid:**

* ❌ Tool names in the metric name.
* ❌ Definitions that describe algorithms instead of meaning.
* ❌ Redundant comments or duplicated phrasing.

### See also

* [**QC Metric Classification Reference:**](/metrics/classification) full list of subclasses, definitions, and examples.
* [**QC Metric Usage Guide:**](/metrics/use) how each value type (single, tuple, table, matrix) is encoded in mzQC.

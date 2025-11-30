---
layout: page
title: "Metrics – Usage Guide"
permalink: /metrics/use/
---

*How to use QC CV terms correctly in mzQC files.*

## Introduction

This guide explains **how to use QC metric CV terms** from the [PSI-MS Controlled Vocabulary](https://github.com/HUPO-PSI/psi-ms-CV) when creating or reading **mzQC files**.
You don't need to be an ontology expert — just follow these examples to ensure your QC data is:

* **Standardized** (compatible across tools),
* **Machine-readable** (interpretable by validators), and
* **Traceable** (linked to known metrics in the PSI-MS CV).

## How CV metrics map to mzQC

Each QC metric in mzQC corresponds to one entry in the PSI-MS CV (`MS:4000XXX`).
That entry defines:

* The **metric name** and **definition**,
* Its **units** and **value type**,
* Its **semantic classification**, describing where it applies and what it measures.

When you reference a CV term in your mzQC file, you're telling mzQC-compatible software **exactly what kind of data this metric represents**.

Example (simplified):

```json
{
    "accession": "MS:4000059",
    "name": "number of MS1 spectra",
    "value": 8259,
    "unit": {
        "accession": "UO:0000189",
        "name": "count unit"
    }
}
```

## Metric value types

Each QC metric defines **how its values are structured**, using the `has_value_type` relationship.
mzQC supports four value structures:

| Value type       | Structure                        | Example use                           |
| ---------------- | -------------------------------- | ------------------------------------- |
| **Single value** | One numeric or categorical value | number of MS1 spectra                 |
| **Tuple**        | Ordered list of values           | quantiles, summary statistics         |
| **Table**        | Named columns with multiple rows | precursor charge fractions            |
| **Matrix**       | Rectangular numerical array      | image-like data, correlation matrices |

Your mzQC file must follow the value structure declared in the CV.

## Single-value metrics

**Definition:**
A metric represented by one scalar value (numeric or categorical).

**mzQC encoding:**

* Directly report the single value in the `"value"` field.
* Include the `"unit"` object if defined in the CV.
* The data type (integer, float, string) must match the CV's declared `xsd:` type.

**Example:**

CV definition:

```obo
[Term]
id: MS:4000059
name: number of MS1 spectra
def: "Counts the number of MS1 scans within a single run."
is_a: MS:4000XXX ! acquisition coverage metric
relationship: part_of_workflow_stage MS:4000XXX ! mass spectrometry acquisition stage
relationship: depends_on_data_type MS:4000XXX ! raw acquisition data
relationship: has_measurement_scope MS:4000XXX ! run level
relationship: applies_to_acquisition_mode MS:4000XXX ! acquisition mode independent
relationship: has_quality_directionality MS:4000XXX ! higher is better
relationship: has_value_type MS:4000XXX ! single value
relationship: has_units UO:0000189 ! count unit
relationship: has_value_type xsd:int
xref: QuaMeter:MS1-Count [PMID:24494671]
```

mzQC representation:

```json
{
    "accession": "MS:4000059",
    "name": "number of MS1 spectra",
    "value": 8259,
    "unit": {
        "accession": "UO:0000189",
        "name": "count unit"
    }
}
```

## Tuple metrics

**Definition:**
A metric consisting of an ordered list of scalar values (e.g. quantiles, min/median/max triplets).
All values share the same semantic meaning and unit.

**mzQC encoding:**

* The `"value"` field is a JSON array of numbers.
* Include a single `"unit"` object applying to all elements.
* The CV term defines the interpretation (e.g., "first to (n−1)-th quantiles").

**Example:**

CV definition:

```obo
[Term]
id: MS:4000062
name: MS2 density quantiles
def: "Summarizes the distribution of spectral peak density in MS2 scans as quantiles of the number of fragment peaks per spectrum within a single run. The metric reports an ordered tuple of the first through (n−1)-th quantiles (Q1, ..., Qn−1), characterizing the overall fragmentation complexity and consistency across spectra."
comment: "Values are reported as an (n−1)-element tuple of counts, representing the first to (n−1)-th quantiles of the distribution of fragment peak counts per MS2 spectrum. The final quantile (100th percentile) is omitted because it corresponds to the maximum observed peak count, which is a boundary value that does not convey additional information about distribution shape or variability and is sensitive to outliers. The tuple length implicitly specifies how many quantiles are reported and thus the resolution of the summary. Lower quantiles correspond to sparsely fragmented spectra; higher quantiles indicate spectra with more peaks. Interpretation depends on the acquisition and fragmentation settings and should be treated as context dependent rather than strictly higher- or lower-is-better."
is_a: measures_property MS:4000XXX ! spectral quality metric
relationship: part_of_workflow_stage MS:4000XXX ! mass spectrometry acquisition stage
relationship: depends_on_data_type MS:4000XXX ! raw acquisition data
relationship: has_measurement_scope MS:4000XXX ! run level
relationship: applies_to_acquisition_mode MS:4000XXX ! acquisition mode independent
relationship: has_quality_directionality MS:4000XXX ! context dependent
relationship: has_value_type MS:4000XXX ! tuple
relationship: has_value_concept STATO:0000291 ! quantile
relationship: has_units UO:0000189 ! count unit
relationship: has_value_type xsd:int
xref: QuaMeter:MS2-Density-Q1 [PMID:24494671]
xref: QuaMeter:MS2-Density-Q2 [PMID:24494671]
xref: QuaMeter:MS2-Density-Q3 [PMID:24494671]
```

mzQC representation:

```json
{
    "accession": "MS:4000062",
    "name": "MS2 density quantiles",
    "value": [162, 250, 404],
    "unit": {
        "accession": "UO:0000189",
        "name": "count unit"
    }
}
```

## Table metrics

**Definition:**
A metric represented as columns of equal-length lists, each describing one variable.
Essentially a named column table with one row per observation.

**mzQC encoding:**

* `"value"` is an object where each key is a column identifier and its value is a list.
* Each column has an optional unit.
* All columns must have identical list lengths — each index corresponds to one row.
* Units are provided as an array under `"unit"` and as part of the column definition.

**Example:**

CV definition:

```obo
[Term]
id: MS:4000063
name: MS2 known precursor charge fractions
def: "Fraction of MS/MS precursors for each charge state observed within a run. Each entry lists a precursor charge (z) and its corresponding fraction of all observed MS2 precursors."
comment: "Values are reported as a table with two columns: 'Charge state' and 'Fraction'. The final charge state bin should be interpreted as 'that charge state or higher' to include all unlisted higher charges."
is_a: MS:4000XXX ! ionization quality metric
relationship: part_of_workflow_stage MS:4000XXX ! ionization stage
relationship: depends_on_data_type MS:4000XXX ! raw acquisition data
relationship: has_measurement_scope MS:4000XXX ! run level
relationship: has_value_type MS:4000XXX ! table
relationship: has_column MS:1000041 ! charge state
relationship: has_column UO:0000191 ! fraction
relationship: has_value_type xsd:float
```

mzQC representation:

```json
{
    "accession": "MS:4000063",
    "name": "MS2 known precursor charge fractions",
    "value": {
        "MS:1000041": [1, 2, 3, 4, 5, 6],
        "UO:0000191": [0.000, 0.683, 0.305, 0.008, 0.002, 0.002]
    },
    "unit": [
        {
            "accession": "MS:1000041",
            "name": "charge state"
        },
        {
            "accession": "UO:0000191",
            "name": "fraction"
        }
    ]
}
```

## Matrix metrics

**Definition:**
A metric that stores a rectangular grid of numeric values of the same type and unit.

**mzQC encoding:**

* `"value"` is a rectangular list of lists of numbers (each inner list = a matrix row).
* A single `"unit"` applies to all entries.
* Only homogeneous numeric types are allowed (no mixed datatypes).

## Understanding hierarchy and relationships

Each QC metric term in the CV encodes its semantics in two ways:

* The `is_a` hierarchy specifies *what kind of metric* it is (the analytical dimension).
* The typed `relationship`s describe *where and how* it applies.

| Ontology element              | Describes                             | Example                              |
| ----------------------------- | ------------------------------------- | ------------------------------------ |
| `is_a`                        | Type of metric (analytical dimension) | `chromatographic performance metric` |
| `part_of_workflow_stage`      | Experimental or computational stage   | `chromatography stage`               |
| `depends_on_data_type`        | Type of data used                     | `raw acquisition data`               |
| `has_measurement_scope`       | Level of aggregation                  | `run level`                          |
| `applies_to_acquisition_mode` | Acquisition mode                      | `DIA-specific metric`                |
| `has_quality_directionality`  | Interpretation of values              | `lower is better`                    |
| `has_value_type`              | Structure of the value                | `tuple`                              |

These relationships make each metric comparable, searchable, and logically complete while maintaining a clean metric taxonomy.

For full details and all available subclasses (e.g., analytical metric types, workflow stages, or acquisition modes), see the [QC Metric Classification Reference](../classification).

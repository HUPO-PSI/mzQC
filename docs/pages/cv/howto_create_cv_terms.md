---
layout: page
title: "Metrics - create"
permalink: /metrics/create
---
# CV Term Creation Guide

New CV terms have to be requested via the [PSI-MS CV issue tracker](https://github.com/HUPO-PSI/psi-ms-CV/issues).
Upon creating a new issue, you should select the "New QC Term" template.
This will guide you in providing the necessary information to request your new CV term, as detailed below.
If additional information or clarifications beyond the initial request are needed, the mzQC working group will work with you to finalize your CV term request.
When all the necessary information has been provided, a new CV term will be created based on the request and added to the PSI-MS CV.

## Required Information

Each metric (and CV entry request) MUST include the following information

- Name: A (short) string describing your metric.
- Definition: A longer description. This MUST include information about how the metric should be represented in an mzQC file.
- Comment: OPTIONAL details on how the metric should be interpreted (e.g. is a higher value better, can it only be interpreted relative to...).
- Value type:  Is the metric type a single value, an n-tuple, a table, or a matrix?
- Unit: OPTIONAL unit of the value, specified using an existing CV term.
- Categorization: A categorization can OPTIONALLY be supplied. Examples are whether the metric depends on spectrum, peptide, protein, or metabolite identifications; or to describe the metric context.

## Restrictions

The text in `Name`, `Definition`, and `Comment` MUST NOT contain escaped characters, such as `\"`, or special characters, such as backticks (`` ` ``).
If you need to quote words or sentences, use single quotes, e.g. `def: "A QC metric describes the basis for the metric calculation like 'one MS run' or 'one spectrum'." [PSI:MS]`.
Further restrictions to some term elements may apply; please see details in the [Term Element Details](#term-element-details) section.

## Example CV term

```
[Term]
id: MS:4000059
name: number of MS1 spectra
def: "The number of MS1 events in the run." [PSI:MS]
subset: mzQC
comment: An unusual low number may indicate incomplete sampling/scan rate of the MS instrument, low sample volume and/or failed injection of a sample.
synonym: "MS1-Count" EXACT [PMID:24494671]
is_a: MS:4000003 ! single value
relationship: has_metric_category MS:4000009 ! ID free metric
relationship: has_metric_category MS:4000012 ! single run based metric
relationship: has_metric_category MS:4000021 ! MS1 metric
relationship: has_value_type xsd:int ! The allowed value-type for this CV term
relationship: has_units UO:0000189 ! count unit
```

## Term Element Details

### ID

```
id: MS:4000059
```

Each term MUST have a unique ID, specified as `MS:XXXXXXX`.
Metric IDs are immutable and not reusable (e.g. for redefinition), and will be assigned upon inclusion or redefinition.

### Name

```
name: number of MS1 spectra
```

Each CV term MUST have a human-readable name.
The name SHOULD be informative, SHOULD consist of maximum 100 characters, and SHOULD only consist of alphanumeric 7-bit ASCII characters, spaces, and punctuation marks ([\-_,\.]).

### Definition

```
def: "The number of MS1 events in the run." [PSI:MS]
```

The definition SHOULD consist of a short explanation of the term and how it should be stored in the mzQC file.
The description SHOULD also provide aid in interpreting the values.
The definition section SHOULD NOT contain calculation or interpretation details, but rather it should explain the purpose, requirements, and scope of the metric.

### Comment

```
comment: An unusual low number may indicate incomplete sampling/scan rate of the
MS instrument, low sample volume and/or failed injection of a sample.
```

The comment section SHOULD contain calculation and interpretation details, like whether smaller or larger values are desirable.
It is also RECOMMENDED to give a short explanation about how the metric works.
If the metric calculation is not obvious, the calculation is RECOMMENDED to be briefly described in common terms.
For published metrics, it is also RECOMMENDED to refer to the corresponding code.

### Value Type and Unit

```
is_a: MS:4000003 ! single value
relationship: has_value_type xsd:int ! The allowed value-type for this CV term
relationship: has_units UO:0000189 ! count unit
```

A single value metric with a count as unit (`UO:0000189`).

```
is_a: MS:4000003 ! single value
relationship: has_value_type xsd:float ! The allowed value-type for this CV term
relationship: has_value_concept STATO:0000237 ! standard deviation
relationship: has_units UO:0000221 ! dalton
```

A single value metric with as unit Dalton (`UO:0000221`) and as value concept the standard deviation (`STATO:0000237`), for example, the standard deviation of the distribution of precursor mass errors of identified spectra.

Each term that reports a value MUST indicate the corresponding value type using an `is_a` relation.
Different value types are possible: single value (`MS:4000003`), n-tuple (`MS:4000004`), table (`MS:4000005`), or matrix (`MS:4000006`).
A value must be associated with a unit, see below.
The allowed data type of the value is given with `has_value_type` (e.g. `xsd:int` or `xsd:float`).
Depending on the value type, different additional categorization is REQUIRED.

- **single value:** Unit specification using `has_units` is REQUIRED, specification of a value concept using `has_value_concept` is RECOMMENDED.
- **n-tuple:** An ordered list/array of length 'n'. Unit specification using `has_units` is REQUIRED, specification of a value concept using `has_value_concept` is RECOMMENDED.
Units and value concepts (optional) MUST be uniform for all values.
An n-tuple is represented by a JSON array, which implicitly defines its length 'n'.
- **table:** A table MUST have one or more columns defined using `has_column` and MAY have optional columns defined using `has_optional_column`.
A table is represented using a JSON key–value object where key(s) represent the column term names/accessions and the value(s) are JSON arrays of uniform value type and
length.
- **table column definitions:** Each column is defined by referencing an existing CV term. The term name will be used as the column's header, and the units of the column are implied by the referenced term.
- **matrix:** Unit specification using `has_units` is REQUIRED, specification of a value concept using `has_value_concept` is RECOMMENDED.
Units and value concepts (optional) MUST be uniform for all values.
A matrix is represented by a JSON array of JSON arrays where the inner arrays MUST be of uniform length, which implicitly defines the matrix dimensions.

Units SHOULD be sourced from the [Units of Measurement Ontology (UO)](https://www.ebi.ac.uk/ols/ontologies/uo), if available, otherwise from the
[Statistical Methods Ontology (STATO)](http://stato-ontology.org/) or others as necessary.
Protein modifications SHOULD be sourced from [Unimod](http://www.unimod.org/) or [PSI-MOD](https://github.com/HUPO-PSI/psi-mod-CV) where possible.

### Metric Categorization

```
relationship: has_metric_category MS:4000009 ! ID free metric
relationship: has_metric_category MS:4000012 ! single run based metric
relationship: has_metric_category MS:4000021 ! MS1 metric
relationship: has_relation MS:1000285 ! total ion current
```

Different types of categorization can be assigned to CV terms.
First, it is RECOMMENDED to specify whether a metric requires identification information to be computed (ID based, `MS:4000008`) or not (ID free, `MS:4000009`).
Second, additional categories to describe the metric context (from which data the metric is derived, to which element of the instrumental setup the metric pertains, etc.) can be specified as well, using `has_metric_category`.
The `has_relation` relation can be used to link a metric to the measured quantity or data it is derived from.
It is RECOMMENDED to align the categorization of novel metrics to existing terms to facilitate consumption of related metrics.

```
relationship: has_units UO:0000010 ! second
relationship: has_column MS:1000041 ! charge state
```

If the metric term has an associated value, its unit MUST be defined using the `has_units` relationship.
"Single", "n-tuple", and "matrix" type values MUST be assigned a single, uniform unit type with `has_units`.
For "table" type values, one or more `has_column` specifications (and optionally `has_optional_column` specifications) MUST be associated with the table.
These implicitly define the column units through the units of the referenced column terms.

```
relationship: has_value_concept STATO:0000237 ! standard deviation
```

For full semantic integration, it is RECOMMENDED to specify the value concept for automatic processing and interpretation of the value.
It is RECOMMENDED to source value concepts from [STATO](http://stato-ontology.org/).

### Additional Information

```
synonym: "MS1-Count" EXACT [PMID:24494671]
```

In case of reimplementing, renaming, or redefining a metric, it is RECOMMENDED to also add synonym attributes with either the name or ID of the initial metric.
It is not required for the initial metric to be included in any controlled vocabulary, but the name SHOULD be unambiguous and recognizable (e.g. from the source publication).
Synonyms can be "RELATED" (the defined metric is similar, but not the same as what is connected with the synonym name), "NARROW" (the metric's values can be identically interpreted as in the meaning of the synonym metric, however, definition and calculation may somewhat differ), "EXACT" (the defined metric is basically a result of renaming).

## More CV Term Examples

**Single value:**

```
[Term]
id: MS:4000050
name: XIC50 fraction
def: "The number of XIC that account for the top half of all XIC-FWHM divided by the number of all XIC." [PSI:MS]
subset: mzQC
synonym: "XIC-WideFrac" EXACT [PMID:24494671]
is_a: MS:4000003 ! single value
relationship: has_metric_category MS:4000009 ! ID free metric
relationship: has_metric_category MS:4000012 ! single run based metric
relationship: has_value_type xsd:float ! The allowed value-type for this CV term
relationship: has_units UO:0000191 ! fraction
```

**n-tuple:**

```
[Term]
id: MS:4000051
name: XIC-FWHM quantiles
def: "The first to n-th quantile of peak widths for XICs. A metric's value triplet represents the related QuaMeter metrics of XIC-FWHM-Q1,Q2,Q3." [PSI:MS]
subset: mzQC
synonym: "XIC-FWHM-Q1" RELATED [PMID:24494671]
synonym: "XIC-FWHM-Q2" RELATED [PMID:24494671]
synonym: "XIC-FWHM-Q3" RELATED [PMID:24494671]
is_a: MS:4000004 ! n-tuple
relationship: has_metric_category MS:4000009 ! ID free metric
relationship: has_metric_category MS:4000012 ! single run based metric
relationship: has_metric_category MS:4000018 ! XIC metric
relationship: has_value_type xsd:float ! The allowed value-type for this CV term
relationship: has_value_concept MS:1000086 ! full width at half-maximum
relationship: has_value_concept STATO:0000291 ! quantile
relationship: has_units UO:0000010 ! second
```

**Table:**

```
[Term]
id: MS:4000063
name: MS2 known precursor charges fractions
def: "The fraction of MS/MS precursors of the corresponding charge. The fractions [0,1] are given in the 'Fraction' column, corresponding charges in the 'Charge state' column. The highest charge state is to be interpreted as that charge state or higher." [PSI:MS]
subset: mzQC
synonym: "MS2-PrecZ-1" NARROW [PMID:24494671]
synonym: "MS2-PrecZ-2" NARROW [PMID:24494671]
synonym: "MS2-PrecZ-3" NARROW [PMID:24494671]
synonym: "MS2-PrecZ-4" NARROW [PMID:24494671]
synonym: "MS2-PrecZ-5" NARROW [PMID:24494671]
synonym: "MS2-PrecZ-more" NARROW [PMID:24494671]
is_a: MS:4000005 ! table
relationship: has_metric_category MS:4000009 ! ID free metric
relationship: has_metric_category MS:4000012 ! single run based metric
relationship: has_metric_category MS:4000020 ! ion source metric
relationship: has_metric_category MS:4000022 ! MS2 metric
relationship: has_column MS:1000041 ! charge state
relationship: has_column UO:0000191 ! fraction
```

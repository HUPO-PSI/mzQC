---
layout: page
title: "Metrics - create"
permalink: /metrics/create
---
## CV Term Creation Guide

### New CV terms 
New CV terms have to be requested via the [mzQC GitHub issue tracker](https://github.com/HUPO-PSI/psi-ms-CV/issues/new?assignees=&labels=&template=new_qc_term.yml). 
This will produce a template that will guide you in providing the necessary information to request your new QC CV term, as detailed below. 
If additional information or clarifications beyond the initial request are needed, the mzQC working group will work with you to finalize your CV term request. 
When all the necessary information has been provided, a new CV term will be created based on the request and added to the QC CV.

### Requesting a new term

Anyone can request a new term be added to the controlled vocabulary by opening an issue or a pull
request against this repository. We'd appreciate any help you can contribute when submitting a new
term, from proposing the term name and description to defining its relationships and properties. 

Each metric (and CV entry request) MUST include the following information:

- Name: A (short) string describing your metric.
- Definition: A longer description. This MUST include information about how the 
metric should be represented in an mzQC file.
- Comment: OPTIONAL details on how the metric should be interpreted (e.g. is a 
higher value better, can it only be interpreted relative to...).
- Value type:  Is the metric type a single value, an n-tuple, a table, or a
matrix?
- Unit: OPTIONAL unit of the value, specified using an existing CV term.
- Categorization: A categorization can OPTIONALLY be supplied. Examples are 
whether the metric depends on spectrum, peptide, protein, or metabolite 
identifications; or to describe the metric context.

More information on how use CV terms and their translation to elements in an mzQC file is available in the following CV guide: [CV Term Usage Guide](cv/howto_use_cv_terms.md)

### Submitting a new term 

Please see the instructions of PSI-MS-CV for [submitting a new term](https://github.com/HUPO-PSI/psi-ms-CV/blob/master/README.md#submitting-a-new-term).

### Restrictions

The text in `Name`, `Definition`, and `Comment` MUST NOT contain escaped characters, such as `\"`, or special characters, such as backticks (`` ` ``).
If you need to quote words or sentences, use single quotes, e.g. `def: "A QC metric describes the basis for the metric calculation like 'one MS run' or 'one spectrum'." [PSI:QC]`.
Further restrictions to some term elements may apply; please see details in the [Term Element Details](#term-element-details) section.

#### ID

Each term MUST have a unique ID, specified as `QC:XXXXXXX`.
Metric IDs are immutable and not reusable (e.g. for redefinition), and will be assigned upon inclusion or redefinition.

#### Name

Each CV term MUST have a human-readable name.
The name SHOULD be informative, SHOULD consist of maximum 100 characters, and SHOULD only consist of alphanumeric 7-bit ASCII characters, spaces, and punctuation marks ([\-_,\.]).

#### Definition

The definition SHOULD consist of a short explanation of the term and how it should be stored in the mzQC file.
The description SHOULD also provide aid in interpreting the values.
The definition section SHOULD NOT contain calculation or interpretation details, but rather it should explain the purpose, requirements, and scope of the metric.

#### Comment

The comment section SHOULD contain calculation and interpretation details, like whether smaller or larger values are desirable.
It is also RECOMMENDED to give a short explanation about how the metric works.
If the metric calculation is not obvious, the calculation is RECOMMENDED to be briefly described in common terms.
For published metrics, it is also RECOMMENDED to refer to the corresponding code.

#### Value Type and Unit

A single value metric with as unit the standard deviation (`STATO:0000237`) in Dalton (`UO:0000221`), for example, the standard deviation of the distribution of precursor mass errors of identified spectra.

Each term that reports a value MUST indicate the corresponding value type using an `is_a` relation.
Different value types are possible: single value, n-tuple, table, or matrix.
A value must be associated with a unit, see below.
Depending on the value type, different additional categorization is REQUIRED.

- **single value:** Unit specification using `has_units` is REQUIRED, type specification using `has_type` is RECOMMENDED.
- **n-tuple:** An ordered list/array of length 'n'. Unit specification using `has_units` is REQUIRED, type specification using `has_type` is RECOMMENDED.
Units and types (optional) MUST be uniform for all values.
An n-tuple is represented by a JSON array, which implicitly defines its length 'n'.
- **table:** A table MUST have one or more columns defined using `has_column` and MAY have optional columns defined using `has_optional_column`.
A table is represented using a JSON key–value object where key(s) represent the column term names/accessions and the value(s) are JSON arrays of uniform value type and
length.
- **table column type definitions:** Unit specification using `has_units` is REQUIRED, type specification using `has_type` is RECOMMENDED.
The term name will be used as the column's header.
- **matrix:** Unit specification using `has_units` is REQUIRED, type specification using `has_type` is RECOMMENDED.
Units and types (optional) MUST be uniform for all values.
A matrix is represented by a JSON array of JSON arrays where the inner arrays MUST be of uniform length, which implicitly defines the matrix dimensions.

Units SHOULD be sourced from the [Units of Measurement Ontology (UO)](https://www.ebi.ac.uk/ols/ontologies/uo), if available, otherwise from the
[Statistical Methods Ontology (STATO)](http://stato-ontology.org/) or others as necessary.
Protein modifications SHOULD be sourced from [Unimod](http://www.unimod.org/) or [PSI-MOD](https://github.com/HUPO-PSI/psi-mod-CV) where possible.

#### Metric Categorization

Different types of categorization can be assigned to CV terms.
First, it is RECOMMENDED to specify whether a metric requires identification information to be computed (ID based) or not (ID free).
Second, additional categories to describe the metric context (from which data the metric is derived, to which element of the instrumental setup the metric pertains, etc.) can be specified as well.
It is RECOMMEND to align the categorization of novel metrics to existing terms to facilitate consumption of related metrics.

If the metric term has an associated value, its unit MUST be defined using the `property_value` tag.
"Single", "n-tuple", and "matrix" type values MUST be assigned a single, uniform unit type with `has_units`.
For "table" type values, one or more `has_column_type`/`has_optional_column_type` specifications MUST be associated with the table.
These implicitly define the column units through the `has_units` attributes of the corresponding column definitions.

For full semantic integration, it is RECOMMENDED to specify the value type for automatic processing and interpretation of the value.
It is RECOMMENDED to source value types from [STATO](http://stato-ontology.org/).

#### Additional Information

In case of reimplementing, renaming, or redefining a metric, it is RECOMMENDED to also add synonym attributes with either the name or ID of the initial metric.
It is not required for the initial metric to be included in any controlled vocabulary, but the name SHOULD be unambiguous and recognizable (e.g. from the source publication).
Synonyms can be "RELATED" (the defined metric is similar, but not the same as what is connected with the synonym name), "NARROW" (the metric's values can be identically interpreted as in the meaning of the synonym metric, however, definition and calculation may somewhat differ), "EXACT" (the defined metric is basically a result of renaming).

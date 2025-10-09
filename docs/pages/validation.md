---
title: "Validation process"
layout: default
permalink: "/validator/validation/"
---
# Validation of mzQC Files

Here we give a brief overview of syntactic and semantic validation requirements
of mzQC files. Full validation is implemented in the
[mzqc-pylib](https://github.com/bigbio/mzqc-pylib) reference implementation.

## Syntactic Validation

With the help of the mzQC JSON schema, mzQC instances can be readily checked for syntactic schema compliance.
There are a [number of JSON schema implementations for use in various programming languages](https://json-schema.org/tools) that also support validation of JSON schema draft-07 from which the mzQC schema is designed.

## Semantic Validation

Due to the advanced design of the mzQC JSON schema, many aspects of a valid mzQC
file can already be verified via syntactic validation without the need of
explicit semantic validation. There are, however, a few additional semantic
rules that need to be followed to create fully compliant mzQC files.

- All used `controlledVocabulary` elements MUST reference a valid ontology.
- All used CV terms (including the quality metrics) must be present in one of
the controlled vocabularies listed in the files `controlledVocabularies`
element, matching in name and accession.
- All `qualityMetric` elements MUST be unique within their `runQuality` or
`setQuality` parent.
- The value type of `qualityMetric` elements MUST match the specification in the
CV (i.e. single value, n-tuple, matrix, or table).
- The value of `qualityMetric` MUST match its unit definition (and type
implicitly).
- All columns of table `qualityMetric` elements MUST have the same length.
- `label` attributes in the metadata elements MUST be unique within its mzQC
file.
- All `inputFile` elements MUST have a unique `location` attribute within their
`runQuality` or `setQuality` element.

Additionally, more detailed checks might be performed to assess the validity of
specific metric values on a case-by-case basis (e.g., percentages should sum to
100%).

Find out about more details on the [validator page itself](../).

## Online Validation
mzQC is *web-native*, and integrates nicely with modern applications and websites. You can find one example on this website if you visit the [Validator](../).

We have several alternatives for validation, however. For these, have a look at the respective projects.

- [jmzqc](https://github.com/MS-Quality-Hub/jmzqc): Java library to create, process, and validate mzQC files.
- [pymzqc](https://github.com/MS-Quality-Hub/pymzqc): Python library to create, process, and validate mzQC files.

## Offline Validation
If you have many mzQC files to validate, or the validation API is temporaily unreachable,
you can set up your own validation process without much effort!

The pymzqc library now supports a offline validator:
```
mzqc-validator [OPTIONS] INFILE
```
You will have to install pymzqc python module, but the process is quick and easy thanks to pypi.
More details can be found at the [pymzqc site](https://pymzqc.readthedocs.io/).
The validator tool is a CLI tool built on click. 
It will generate a joint validation of syntax and semantics of a given mzQC input. The output is in json format. 
The validator will segment the validation report into lists of the following categories:

* “input files”: reports duplicate input files for sets or runs or inconsistent file name and location

* “label uniqueness”: checking if run and set labels are unique within the file,

* “metric use”: reports duplicate metric use within a set or run, and, if applicable, table consistency, unit use, “ontology load errors”: all controlled vocabularies that could not be loaded,

* “ontology term errors”: checks for ambiguous terms found in multiple of the used controlled vocabularies, terms used not found in any given controlled vocabulary, and correct name, definition, and reference usage,

* “schema validation”: report all elements not corresponding to the mzQC schema”,

* “ontology validation”: in case any non-online controlled vocabularies were used.

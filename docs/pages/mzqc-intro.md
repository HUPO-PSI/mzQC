---
layout: page
title: "Introduction to mzQC"
permalink: mzQC-intro/
---

The mzQC specification defines a simple yet versatile file format with a hierarchical structure to store quality metrics. Following is a ~5 minutes overview to mzQC:

## Basics
The format (`.mzQC` file extension) is hierarchically structured and CV controlled (see more below).
The format is realized in the widespread JavaScript Object Notation (JSON). 
Validation can be done with through our format JSON-schema.
It's schema is in JSON, too.

## Schema
The mzQC format can accommodate multiple metrics, possibly from multiple MS runs. 
Several dedicated (and named) data structures (arrays) are available for this purpose. 
These are named as the plural of the elements they provide space for, for example, the controlledVocabularies element contains controlledVocabulary objects.
The following schema visualisation illustrates the hierarchical relations of the mzQC elements.

![mzQC schema illustration](https://raw.githubusercontent.com/HUPO-PSI/mzQC/main/schema/mzqc_schema.jpg)

QC metrics in an mzQC file are grouped in “runQuality” or “setQuality” elements, depending on whether the metrics pertain to a single or multiple MS runs, respectively. Each runQuality or setQuality element contains a “metadata” section that provides information to track the provenance of the QC metrics, such as the originating MS run(s) and the software tool(s) used to calculate the metrics. QC metric values are stored in “qualityMetric” elements and can consist of single values, tuples, or tabular data. Additionally, each QC metric is defined by a corresponding term in the PSI-MS controlled vocabulary (19) for semantic annotation of the data and to ensure an unambiguous definition of each QC metric. 


## Structure
JSON data structures are built using two structures: 
* An (unordered) collection of key–value pairs, generally called an object.
An object begins with a left brace { and ends with a right brace }. Each name is followed by a colon and the key–value pairs are separated by a comma. Keys must be strings.

    Syntax: *{key_1: value_1, key_2: value_2}*

    Example: `{"precursor_charge": 2, "is_contaminant": true}`

* An (ordered) list of values, generally called an array or list. 
An array begins with a left bracket [ and ends with a right bracket ]. Values are separated by a comma. Value types can be mixed.

    Syntax: *[value_3, {"subobject": "value_4"}, value_5]*

    Example: `[true, {"precursor_charge": 42}, "text"]`

Values can be a string in double quotes, a number, a boolean value (true or false), null, an object, or an array. 
These structures can be nested; for example, multidimensional tables can be represented as arrays of arrays. 
Strings and values are like the respective C or Java structures. 
Syntactic validation is available through the usage of JSON Schema for annotation and validation of JSON documents.


## CV
The PSI-QC controlled vocabulary subsection (QC CV) of the PSI-MS CV defines quality metrics and related supporting values. 
Its main purpose is describing metrics related to mass spectrometry quality control, for which it builds on established terms and definitions from chemistry, physics, and biology ontologies. 
Another purpose is to provide the underlying definitions and specialized metrics for data structures usable within mzQC files. 
Initially included in the QC CV are a collection of published and basic metrics. 
Special care went into clearly defining the metrics and associated values to help interpretation, use, and visualization.

The QC CV is present in the `MS:4000000–MS:4999999` namespace of the PSI-MS CV. 
The CV is encoded as an OBO (Open Biological and Biomedical Ontologies) file that follows the [OBO specification](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_2.html). 
The OBO file format is a biology-oriented language for building ontologies, similar to the Web Ontology Language (OWL). 
The OBO Foundry maintains a comprehensive index of ontologies related to the life sciences.

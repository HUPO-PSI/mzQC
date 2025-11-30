---
layout: page
title: QC Metrics
permalink: /metrics/
---

The mzQC format achieves both _simplicity_ and _flexibility_ by using **Controlled Vocabulary (CV) terms** to describe quality metrics in a precise and machine-readable way.
These terms are defined within the [**PSI-MS Controlled Vocabulary (CV)**](https://github.com/HUPO-PSI/psi-ms-CV) and specify:

* what each metric measures,
* how it is computed and represented, and
* how it relates to specific workflow stages or data types.

This ensures that QC results are interoperable across software tools, consistent across datasets, and unambiguously interpretable by both humans and machines.

## Learn more about QC metric CV terms

Whether you're using, creating, or browsing metrics, the following pages explain everything you need to know:

### [Metric Classification Reference](classification/)

A taxonomy of QC metric categories and relationships.
Defines the seven classification dimensions used in mzQC and how they describe each metric's meaning, context, and structure.

### [Using QC Metrics](use/)

A hands-on guide for developers and tool integrators.
Learn how to reference, interpret, and serialize CV terms in mzQC files — including examples for single-value, tuple, table, and matrix metrics.

### [Creating New QC Metrics](create/)

Step-by-step instructions for proposing or updating QC metric terms in the PSI-MS CV.
Explains how to write clear definitions, select correct classifications, and provide provenance and quantitative details.

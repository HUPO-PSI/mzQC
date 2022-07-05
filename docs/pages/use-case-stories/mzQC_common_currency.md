---
layout: page
title: "mzQC: a 'common currency' for quality control of biological mass spectrometry"
permalink: /use-cases/mzQC-common-currency/
---

Quality control for biological mass spectrometry has, in recent years, become an increasingly established and mature field. This maturity has been reflected in the emergence of many quality control tools and metrics that are derived from instrumental data, many of which are being used more widely every month.


If the tools for generating, storing, analyzing, and visualizing quality metrics for experiments were able to express these metrics and analyses in a standard format, it would be easier for laboratories to try different sets of metrics to determine which work best to support their decision-making.  Downstream tools for detecting current instrument status, establishing comparability across many MS experiments, and evaluating repository data sets retrospectively could avoid the problem of working exclusively with the quality metrics used in their developers’ laboratories.  The Proteomics Standards Initiative of the Human Proteomics Organization launched the Quality Control working group in 2016 to design a data format that would allow this interoperability; with a shared means to communicate quality values, the use of these systems could spread throughout the biological MS community more rapidly.


The qcML specification, released in 2014, represented a significant effort to generate and codify a shared language for the exchange of mass spectrometry quality control data.


Whilst qcML represented a meaningful first draft of an exchange format for this data, a community standard to meet a diverse range of use cases from the biological mass spectrometry community was required. Such a format would enable not only the generation of new data in a coherent format, but also 


mzQC represents the first example of a PSI file format recommendation using Javascript object notation language (JSON), instead of the prior XML formats, for ease of generation, consumption and human readability.


Here, we describe the mzQC specification, along with possible use cases and an illustrative example of the subsequent analysis possibilities. Further to the format, we demonstrate several tools to calculate quality metrics and output in mzQC, as well as tools to consume these files for practical use.

1. Mass spec is the pre-eminent tool in molecular biology
2. Vast amounts of data is being produced and disseminated each year
3. Omics are transitioning to large (and even population) scale



---
Original draft: https://docs.google.com/document/d/1-vELNWwQC5yJvb8VNU8WJS5x3JLTlQkgF6uvsW1M4jk/edit

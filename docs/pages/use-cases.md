---
layout: page
title: "mzQC Use Cases"
permalink: /use-cases/
---
This page should give you a (non-exclusive) overview over the use cases covered by mzQC:

## Handover Format
It is easy with **mzQC** to get relevant QC info, easy to put your data into context (of measurement realities). That makes it a preferred medium to handover quality information. Read more about it in [mzQC at a glance](at-a-glance/) and explore [a small mzQC example](../examples/intro_run/).

## Quality Reports
With JSON at its core, mzQC follows a '_works online, works everywhere_' approach. Even for single spectra, as we show with the [universal spectrum identifier example](../examples/USI-example/).

## Archival
The format is an optimal QC tool for the analytical chemist and instrument operators keeping track (and archive) instrument performance. Read on with an [introduction to mzQC for anlytical chemists](analytical-chemists/) or explore our [QC sample example](../examples/QC2-sample-example/). You can even embed mzQC in mzML, should you choose to. [View an example here](../examples/mzml-mzqc-example/).

## Common currency
With mzQC for archival, quality reports, and as handover format, [mzQC can serve as a common currency](mzQC-common-currency/) for data repositories, journals, and collaborators.

## Bridge the *omics Gap: Metabolomics
A technology agnostic design makes QC with mzQC easy in other fields as well! Assuming you make per sample measurements (runs in mzQC parlance) and multiple groups of runs in a study (sets), then all you need is to define your metrics to open up the mzQC 'ecosystem' to your field. Explore in [this example](../examples/metabo-batches/), how easy you can include QC data from quite different instruments, employ advanced QC concepts like batch correction, and use metrics on expansive datasets. 

## Keep track of your study's runs as a whole
With mzQC you can keep track of the quality of all your study's runs. We show in [this example](../examples/set-of-runs/) how you can apply metrics to a whole set of runs. There are of course more scenarios in which you want to consider the quality of multiple runs, and you can read [more here](mzqc-multi/).

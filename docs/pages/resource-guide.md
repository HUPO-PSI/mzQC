---
layout: page
title: "mzQC Resources"
permalink: /resource-guide/
---

This is the guide to mzQC resources from software libraries, QC software supporting mzQC, to validation. 


## Core libraries
- [pymzqc](https://github.com/MS-Quality-Hub/pymzqc): Python library to create, process, and validate mzQC files.
It includes a Python object model, (de-)serialisation functions, syntactic validation, and semantic validation of mzQC files.
- [jmzqc](https://github.com/MS-Quality-Hub/jmzqc): Java library to create, process, and validate mzQC files.
It includes a Java object model, (de-)serialisation functions, syntactic validation, and semantic validation of mzQC files.
- [rmzqc](https://github.com/MS-Quality-Hub/rmzqc): R library to create, process, and validate mzQC files.
It includes a R object model, (de-)serialisation functions, syntactic validation, and semantic validation of mzQC files. In development.

## QC Software
Metrics generating software with mzQC support. Input formats are listed where known; for the others, see the tool's own documentation.
- [PTXQC](https://github.com/cbielow/PTXQC): An R package for creation of QC reports from MaxQuant results and OpenMS mzTab files. *Input: MaxQuant result tables, OpenMS mzTab.*
- [OpenMS](https://github.com/OpenMS/OpenMS): Open-source software C++ library for LC/MS data management and analyses. *Input: common LC/MS formats, e.g. mzML.*
- [QCCalculator](https://github.com/bigbio/qccalculator): Python tool for base QC metric calculation from mzML, mzIdentML, and MaxQuant input files. *Input: mzML, mzIdentML, MaxQuant output.*
- [Yamato / SwaMe / Prognosticator](https://github.com/PaulBrack/Yamato): SWATH-MS QC metrics generation tools. *Input: see the tool documentation.*
- [DIAuditor](https://github.com/dtabb73/DIAuditor): Infers the DIA isolation window scheme and reports acquisition quality metrics. *Input: mzML. Output: mzQC.*
- [MSstatsQC](https://bioconductor.org/packages/MSstatsQC/): R package for longitudinal system suitability monitoring with statistical control charts. *Reads mzQC.*
- QuaMeter: Multivendor QC metrics for LC-MS/MS data. *conversion scripts to mzQC are available.*
- [MsQuality](https://bioconductor.org/packages/release/bioc/html/MsQuality.html): An R Bioconductor package, which provides functionality to calculate quality metrics for mass spectrometry-derived, spectral data at the per-sample level. MsQuality relies on the mzQC framework of quality metrics. It supports the calculation of the following metrics.
  - chromatography duration (MS:4000053)
  - TIC quarters RT fraction (MS:4000054)
  - MS1 quarter RT fraction (MS:4000055)
  - MS2 quarter RT fraction (MS:4000056)
  - MS1 TIC-change quartile ratios (MS:4000057)
  - MS1 TIC quartile ratios (MS:4000058)
  - number of MS1 spectra (MS:4000059)
  - number of MS2 spectra (MS:4000060)
  - m/z acquisition range (MS:4000069)
  - retention time acquisition range (MS:4000070)
  - MS1 signal jump (10x) count (MS:4000097)
  - MS1 signal fall (10x) count (MS:4000098)
  - number of empty MS1 scans (MS:4000099)
  - number of empty MS2 scans (MS:4000100)
  - number of empty MS3 scans (MS:4000101)
  - MS2 precursor intensity distribution Q1, Q2, Q3 (MS:4000116)
  - MS2 precursor intensity distribution mean (MS:4000117)
  - MS2 precursor intensity distribution sigma (MS:4000118)
  - MS2 precursor median m/z of identified quantification data points (MS:4000152)
  - interquartile RT period for identified quantification data points (MS:4000153)
  - rate of the interquartile RT period for identified quantification data points (MS:4000154)
  - area under TIC (MS:4000155)
  - area under TIC RT quantiles (MS:4000156)
  - extent of identified MS2 precursor intensity (MS:4000157)
  - median of TIC values in the RT range in which the middle half of quantification data points are identified (MS:4000158)
  - median of TIC values in the shortest RT range in which half of the quantification data points are identified (MS:4000159)
  - MS2 precursor intensity range (MS:4000160)
  - identified MS2 precursor intensity distribution Q1, Q2, Q3 (MS:4000161)
  - unidentified MS2 precursor intensity distribution Q1, Q2, Q3 (MS:4000162)
  - identified MS2 precursor intensity distribution mean (MS:4000163)
  - unidentified MS2 precursor intensity distribution mean (MS:4000164)
  - identified MS2 precursor intensity distribution sigma (MS:4000165)
  - unidentified MS2 precursor intensity distribution sigma (MS:4000166)
  - ratio of 1+ over 2+ of all MS2 known precursor charges (MS:4000167)
  - ratio of 1+ over 2+ of identified MS2 known precursor charges (MS:4000168)
  - ratio of 3+ over 2+ of all MS2 known precursor charges (MS:4000169)
  - ratio of 3+ over 2+ of identified MS2 known precursor charges (MS:4000170)
  - ratio of 4+ over 2+ of all MS2 known precursor charges (MS:4000171)
  - ratio of 4+ over 2+ of identified MS2 known precursor charges (MS:4000172)
  - mean MS2 precursor charge in all spectra (MS:4000173)
  - mean MS2 precursor charge in identified spectra (MS:4000174)
  - median MS2 precursor charge in all spectra (MS:4000175)
  - median MS2 precursor charge in identified spectra (MS:4000176)

### A Hub for QC
If you are looking for a home to your QC software or library, check out [MS-Quality-Hub](https://github.com/MS-Quality-Hub). All the above libraries have their development home there and some other very useful repositories.


## QC controlled vocabulary
All mzQC metrics are defined as terms in the QC namespace of the PSI-MS controlled vocabulary (`MS:4000000` to `MS:4999999`). You can browse them in the [EBI Ontology Lookup Service](https://www.ebi.ac.uk/ols4/ontologies/ms). To propose a new metric, see the [metrics page](https://hupo-psi.github.io/mzQC/metrics/) and our [contribution guide](https://github.com/HUPO-PSI/mzQC/blob/main/CONTRIBUTING.md).

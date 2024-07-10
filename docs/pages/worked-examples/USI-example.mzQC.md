---
layout: page
title: "USI Example of mzQC"
permalink: /examples/USI-example/
---

Here, we describe a mzQC JSON document to exemplify the use of Universal Spectrum Identifiers ([USI](https://doi.org/10.1038%2Fs41592-021-01184-6])
to address the quality of specific spectra by metrics recorded in a table value type.


Find the complete example file at the bottom of this document or in the [examples folder](https://github.com/HUPO-PSI/mzQC/tree/main/specification_documents/examples).

We explained the basic structure of an mzQC in [previous examples](https://hupo-psi.github.io/mzQC/examples/) (e.g. intro_run.mzQC) and here dive directly into the details. 
The metric values are derived from spectra of a particular run in the CPTAC project, acquired on a Thermo Orbitrap Velos instrument.
For purposes of examplification the original run was truncated to the first 10 MS/MS spectra.
```
        "inputFiles": [
          {
            "location": "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2014/09/PXD000966/CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09.mzML.gz",
            "name": "CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09.trfr.t3.mzML.gz",
            "fileFormat": {
              "accession": "MS:1000584",
              "name": "mzML format"
            },
```
The metric gauges each considered spectra's TIC in relation to the peak intensities. 
It does so by calculating the (minimal) fraction of peaks neccessary to sum up to half the total intensity of the spectrum itself.
Thus, the metric value will range between 0 and 1, where values closer to 0 will indicate spectra whose TIC is dominated by a few high intensity peaks.
```
        "qualityMetrics": [
        {
          "accession": "MS:4000068",
          "name": "spectra half-TIC",
          "value": {
```
The values for this metric are recorded in a table defined by the CV Term [MS:4000068](https://github.com/HUPO-PSI/psi-ms-CV/blob/be1085ed502ef6efc17ec896a03f4154e13428cc/psi-ms.obo#L22927) and consist of a column for the spectrum reference and a second column for the fractional value ("UO:0000191").
The spectrum reference is defined by the CV as either the NativeID and/or preferrably the USI in a separate column, of which at least one has to be present.
In our case, as the originating MS-run is available via ProteomExchange, and the USI is a more detailed version of NativeID, no NativeID column is given.
```
            "MS:1003063": [
              "mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:2",
              "mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:7",
              "mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:29",
              "mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:31",
              "mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:34",
              "mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:43",
              "mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:45",
              "mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:48",
              "mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:50",
              "mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:51"
            ],
            "UO:0000191": [
              0.1134,
              0.1628,
              0.0536,
              0.102,
              0.1042,
              0.0947,
              0.0784,
              0.1239,
              0.2593,
              0.1214
            ]
          }
        }
      ],
```
As you can see from the values in the fractional value (UO:0000191) column, 
most of the first ten spectra cluster around a value of about 10% of the peaks dominating the respective spectras' TIC, 
with only a few outliers to the 25% and the 5% range.
Each row represents one spectrum that can be directly looked up. For USI, 
[even directly from the web](https://www.ebi.ac.uk/pride/archive/usi?usi=mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_05_2Feb12_Cougar_11-10-09:scan:2).

### This is the mzQC file once again, in full:
**[USI-example.mzQC](https://github.com/HUPO-PSI/mzQC/blob/main/specification_documents/examples/USI-example.mzQC)**
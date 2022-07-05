---
layout: page
title: "USI Example of mzQC"
permalink: /examples/USI-example/
---

Here, we describe a mzQC JSON document to exemplify the use of USI to address the quality of specific spectra by metrics recorded in a table value type.


Find the complete example file at the bottom of this document or in the example folder.

We explained the basic structure of an mzQC in previous examples (e.g. individual-runs.mzQC) and here dive directly into the details. 
The metric values are derived from spectra of a particular run in the CPTAC project, acquired on a Thermo Orbitrap Velos instrument.
For purposes of examplification the original run was truncated to the first 10 MS/MS spectra.
```
        "inputFiles": [
          {
            "location": "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2014/09/PXD000966/CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09.raw",
            "name": "CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09.trfr.t3.mzML",
            "fileFormat": {
              "accession": "MS:1000584",
              "name": "mzML format"
            },
```
The metric gauges each considered spectra's TIC in relation to the spectra's peak intensities. 
It does so by calculating the (minimal) fraction of peaks neccessary to sum up to half the total intensity of the spectrum itself.
Thus, the metric value will range between 0 and 1, where values closer to 0 will indicate spectra which' TIC is dominated by a few high intensity peaks.
```
        "qualityMetrics": [
        {
          "accession": "MS:4000068",
          "name": "spectra half-TIC",
          "value": {
```
The values for this metric are recorded in a table value type and consist of a column for the spectrum reference and the fractional value ("UO:0000191").
The spectrum reference is defined by the metric as either the NativeID and/or preferrably the USI in a separate column. 
The latter two columns are optional, however at least one has to be present. In our case, as the originating MS-run is available via proteomexchange, and the USI is a more detailed version of NativeID, no NativeID column is given.
```
            "MS:1003063": [
              "mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:2","mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:7","mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:29","mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:31","mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:34","mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:43","mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:45","mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:48","mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:50","mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:51"
            ],
            "UO:0000191": [
              0.1134,0.1628,0.0536,0.102,0.1042,0.0947,0.0784,0.1239,0.2593,0.1214
            ]
          }
        }
      ],
```
As you can see from the values in the fractional value column, 
most of the first ten spectra cluster around a value of about 10% of the peaks dominating the respective spectras' TIC, 
with only a few outliers to the 25% and the 5% range.
Each row represents one spectrum that can be directly looked up, in the case of using USI for spectra reference, 
[even directly from the web](https://www.proteomicsdb.org/use/?usi=mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:2).

### This is the mzQC file once again, in full:
**[USI-example.mzQC](https://github.com/HUPO-PSI/mzQC/tree/main/specification_documents/draft_v1/examples/USI-example.mzQC)**
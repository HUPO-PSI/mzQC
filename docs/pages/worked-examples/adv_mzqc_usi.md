---
layout: page
title: "Integration of the Universal Spectrum Identifier (USI) in mzQC"
permalink: /examples/adv_mzqc_usi/
---

The mzQC format supports various QC metrics that can operate at the level of MS runs or individual spectra.
One of the powerful features of mzQC is its compatibility with the [Universal Spectrum Identifier (USI)](https://www.psidev.info/usi), also developed by the Proteomics Standards Initiative.
This compatibility allows mzQC to reference individual spectra explicitly and precisely within a larger dataset.

## Example: Computing the "spectra half-TIC" metric using USI

In this example, we demonstrate the calculation of the "spectra half-TIC" metric for multiple MS/MS spectra.
The "spectra half-TIC" metric measures the minimal number of the most intense peaks needed to achieve half of the total ion current (TIC) of a spectrum.
This metric helps in understanding the peak intensity distribution within a spectrum, where a lower value indicates a concentration of intensity in fewer peaks.

For this example, the calculation is limited to the first 10 MS/MS spectra.
The results are formatted as a tabular metric where one column lists the USIs of the spectra and the other the computed fractional TIC values.
This example emphasizes the utility of USIs for directly linking QC metrics to specific spectra in public databases like ProteomeXchange.

The JSON representation of the quality metric in the mzQC format includes:

```json
"qualityMetrics": [
  {
    "accession": "MS:4000068",
    "name": "spectra half-TIC",
    "description": "The minimal proportion of peaks needed to account for at least 50% of the total ion current in each individual spectrum considered, recorded in a mandatory fraction column. Either USI or native spectrum identifier columns must be present as well.",
    "value": {
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
        0.1020,
        0.1042,
        0.0947,
        0.0784,
        0.1239,
        0.2593,
        0.1214
      ]
    }
  }
]
```

The table pairs each spectrum's USI with its corresponding "spectra half-TIC" value.
This format enables clear, unambiguous links between the QC data and the specific spectra, facilitating straightforward validation and further analysis.
Spectrum references use USIs which provide a robust method to trace back to the exact source data in public repositories, enhancing transparency and reproducibility in proteomic research.

Each spectrum and its TIC contribution can be directly accessed and verified online, ensuring that researchers can easily validate and reproduce findings.
For instance, the spectrum at USI [`mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:2`](https://www.ebi.ac.uk/pride/archive/usi?usi=mzspec:PXD000966:CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09:scan:2) can be directly resolved and viewed on PRIDE.
Additionally, the full mzQC file is available [here](https://github.com/HUPO-PSI/mzQC/tree/main/specification_documents/examples/adv_mzqc_usi.mzQC).

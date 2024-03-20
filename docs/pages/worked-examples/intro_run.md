---
layout: page
title: "Introduction to mzQC – Single Mass Spectrometry Run"
permalink: /examples/intro_run/
---

This introduction focuses on how mzQC can be used to detail QC information for individual mass spectrometry experiments, also known as "runs."
For example, a run may represent an untargeted LC-MS experiment with numerous MS/MS scans, a DIA experiment that quantifies thousands of peptides, or an SRM experiment that measures specific transitions.
Additionally, a run may also represent a mass spectrometry experiment when liquid chromatography is not directly coupled, such as spectra resulting from a plate of MALDI-TOF data or from a GC-MS experiment.

Here, we'll walk through the key components of an mzQC file, which uses a JSON-based format.
You can explore the complete mzQC file [here](https://github.com/HUPO-PSI/mzQC/tree/main/specification_documents/examples/intro_run.mzQC), to see all of the elements in their context.

An mzQC file starts with the root element `mzQC`:

```
{
  "mzQC": {
    ...
  }
}
```

Within `mzQC`, there are three main sections:

1. **General file information:** These attributes provide essential details about the mzQC file itself.

```
"version": "1.0.0",
"creationDate": "2020-12-01T11:56:34Z",
"contactName": "Mathias Walzer",
"contactAddress": "walzer@ebi.ac.uk",
"description": "A simple mzQC file containing information for a single mass spectrometry run.",
```

2. **Controlled vocabulary (CV) references:** This section points to standardized vocabularies used to ensure consistent metric definitions across files.
It is typically included at the end of the mzQC file.

```
"controlledVocabularies": [
  {
    "name": "Proteomics Standards Initiative Mass Spectrometry Ontology",
    "uri": "https://github.com/HUPO-PSI/psi-ms-CV/releases/download/v4.1.130/psi-ms.obo",
    "version": "4.1.130"
  }
]
```

3. **Quality metrics for the run:** This core part of the file captures the QC metrics specific to the run being described.

```
"runQualities": [
  {
    ...
  }
]
```

In the `runQualities` section, you may find multiple `runQuality` elements, each corresponding to a unique mass spectrometry run.
For simplicity, this example only includes a single run in the mzQC file.
First, this includes a `metadata` part detailing the run specifics, such as the source files and software used in analysis:

```
"metadata": {
  "inputFiles": [
    ...
  ],
  "analysisSoftware": [
    ...
  ]
},
```

Digging a bit deeper, for example, the `inputFiles` array describes each file contributing to the run, including details like file name, location (URI), format, and properties—all standardized using CV terms.

```
"inputFiles": [
  {
    "name": "CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09.mzML",
    "location": "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2014/09/PXD000966/CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09.mzML.gz",
    "fileFormat": {
      "accession": "MS:1000584",
      "name": "mzML format"
    },
    "fileProperties": [
      {
        "accession": "MS:1000747",
        "name": "completion time",
        "value": "2012-02-03 11:00:41"
      },
      {
        "accession": "MS:1003151",
        "name": "SHA-256",
        "value": "82ff4545ab8ab85252a4c5bc2c62abbfd04021ef5fefce145386bf27ae663a0f"
      },
      {
        "accession": "MS:1000031",
        "name": "instrument model",
        "value": "LTQ Orbitrap Velos"
      }
    ]
  }
],
```

Finally, the `qualityMetrics` array lists the metrics derived from the run, each defined clearly by CV terms to ensure clarity and consistency.
Metrics can take various forms, such as single values, tuples (arrays of values), or more complex structures like matrices or tables, depending on the information being conveyed.

For example, a single valued metric:

```
{
  "accession": "MS:4000059",
  "name": "number of MS1 spectra",
  "description": "The number of MS1 events in the run.",
  "value": 5074,
  "unit": {
    "accession": "UO:0000189",
    "name": "count unit"
  }
},
```

And a tuple metric:

```
{
  "accession": "MS:4000069",
  "name": "m/z acquisition range",
  "description": "Upper and lower limit of m/z precursor values at which MSn spectra are recorded.",
  "value": [
    300.1573,
    1778.8639
  ],
  "unit": {
    "accession": "MS:1000040",
    "name": "m/z"
  }
},
```

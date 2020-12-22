
## Single-Run Example of mzQC
Here, we describe an mzQC JSON document used for QC of a **single mass spectrometry** run.
mzQC can store information for multiple independent runs, which would be an easy extension of this example and is briefly described below.
To store QC information which is derived by looking at **sets** of runs (i.e. information is not attributable to a single run), please refer to the `multi-run.mzQC` example.

Find the complete example file at the bottom of this document or in the example folder.

The documents main anchor is between the outer curly brackets:
```
{ "mzQC":
  {
    ...
  }
}
```

Within this main anchor, there are usually the following sections:
a) general information about the file,
```
    "version": "1.0.0",
    "creationDate": "2020-12-01T11:56:34",
    "contactName": "Mathias Walzer",
    "contactAddress": "walzer@ebi.ac.uk",
    "description": "A simple mzQC file containing information for a single run.",
```

b) reference information for controlled vocabularies (cv) at the bottom, 
```
    "controlledVocabularies": [
      {
        "name": "Proteomics Standards Initiative Quality Control Ontology",
        "uri": "https://github.com/HUPO-PSI/qcML-development/blob/master/cv/v0_1_0/qc-cv.obo",
        "version": "0.1.0"
      },
      {
        "name": "Proteomics Standards Initiative Mass Spectrometry Ontology",
        "uri": "https://github.com/HUPO-PSI/psi-ms-CV/blob/master/psi-ms.obo",
        "version": "4.1.7"
      }
    ]
```
and
c) most importantly information about the metric values computed for a particular run.
```
    "runQualities": [
      {
        ...
      }
    ]
```
In fact, `runQualities` can contain one or more `runQuality` objects (one for each run). Each `runQuality` object is an element of a JSON array, thus it is not explicitly named (i.e. there is no "runQuality" key in the mzQC file).
A different object `setQualities` may hold the QC information for groups of runs (shown in a different example).
For the purpose of this example, we will just use one `runQuality`.
A `runQuality` reflects all QC data we have to a particular run (as `qualityMetric` objects), independent of other runs. It also contains `metadata` (about the run, input files, the software used). 
```
      {
        "metadata": {
          "inputFiles": 
            ...
        },
        "qualityMetrics": [
            ...
        ]
      }
```
The `inputFiles` consist of a single object, describing the source file with structured information about the file's name, format, location and other properties, defined via cv terms. 
```
          "inputFiles": [
            {
              "name": "CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09.trfr.t3.mzML",
              "location": "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2014/09/PXD000966/CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09.raw",
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
                  "accession": "MS:1000569",
                  "name": "SHA-256",
                  "value": "82ff4545ab8ab85252a4c5bc2c62abbfd04021ef5fefce145386bf27ae663a0f"
                },
                {
                  "accession": "MS:1000031",
                  "name": "instrument model",
                  "value": "LTQ Orbitrap Velos"
                }
              ]
```
As you can see, the location can not only be a filesystem location, but also a URL as you would get as part of a dataset submission to ProteomeXchange. Different meta information can be included, too, like on which `instrument model` the run was acquired on, or the `completion time` of the run.

This example will now show several simple metrics included in `qualityMetrics`, which contain the actual QC information for a particular `runQuality`. The `accession` and the corresponding `name` are defined by the QC CV (see `qc-cv.obo`) and should be represented exactly as stated in the .obo file. The `value` carries the actual information.
Metric values can be either single values,
```
            "accession": "QC:4000059",
            "name": "Number of MS1 spectra",
            "value": 5074
```
tuple of values,
```
            "accession": "QC:4000138",
            "name": "MZ acquisition range",
            "value": [ 300.157287597656, 1778.8639 ]
```
or matrices or tables (shown in other examples). 

### This is the mzQC file once again, in full:
```
{ "mzQC": {
    "version": "1.0.0",
    "creationDate": "2020-12-01T11:56:34",
    "contactName": "Mathias Walzer",
    "contactAddress": "walzer@ebi.ac.uk",
    "description": "A simple mzQC file containing information for a single run.",
    "runQualities": [
      {
        "metadata": {
          "inputFiles": [
            {
              "name": "CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09.trfr.t3.mzML",
              "location": "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2014/09/PXD000966/CPTAC_CompRef_00_iTRAQ_01_2Feb12_Cougar_11-10-09.raw",
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
                  "accession": "MS:1000569",
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
          "analysisSoftware": [
            {
              "accession": "MS:1001058",
              "name": "quality estimation by manual validation",
              "version": "0",
              "uri": "https://dx.doi.org/10.1021/pr201071t"
            },
            {
              "accession": "QC:0000000",
              "name": "QCCalculator",
              "version": "0.9.0",
              "uri": "qccalculator.readthedocs.io"
            }
          ]
        },
        "qualityMetrics": [
          {
            "accession": "QC:4000059",
            "name": "Number of MS1 spectra",
            "value": 5074
          },
          {
            "accession": "QC:4000060",
            "name": "Number of MS2 spectra",
            "value": 14812
          },
          {
            "accession": "QC:4000135",
            "name": "Number of chromatograms",
            "value": 1
          },
          {
            "accession": "QC:4000138",
            "name": "MZ acquisition range",
            "value": [ 300.157287597656, 1778.8639 ]
          },
          {
            "accession": "QC:4000139",
            "name": "RT acquisition range",
            "value": [ 0.2959, 5969.8172 ]
          }
        ]
      }
    ],
    "controlledVocabularies": [
      {
        "name": "Proteomics Standards Initiative Quality Control Ontology",
        "uri": "https://github.com/HUPO-PSI/qcML-development/blob/master/cv/v0_1_0/qc-cv.obo",
        "version": "0.1.0"
      },
      {
        "name": "Proteomics Standards Initiative Mass Spectrometry Ontology",
        "uri": "https://github.com/HUPO-PSI/psi-ms-CV/blob/master/psi-ms.obo",
        "version": "4.1.7"
      }
    ]
  }
}
```

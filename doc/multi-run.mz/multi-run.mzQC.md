## Multi-Run Example of mzQC
Here, we describe a mzQC JSON document used for QC of multiple mass spectrometry runs. 
Find the complete file at the bottom of this document or in the example folder.
The file has the same basic structure as a single run mzQC, a description of the specific set conditions will help later use/revisit:
```
    "creationDate": "2020-12-01T14:19:09",
    "contactName": "Chris Bielow, Mathias Walzer",
    "contactAddress":  "inspect.qc@no.reply.com",
    "version": "1.0.0",
    "description": "A multi-run example, where sets of runs are grouped into setQualities according to the experimental design. 
        Each setQuality has a label annotation, that must be unique. The label also lends itself as input source to axis labels 
        if you need to plot a figure from multiple setQualities. If you want to specifiy an upper level of hierarchy (summarizing 
        dimensions), then add a describing cvParameter in metadata. E.g. you have a sets, one set describes a group at a specific 
        timepoint."
```

The runQualities of the individual runs can be included, especially if the setQuality metrics interpretation depend on knowledge of runMetric values of the individual runs.
The setQualities element works just as the runQualities element works by registering elements of setQuality in its array.
Each setQuality describes any number of metrics for a distinct set of runs. 
All metrics must describe properites applicable to all runs in the set, listed in the setQuality inputFiles, here mzML files of a series of three:
```
          "inputFiles": [
            {
              "location": "/tmp/series-1.mzML",
              "name": "series-1.mzML",
              "fileFormat": {
                "accession": "MS:1000584",
                "name": "mzML format"
              }
            },
            {
              "location": "/tmp/series-2.mzML",
              "name": "series-2.mzML",
              "fileFormat": {
                "accession": "MS:1000584",
                "name": "mzML format"
              }
            },
            {
              "location": "/tmp/series-3.mzML",
              "name": "series-3.mzML",
              "fileFormat": {
                "accession": "MS:1000584",
                "name": "mzML format"
              }
            }
          ]
```
For further reference, the set should also feature a label. 
This becomes handy e.g. when dealing with discrete time points in time series of separate groups.
The labels must be unique within the file.
```
    "setQualities": [
      {
        "metadata": {
          "label": "groupA_timepoint1",
```
In case you want to specifiy summarising dimensions of multiple sets or have a complex grouping, add cvParameter(s) here that describes the respective dimension for better machine interpretability (and visualisation).
```
          "cvParameters": [
            {
              "accession": "NCIT:C25523",
              "name": "Grouping",
              "value": "group A"
            },
            {
              "accession": "NCIT:C83158",
              "name": "Laboratory Test Time Point",
              "value": "timepoint 1"
            }
```
Then, the chosen metrics can be reflected as before:
```
        "qualityMetrics": [
          {
            "accession": "QC:4000167",
            "name": "Precursor intensity distribution Q1, Q2, Q3",
            "value": [ 1079.667, 5000.2, 15022.9 ]
          },
          {
            "accession": "QC:4000168",
            "name": "Precursor intensity distribution mean",
            "value": 4999.9
          },
          {
            "accession": "QC:4000169",
            "name": "Precursor intensity distribution sigma",
            "value": 800.9
          },
          {
            "accession": "QC:4000170",
            "name": "Precursor intensity distribution low outliers (<Q1-1.5*IQR)",
            "value": [ 1.3, 2.1 ]
          },
          {
            "accession": "QC:4000171",
            "name": "Precursor intensity distribution high outliers (>Q3+1.5*IQR)",
            "value": [ 18001.1, 21323.99 ]
          }
        ]
      }
    ],
```

### This is the mzQC file once again, in full:
```
{
  "mzQC": {
    "creationDate": "2020-12-01T14:19:09",
    "contactName": "Chris Bielow, Mathias Walzer",
    "contactAddress":  "inspect.qc@no.reply.com",
    "version": "1.0.0",
    "description": "A multi-run example, where sets of runs are grouped into setQualities according to the experimental design. 
        Each setQuality has a label annotation, that must be unique. The label also lends itself as input source to axis labels 
        if you need to plot a figure from multiple setQualities. If you want to specifiy an upper level of hierarchy (summarizing 
        dimensions), then add a describing cvParameter in metadata. E.g. you have a sets, one set describes a group at a specific 
        timepoint."
    "setQualities": [
      { "metadata": {
          "label": "groupA_timepoint1",
          "inputFiles": [
            {
              "location": "/tmp/series-1.mzML",
              "name": "series-1.mzML",
              "fileFormat": {
                "accession": "MS:1000584",
                "name": "mzML format"
              }
            },
            {
              "location": "/tmp/series-2.mzML",
              "name": "series-2.mzML",
              "fileFormat": {
                "accession": "MS:1000584",
                "name": "mzML format"
              }
            },
            {
              "location": "/tmp/series-3.mzML",
              "name": "series-3.mzML",
              "fileFormat": {
                "accession": "MS:1000584",
                "name": "mzML format"
              }
            }
          ],
          "analysisSoftware": [
            {
              "accession": "MS:1001058",
              "name": "quality estimation by manual validation",
              "version": "0",
              "uri": "https://dx.doi.org/10.1021/pr201071t"
            }
          ]
        },
        "qualityMetrics": [
          {
            "accession": "QC:4000167",
            "name": "Precursor intensity distribution Q1, Q2, Q3",
            "value": [ 1079.667, 5000.2, 15022.9 ]
          },
          {
            "accession": "QC:4000168",
            "name": "Precursor intensity distribution mean",
            "value": 4999.9
          },
          {
            "accession": "QC:4000169",
            "name": "Precursor intensity distribution sigma",
            "value": 800.9
          },
          {
            "accession": "QC:4000170",
            "name": "Precursor intensity distribution low outliers (<Q1-1.5*IQR)",
            "value": [ 1.3, 2.1 ]
          },
          {
            "accession": "QC:4000171",
            "name": "Precursor intensity distribution high outliers (>Q3+1.5*IQR)",
            "value": [ 18001.1, 21323.99 ]
          }
        ]
      }
    "controlledVocabularies": [
      {
        "name": "Proteomics Standards Initiative Quality Control Ontology",
        "uri": "https://github.com/HUPO-PSI/qcML-development/blob/master/cv/v0_1_0/qc-cv.obo",
        "version": "0.1.0"
      },
      {
        "name": "NCI Thesaurus OBO Edition",
        "uri": "http://purl.obolibrary.org/obo/ncit/releases/2021-05-25/ncit.owl",
        "version": "21.05d"
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

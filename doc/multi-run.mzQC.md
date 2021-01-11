## Multi-Run (i.e. sets) Example of mzQC
Here, we describe an mzQC JSON document used to convey QC data which is computed on a set of runs, i.e.
is **only interpretable in the context of this set** (group).
Of course, QC metrics which refer to each run individually can also be stored, also in the same mzQC file
(see our example single-run.mzQC.md on how to do that), but this example is about group/set metrics.

Find the complete example file at the bottom of this document or in the example folder.

The basic structure of our mzQC file is identical to the `single-run.mzQC` example, i.e.
the documents main anchor is between the outer curly brackets:
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
    "creationDate": "2020-12-21T11:56:34",
    "contactName": "Chris Bielow",
    "contactAddress": "chris.bielow@bsc.fu-berlin.de",
    "description": "A simple mzQC file containing information for sets of runs.",
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
and (now in addition or as replacement) to the `runQualities` of the `single-run.mzQC` we have
c) information about the QC metrics computed on **a set of runs**.
```
    "setQualities": [
      {
        ...
      }
    ]
```
In fact, `setQualities` can contain one or more `setQuality` objects, each defining a different set of runs.
E.g. if you have three technical replicates for two conditions, you might want to subsume three runs into a set, one for each condition and report the total number of proteins you identified, or the percentage of total intensity attributable to contaminants). Each `setQuality` object is an element of a JSON array, thus it is not explicitly named (i.e. there is no "setQuality" key in the mzQC file).
A different `runQualities` object may hold QC information about the individual runs (shown in the `single-run.mzQC` example).
For the purpose of this example, we will just use two `setQuality` objects (there could be none, only one or more than two though). How you define (and name) each set, is up to you and depends on your experimental design.
A `setQuality` represents QC data that must be viewed in the context of all the runs of this set/group. I.e. the data is only valid within the context of the runs it comprises. E.g. it would be invalid to define a set of three runs and report their individual MS1 scan counts as a 3-tuple -- because this information can clearly be attributed to individual runs.
Similar to `runQuality`, a `setQuality` also contains `metadata` about the set of runs (its input file**s**, the software used). 
You can give the set a unique name using the `label` attribute. Here is how a `setQuality` object looks like:
```
      {
        "metadata": {
          "label": "TechRepl:1,2,3_healthy"
          "inputFiles": 
            ...
        },
        "qualityMetrics": [
            ...
        ]
      }
```
The `inputFiles` consist of an array of `inputFile` objects, describing the source files with structured information about the file's name, format, location and other properties, defined via cv terms. 
```
          "inputFiles": [
            {
              "name": "techRep1_healthy",
              "location": "c:\msdata\techRep1_healthy.raw",
              ...
            },
            {
              "name": "techRep2_healthy",
              "location": "c:\msdata\techRep2_healthy.raw",
              ...
            },
            {
              "name": "techRep3_healthy",
              "location": "c:\msdata\techRep3_healthy.raw",
              ...
            }
          ]
```
The `inputFile` object is only sketched here. It can contain a lot more information, such as file format and further properties. See the full example below or `single-run.mzQC` for details.

In  `qualityMetrics`, we will store the actual QC information for a particular `setQuality`. Each `qualityMetric` has an `accession` and the corresponding `name` are defined by the QC CV (see `qc-cv.obo`) and should be represented exactly as stated in the .obo file. The `value` carries the actual information.
Metric `value`s can be either single values, tuple of values, or matrices or tables (shown in other examples). 

Here we show two metrics: the first describes the relative total intensity of all contaminant proteins (from all runs in the set) -- the higher the value the more contaminants are present in the samples of the set.
```
            "accession": "QC:0000000",
            "name": "Protein contaminant intensity ratio",
            "value": 0.25
```
... and the second metric is a single column of a PCA result matrix. This metric is a bit special because it only partially describes the data.
This data is part of a superset (a.k.a. set of sets). Let's see what the full data would look like:
![PCA results based on a table where each row is a proteingroup, and each column represents a set of Rawfiles(runs). Each data point in the plot represents one set, e.g. `TechRepl:1,2,3_diseased` or `TechRepl:1,2,3_healthy`.](figures/MultiSet_PCA.png)
But let's see the mzQC data first: The metric for this set stores its first 5 principal components (PC):
```
            "accession": "QC:0000000",
            "name": "PrincipalComponents5_RawProteinGroupIntensity",
            "value": [ 47.22, 29.1, 3.8, -7.7, 140.6 ]
```
Now, these values are meaningless unless we know the PC's for other sets to puzzle together the PCA plot above (this is how the PCA was done in the first place: from a table, where each column represents a set of Raw files (e.g. subsumed technical replicates), and each row is a proteingroup; you would find this data, for example, in MaxQuant's proteinGroups.txt). To make sure we can identify all sets which belong to this 'superset' for our PCA result, we annotate the `metadata` section with a CV term. All sets which have the same term (and value!), contribute one row of our PCA result matrix.
```
  "metadata" : {
    ...,
    "cvParameters": [
      {
        "accession": "QC:0000000",
        "name": "superset-label",
        "value": "MaxQuant experiment groups"
      }
    ]
  }
```
In other words: if you need to represent some kind of hierarchy of QC information (supersets), maybe due to your experimental design, `setQuality`'s are always the leaf nodes in that tree. To describe data for inner nodes (supersets), annotate the sets in the leaf nodes with a CV term. This allows to reconstruct this hierarchy.


### This is the mzQC file once again, in full:
```
{
  "mzQC": {
    "version": "1.0.0",
    "creationDate": "2020-12-01T14:19:09",
    "contactName": "Chris Bielow",
    "contactAddress": "chris.bielow@bsc.fu-berlin.de",
    "description": "A simple mzQC file containing information for sets of runs.",
    "setQualities": [
      {
        "metadata": {
          "label": "TechRepl:1,2,3_healthy",
          "inputFiles": [
            {
              "name": "techRep1_healthy",
              "location": "c:\\msdata\\techRep1_healthy.raw",
              "fileFormat": {
                "accession": "MS:1000584",
                "name": "mzML format"
              },
              "fileProperties": [
                {
                  "accession": "MS:1000747",
                  "name": "completion time",
                  "value": "2012-02-03 11:00:41"
                }
              ]
            },
            {
              "name": "techRep2_healthy",
              "location": "c:\\msdata\\techRep2_healthy.raw",
              "fileFormat": {
                "accession": "MS:1000584",
                "name": "mzML format"
              },
              "fileProperties": [
                {
                  "accession": "MS:1000747",
                  "name": "completion time",
                  "value": "2012-02-03 13:00:41"
                }
              ]
            },
            {
              "name": "techRep3_healthy",
              "location": "c:\\msdata\\techRep3_healthy.raw",
              "fileFormat": {
                "accession": "MS:1000584",
                "name": "mzML format"
              },
              "fileProperties": [
                {
                  "accession": "MS:1000747",
                  "name": "completion time",
                  "value": "2012-02-03 14:00:41"
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
            }
          ],
          "cvParameters": [
            {
              "accession": "QC:0000000",
              "name": "superset-label",
              "value": "MaxQuant experiment groups"
            }
          ]
        },
        "qualityMetrics": [
          {
            "accession": "QC:0000000",
            "name": "Protein contaminant intensity ratio",
            "value": 0.25
          },
          {
            "accession": "QC:0000000",
            "name": "PrincipalComponents5_RawProteinGroupIntensity",
            "value": [ 47.22, 29.1, 3.8, -7.7, 140.6 ]
          }
        ]
      },
      
      {
        "metadata": {
          "label": "TechRepl:1,2,3_diseased",
          "inputFiles": [
            {
              "name": "techRep1_diseased",
              "location": "c:\\msdata\\techRep1_diseased.raw",
              "fileFormat": {
                "accession": "MS:1000584",
                "name": "mzML format"
              },
              "fileProperties": [
                {
                  "accession": "MS:1000747",
                  "name": "completion time",
                  "value": "2012-02-03 12:00:41"
                }
              ]
            },
            {
              "name": "techRep2_diseased",
              "location": "c:\\msdata\\techRep2_diseased.raw",
              "fileFormat": {
                "accession": "MS:1000584",
                "name": "mzML format"
              },
              "fileProperties": [
                {
                  "accession": "MS:1000747",
                  "name": "completion time",
                  "value": "2012-02-03 14:00:41"
                }
              ]
            },
            {
              "name": "techRep3_diseased",
              "location": "c:\\msdata\\techRep3_diseased.raw",
              "fileFormat": {
                "accession": "MS:1000584",
                "name": "mzML format"
              },
              "fileProperties": [
                {
                  "accession": "MS:1000747",
                  "name": "completion time",
                  "value": "2012-02-03 15:00:41"
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
            }
          ],
          "cvParameters": [
            {
              "accession": "QC:0000000",
              "name": "superset-label",
              "value": "MaxQuant experiment groups"
            }
          ]
        },
        "qualityMetrics": [
          {
            "accession": "QC:0000000",
            "name": "Protein contaminant intensity ratio",
            "value": 0.31
          },
          {
            "accession": "QC:0000000",
            "name": "PrincipalComponents5_RawProteinGroupIntensity",
            "value": [ -30.22, -36.5, -7.3, 5.55, -64.1 ]
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

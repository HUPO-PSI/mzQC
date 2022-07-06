---
layout: page
title: "mzQC format for analytical chemists"
permalink: /use-cases/analytical-chemists/
---

The Proteomics Standards Initiative of the Human Proteomics Organization (HUPO-PSI) has developed the mzQC format to simplify communicating quality control metrics for biological mass spectrometry experiments.  HUPO-PSI wants it to be easy to generate quality metrics from proteomics and metabolomics data sets and easy to read and interpret these values.  mzQC is different from other HUPO-PSI standards in that it employs “JSON” (JavaScript Object Notation) rather than XML (as in mzML or mzIdentML) or tab-delimited text (as in mzTab).  JSON is in widespread use for communicating data among web applications and other network services.

## Decide on a set of metrics
While many of the papers describing QC metrics for mass spectrometry have been built around “shotgun” proteomics experiments, metrics can be defined for any biological mass spectrometry application.  In this case, we will use data from PXD006843, a GeLC-MS shotgun examination of Mycobacterium tuberculosis proteomes.  We might start with the mzML file for experiment H2-1-1 (an arbitrary choice).  In this case, we might ask the following questions about the mzML file:
1. How long did this experiment take on the instrument?
    _7199.34 seconds_
2. How many MS scans were generated in this experiment?
    _8279 MS scans_
3. How many MS/MS scans were generated in this experiment?
    _7255 MS/MS scans_
4. What fraction of MS/MS scans came from +2 precursor ions?
    _63.67%_

Naturally, it’s much easier if you use software to produce these values.  In this case, I am using values reported by the QuaMeter software[1] in “IDFree” mode.


## Format metrics in JSON
For each of the metrics we defined in the prior section, we note that there’s an entity (the mzML in question), an _attribute_ (the question we’re answering), a _value_ (the number answering the question), and a _unit_ (the type of thing represented by the value).  For this section, we will concern ourselves only with attributes, values, and units.  The following bloc expresses the answers from the first two questions in the previous section:

```
"qualityMetrics": [
    {
        "id": "RT-Duration",
        "cvRef": "QC",
        "accession": "QC:4000053",
        "name": "Quameter metric: RT-Duration",
        "unit": {
            "cvRef": "UO",
            "accession": "UO:0000010",
            "name": "second"
        },
        "value": 7199.34
    },
    {
        "id": "MS1-Count",
        "cvRef": "QC",
        "accession": "QC:4000059",
        "name": "Quameter metric: MS1-Count",
        "unit": {
            "cvRef": "UO",
            "accession": "UO:0000189",
            "name": "count"
        },
        "value": 8279
    }
]
```

In essence, we have a **list** of two _qualityMetrics_ (started and terminated by square brackets).  Each of the curly braces inside that list enclose an **object**; JSON does not require us to specify how many objects appear on a list in advance, so we could have continued to append more _qualityMetrics_ until we were satisfied.  The pieces within the object are called **key / value pairs**.  In the case of “unit,” the value is a unit object **nested** inside the _qualityMetric_ object.


It’s important that each of the attributes (metrics) we compute for an entity references the **controlled vocabulary** (“CV”) for mzQC.  We don’t just create metrics out of the blue; metrics should be described in the CV before they are used in mzQC files.  Each type of metric gets an accession within the CV to help people interpret these values from a given mzQC.  This greatly improves the interpretability of mzQC outputs over a text table that bears only a couple words of a caption for each column.


## Relate these data to external resources
We anticipate that each mzQC supplies quality metrics for one or more mass spectrometry experiments.  It’s obviously important that the mass spectrometry data files from which the metrics were computed be specified.  In mzQC, this description comes at the top of the file in a section labeled “InputFiles.”  Computing metrics from raw data may differ from the same metrics from an mzML file (for example, the latter is frequently centroided to peak lists rather than retaining peak profiles).  As a result, the mzQC needs to describe the file format in a "FileFormat" object.  Since a variety of mzML files may be produced from a raw file, mzQC files are also expected to report a “hash” for the input files, such as an MD5 or SHA1 value for the input file.  Altogether, this description has this appearance:

```
"InputFiles": [
    {
        "RawFile": {
            "id": "rawfile001",
            "location": "file://c:/Research/20171124-Lizex-Chia/1091_Pool_start.mzML",
            "FileFormat": {
                "cvRef": "MS",
                "accession": "MS:1000584",
                "name": "mzML format"
            },
            "FileProperties": [
                {
                    "cvRef": "MS",
                    "accession": "MS:1000568",
                    "name": "MD5",
                    "value": "b583f6d2a91b4749d5a75885330f6e5d"
                },
                {
                    "cvRef": "MS",
                    "accession": "MS:1000747",
                    "name": "completion time",
                    "value": "2017-12-08-T15:38:57Z"
                }
            ]
        }
    }
]
```

In our brief snippet of JSON from the previous section, we saw references to terms defined in two different controlled vocabularies, “QC” and “UO.”  We would expect most mzQC files to make reference to the “MS” controlled vocabulary, as well.  The mzQC file needs to explain what these abbreviations represent.  The final part of the mzQC file offers pointers to the URLs where these controlled vocabularies can be found as well as the version numbers to which these references were made: 

```
"controlledVocabularies": [
    {
        "id": "QC",
        "name": "Proteomics Standards Initiative Quality Control Ontology",
        "version": "0.0.11",
        "uri": "https://github.com/HUPO-PSI/qcML-development/blob/master/cv/v0_0_11/qc-cv.obo"
    },
    {
        "id": "MS",
        "name": "Proteomics Standards Initiative Mass Spectrometry Ontology",
        "version": "4.1.7",
        "uri": "https://github.com/HUPO-PSI/psi-ms-CV/blob/master/psi-ms.obo"
    },
    {
        "id": "UO",
        "name": "Unit Ontology",
        "version": "09:04:2014 13:37",
        "uri": "https://github.com/bio-ontology-research-group/unit-ontology/blob/master/unit.obo"
    }
]
```

## Conclusion
Writing an mzQC file means familiarizing yourself with terms defined in controlled vocabularies such as the PSI Mass Spectrometry, PSI Quality Control, and EBI Unit Ontologies.  These terms will be useful for determining the meaning of the values you report in mzQC.  If you have created software to compute quality metrics from MS data, you probably have a clear notion in your mind of what the metrics mean; by discerning which terms from these controlled vocabularies are descriptive of your metrics, you will make it much easier for others to interpret values from your software.  Unless you are computing only metrics that have been previously defined for other software, you will probably need to register metric descriptions with the keeper of the PSI Quality Control controlled vocabulary so that you have an accession number for each new definition.


Choosing JSON rather than XML is intended to reduce the effort required to write and read mzQC format.  Almost every programming language offers functions or libraries to “serialize” a data structure in JSON format.  After some experience working with these files, we believe most developers will find these files relatively easy to read by eye as well as by software!


---
[1]: Bumbershoot from proteowizard.sourceforge.net.  X. Wang et al. Anal. Chem.. (2014) 86: 2497
Original draft: https://docs.google.com/document/d/16b1n_LXYWsxLK2PQfXWj_WvtiwJOXu2EZx1Q8WzZNlc/edit#

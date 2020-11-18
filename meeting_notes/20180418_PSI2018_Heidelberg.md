# HUPO-PSI Meeting Heidelberg 18-20 April 2018

## Session attendees

- Pierre-Alain Binz
- Wout Bittremieux
- Paul Brack
- Martin Eisenacher
- Reza Salek
- Dave Tabb
- Stefan Tenzer
- Julian Uszkoreit
- Mathias Walzer
- Weimin Zhu

---

## [Meeting agenda](https://docs.google.com/spreadsheets/d/e/2PACX-1vQhiu8x_FWXafUgWZ8o6o-bbmINuP8PlDnejJGe8DyagEB1TDLWuGgufM4g0aoqovRVo3r6kljJzpLJ/pub)

## qcML schema

Discussion of the current state of the qcML schema based on several handcrafted example files:

- Dave: QuaMeter ID-free
- Hugo Lopez Fernandez: Mass-Up
- Mathias: OpenMS
- Wout: iMonDB & outlier detection

Several issues and ambiguities were identified based on these example files.

### Metrics encoding

- Should we categorize metrics based on which part of the analytical chemistry they correspond to?
- Currently it is not straightforward to specify metrics tables with different units for each row.
    - Can we explicitly mention units and values for each column of the table?
- How can we represent multidimensional metrics?
    - For example, columns with different unit types: proteins - peptides - intensity - RT for depleted/non-depleted/spiked-in standards
- How do we specify multiple values for the same metric?
    - As a list of e.g. quartiles: `[1, 2, 3, 4]`
    - As a dictionary: `[{'q1': 1, 'q2': 2, 'q3': 3, 'q4': 4}]`
    - The dictionary might make misuse easier, for example by mixing parametric and non-parametric values.

### Units specification

- How can we link to CVs denoting the unit for specific metrics in the JSON strings? Currently the JSON strings only contain accession numbers for the metrics, but no explicit reference to the CV in which to retrieve that accession.
- We mainly use the [unit ontology](https://github.com/bio-ontology-research-group/unit-ontology) (UO) to specify units, but what if we need a unit that's not in there? Check whether a suitable unit is in the UO, e.g. log ratio is _not_ in the UO but ratio is, or support it in our own CV.

### Miscellaneous

- How can we refer uniquely to local source files? If the file is available in a repository we can derive a unique identifier from that, but not for local files.

### Use cases

We discussed different use cases qcML should support based on Paul's metrics for DIA experiments and Hugo's example for MALDI-TOF profiling.

## MIAPE-QC

Which metrics are important enough to be included in the MIAPE-QC? Who does the MIAPE-QC serve?

- Either it contains the minimum information to repeat the same experiment?
- Or it contains the minimum metrics that should be reported.

As other MIAPE specifications are not widely supported in the community we should keep the requirements for the MIAPE-QC minimal and only require a limited set of metrics to be reported rather than detailed information that would be needed for a full replication.
For these metrics we will provide a common definition (fixed CV-term, non-tool specific) so that these metrics are always reported the same way.
Additionally the CV should include a flag `is_miape_metric` to indicate that this metrics is required.

The current version of the MIAPE-QC presented by Weimin contains two sets of metrics:

1. Minimal metrics, easy to collect.
2. Wishlist of useful metrics, contains more details to reproduce the experiment.

Currently not all metrics included in the MIAPE-QC are universally applicable (e.g. the number of MS2 scans is not applicable if only MS1-level data is collected). We should ensure that the MIAPE-QC metrics are relevant for any type of biological mass spectrometry experiment, currently this is fixated too much on shotgun LC-MS/MS.

We should keep in mind that the MIAPE-QC specification is conceptual and is not necessarily directly linked to the qcML format. Furthermore, there is no need to duplicate previous MIAPEs.

### Metric suggestions

Important yet general information to include in the MIAPE-QC would be (sample) processing metadata:

- Temperate control (temperate range of the sample storage)
- Time between sample extraction and measurement
- Duration of the tryptic digestion
- Age of the LC column
- Whether carbamylation is caused by old urea
- Whether IAM introduced unwanted modifications
- ...

Wout's review from last year could be used as a starting point.

Bittremieux, W. et al. Quality control in mass spectrometry-based proteomics. Mass Spectrom. Rev. Early view, (2017). [doi:10.1002/mas.21544](http://onlinelibrary.wiley.com/doi/10.1002/mas.21544/abstract)

Focus on the QC process rather than on a description of the experiment. The aim of including information in the MIAPE-QC is to _educate_ people what could potentially go wrong.

## CV

How can we add new terms to the CV?

- Issue a pull request on Github with the changes you want to make. Julian will review your pull request.
- Or create an issue on Github describing the wanted changes. Julian will process your issue.

_DO NOT_ edit the CV directly on Github. Julian is the only person who should be making changes to the CV.

When can you request inclusion of a new metric into the CV? Currently we will use a flexible process as we are still in the startup phase.

- First check carefully if the metric is not in the CV yet.
- Otherwise follow the above procedure.

These instructions will also be mentioned on Github.

In the future, when we have a stable version, we will follow the CV procedure as officially delineated by the PSI.

- Send a request for a new CV to the mailing list.
- The request will be discussed in a small committee over a few (max. 5) days to ensure a quick turnover period.
- The new metric will be added by the ontology coordinator.

## qcML implementations

Which qcML implementations are there already at the moment and do we want to provide in the future? Both in repositories and in tools.

### In repositories

Currently public data repositories do not contain raw files for blank runs or QC runs, which are potential sources of valuable QC information! An important problem is that repositories do not have a mechanism to specify what type of run each file is.

Ideal future system: each project deposited to ProteomeXchange is automatically processed through a QC system.

What do we need to achieve this?

- Define a set of important metrics
    - General metrics as well as experiment-specific metrics
    - Including a comparison between multiple files, quality is not relevant for an individual file in isolation
- Provide implementations to compute these metrics

### In tools

Which tools will support qcML and what is their current status?

- QuaMeter NIST/ID-free/SWAMe (Dave): 90% clear on target, 0% implemented
- SWATHQC (Paul): 50% clear on target, 0% implemented
- OpenMS NIST (Mathias): 90% implemented
- iMonDB (Wout)
- KNIME MPC-QC (Julian)
- R LFQBench (Stefan)
- XCMS (Steffen Neuman, Reza)

Unavoidable: different tools will give different QC results, there is no single truth.

## Miscellaneous

### Group structure

Julian replaces Martin as ontology coordinator. This will need to be changed on the new HUPO-PSI website.

### Community outreach

- Suggestion by Stefan: It might be useful to prepare a manuscript showing why QC is relevant for proteomics research. For example, in clinical chemistry everyone finds it very obvious that you need QC while this is often not the case for proteomics research.
- Idea by Martin: Back up this viewpoint article by a large-scale reanalysis of PRIDE data to show that most uploaded data has problems. Do not name and shame specific people but rather show that the community deals with a problem in general.
- It might be useful for Jinmeng to take the lead in this based on the requirements to finish her PhD. Dave will closely follow up on this and the MIAPE-QC with Jinmeng and Weimin.

---
layout: page
title: "mzQC with multiple experiments"
permalink: /use-cases/mzqc-multi/
---

At first glance, it might seem that mzQC is intended to store quality metrics for a single LC-MS/MS experiment.  In fact, the format is designed to scale to store metrics for collections of many LC-MS/MS experiments.  For that matter, it is capable of experiments using altogether different types of separation or that lack tandem mass spectra!  This tutorial examines scenarios in which a single mzQC contains metrics from a group of experiments.


## Scenario 1: post-experiment quality check
Frequently, researchers receive a batch of raw data at a stroke.  For example, they may ship a few dozen samples to a core facility and receive a collection of Thermo RAW files or SCIEX WIFF/SCAN files in return.  Alternatively, they may read an interesting paper and download the corresponding files from ProteomeXchange.  Having marshalled the data on a lab workstation, they may begin their analysis by asking whether these files are of consistent quality.  The question is of real consequence, since cohort versus cohort comparisons are only likely to yield fruit if technical variation is considerably less than the biological difference being studied.


Software for quality metric generation can access the raw data, and it may also work with identification or quantitative results that were derived from the raw data.  It may treat each raw file independently, generating an mzQC to represent each on-line separation.  The metric generator reads 100 RAW files, and it emits 100 mzQCs.  The researcher, however, knows that these 100 files are not independent of each other but rather are to be evaluated as a set.  If the fraction of MS/MS scans identified confidently is considerably higher in cohort A than in cohort B, that difference will compromise differentiation.  If some of the experiments were so sample-limited that they produced far fewer MS/MS scans than the others, the researcher would like to have that information as early as possible.


In this case, each of the 100 experiments have resulted in a vector of quality metrics.  Dimensionality reduction techniques such as Principal Components Analysis (PCA) can handle correlations among these quality metrics to produce a relatively small number of uncorrelated components from a larger number of metrics.  Each experiment can then be regarded as a node in space, with its position specified by the PCA components.


The 100 mzQCs mentioned above are likely to go through two different processes in this workflow: aggregation and conjoint analysis.  mzQC files can store original metrics for a single RAW file, or they can store original metrics from a large collection of experiments.  The process of aggregation simply collects the metrics for many experiments in a single mzQC.  Instead of a single “run quality” object for a single experiment mzQC, an aggregated mzQC will have 100 “run quality” objects, each reporting the file name associated with a particularly experiment.  When multiple mzQCs have been aggregated, it becomes possible to store new metrics that are characteristic of the experiment collection.  In this case, the “set quality” object will store metrics for the group of experiments.  PCA coordinates are examples of these batch-wide quality metrics.


Two applications should be apparent from this visualization of the 100 experiments:
### 1A: Outlier Detection
If 99 of the experiments form a cloud in the center of the PCA plot and the 100th is far away on the perimeter of the plot, a researcher should consider the possibility that the 100th experiment is an outlier.  A variety of criteria have been proposed for suggesting outliers (such as “Tukey’s Fence,” based on interquartiles), but a researcher is likely to use all the information available to determine whether that experiment should be excluded from further analysis.  For example, if they recall that the sample was a very low concentration or was accompanied by an odd precipitate, their lab notebook notations along with the PCA of quality metrics may rule the data out of bounds.
### 1B: Cohort Effect and Batch Effect Detection
One of the most common designs for comparative proteomics involves the measurement of n replicates from cohort A and n replicates from cohort B.  Which proteins are changing most consistently between the two cohorts?  We expect that these two cohorts will show broadly similar expression of proteins, but a subset of the proteins is “up” between cohorts and another subset of proteins is “down” between cohorts.  Quality metrics based upon underlying mass spectrometry signals should not show large deviations from a relatively small proportion of protein changes.  As a result, one should expect that a PCA plot of the 100 experiments should have one cloud of all 100 rather than a cloud representing cohort A and a separate cloud of cohort B.


A batch effect can result when subsets of the experiments were conducted at different times.  A worst-case scenario is when all of the cohort A samples were analyzed at a different time period than all of the cohort B samples.  Mass spectrometers vary in performance as a function of time.  If a time difference separates cohort A and cohort B analysis, biological variation is conflated with technical variation (this is a worst-case design).  When multiple batches of samples are necessitated by the scale of a large study, it is always worthwhile to determine whether experiments run at different times remain comparable.  If experiments analyzed by the mass spectrometer on week one separate on the PCA plot from experiments analyzed during week two and from experiments analyzed during week three, the researcher is likely to need a statistical model in which the batch is reported for each experiment.
### Scenario 2: longitudinal assessment
Biological mass spectrometry is frequently employed in core facility settings.  For laboratories that need to certify the quality of a raw data “product,” demonstrating the stability of an instrument over time is a priority.  In this scenario, the researcher may have hundreds of analyses of a common sample for a given instrument, spanning months or years of time.  Each of these experiments can be individually assessed by a quality metric generator, producing an mzQC output.  These can be aggregated, as before, to produce a single mzQC that represents all the data.  This aggregate mzQC then empirically represents the long-term performance of the instrument.


A typical way to analyze these data produces a Hotelling T-squared metric that combines information among different metrics across the time span of the example data.  The T-squared value for an individual experiment can be converted to an F-statistic.  If the value rises beyond a threshold, the experiment can be ruled to represent an “out of control” state for the instrument.  The aggregate mzQC could then be annotated with the F-statistic derived for each of the experiment files.


Machine learning has been demonstrated to have greater flexibility in recognizing aberrant instrument performance.  A researcher can generally highlight many examples of reliable instrument performance.  Example data that demonstrate the effects of spray instability, column aging, or a dirty source may or may also be available.  A researcher can annotate which of these runs represent reliable instrument phases and which represent failing instrumentation. A supervised machine learning model, for example a random forest classifier, can then accept a new experiment data file and make its prediction whether that file represents good or bad performance.


---
Original draft: https://docs.google.com/document/d/1hnuQrwgH2hCeXGNBuoZAwOOVmxVWRxsIvqizMeLWsOA/edit#heading=h.3jt73ic7z3x1

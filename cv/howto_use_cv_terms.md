# CV Term Usage Guide

The translation from CV terms to elements in an mzQC file depends on the term's
value type and is pretty straightforward.

## Single Value

To report the number of MS1 scans in a peak file:

```
[Term]
id: MS:4000059
name: number of MS1 spectra
def: "The number of MS1 events in the run." [PSI:MS]
synonym: "MS1-Count" EXACT [PMID:24494671]
is_a: MS:4000003 ! single value
relationship: has_metric_category MS:4000009 ! ID free metric
relationship: has_metric_category MS:4000012 ! single run based metric
relationship: has_metric_category MS:4000021 ! MS1 metric
relationship: has_value_type xsd\:int ! The allowed value-type for this CV term
relationship: has_units UO:0000189 ! count unit
```

A corresponding `qualityMetric` object in an mzQC file:

```
{
    "accession": "MS:4000059",
    "name": "number of MS1 spectra",
    "value": 8259,
    "unit": {
        "accession": "UO:0000189",
        "name": "count unit"
    }
}
```

## n-tuple

To report the number of MS2 scans per quantile:

```
[Term]
id: MS:4000062
name: MS2 density quantiles
def: "The first to n-th quantile of MS2 peak density (scan peak counts). A value triplet represents the original QuaMeter metrics, the quartiles of MS2 density. The number of values in the tuple implies the quantile mode." [PSI:MS]
synonym: "MS2-Density-Q1" RELATED [PMID:24494671]
synonym: "MS2-Density-Q2" RELATED [PMID:24494671]
synonym: "MS2-Density-Q3" RELATED [PMID:24494671]
is_a: MS:4000004 ! n-tuple
relationship: has_metric_category MS:4000009 ! ID free metric
relationship: has_metric_category MS:4000012 ! single run based metric
relationship: has_metric_category MS:4000022 ! MS2 metric
relationship: has_value_type xsd\:int ! The allowed value-type for this CV term
relationship: has_value_concept NCIT:C45781 ! Density
relationship: has_units UO:0000189 ! count unit
```

A corresponding `qualityMetric` object in an mzQC file:

```
{
    "accession": "MS:4000062",
    "name": "MS2 density quantiles",
    "value": [162,250,404],
    "unit": {
        "accession": "UO:0000189",
        "name": "count unit"
    }
},
```

## Table

To report the MS/MS precursor charge states:

```
[Term]
id: MS:4000063
name: MS2 known precursor charges fractions
def: "The fraction of MS/MS precursors of the corresponding charge. The fractions [0,1] are given in the 'Fraction' column, corresponding charges in the 'Charge state' column. The highest charge state is to be interpreted as that charge state or higher." [PSI:MS]
synonym: "MS2-PrecZ-1" NARROW [PMID:24494671]
synonym: "MS2-PrecZ-2" NARROW [PMID:24494671]
synonym: "MS2-PrecZ-3" NARROW [PMID:24494671]
synonym: "MS2-PrecZ-4" NARROW [PMID:24494671]
synonym: "MS2-PrecZ-5" NARROW [PMID:24494671]
synonym: "MS2-PrecZ-more" NARROW [PMID:24494671]
synonym: "IS-3A"  RELATED [PMID:19837981]
synonym: "IS-3B"  RELATED [PMID:19837981]
synonym: "IS-3C"  RELATED [PMID:19837981]
comment: the MS2-PrecZ metrics can be directly read from the table respective table rows, the ratios of IS-3 metrics must be derived from the respective table rows, IS-3A as ratio of +1 over +2, IS-3B as ratio of +3 over +2, IS-3C as +4 over +2.
is_a: MS:4000005 ! table
relationship: has_metric_category MS:4000009 ! ID free metric
relationship: has_metric_category MS:4000012 ! single run based metric
relationship: has_metric_category MS:4000020 ! ion source metric
relationship: has_metric_category MS:4000022 ! MS2 metric
relationship: has_column MS:1000041 ! charge state
relationship: has_column UO:0000191 ! fraction
```

A corresponding `qualityMetric` object in an mzQC file:

```
{
    "accession": "QC:4000063",
    "name": "MS2 known precursor charges fractions",
    "value": {
        "MS:1000041": [1,2,3,4,5,6],
        "Fraction": [ 0.000, 0.683, 0.305, 0.008, 0.002, 0.002]
    },
    "unit": [
        {
            "accession": "MS:1000041",
            "name": "charge state"
        },
        {
            "accession": "UO:0000191",
            "name": "fraction"
        }
    ]
}
```

## Matrix

```
TODO
```

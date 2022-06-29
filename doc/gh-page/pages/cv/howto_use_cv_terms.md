# CV Term Usage Guide

The translation from CV terms to elements in an mzQC file depends on the term's
value type and is pretty straightforward.

## Single Value

To report the number of MS1 scans in a peak file:

```
[Term]
id: QC:4000059
name: Number of MS1 spectra
def: "The number of MS1 events in the run." [PSI:QC]
is_a: QC:4000003 ! single value
is_a: QC:4000010 ! ID free
is_a: QC:4000023 ! MS1 metric
comment: A lower number of MS1 spectra acquired during one sample run compared to similar runs can indicate mismatched instrument settings or issues with the instrumentation or issues with sample amounts.
relationship: has_relation MS:1000579 ! MS1 spectrum
relationship: has_relation QC:4000013 ! QC metric relation: single run
property_value: has_units UO:0000189 ! count unit
synonym: "MS1-Count" EXACT []
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
id: QC:4000062
name: MS2 density per quantile
def: "The first to n-th quantile of MS2 scan peak counts." [PSI:QC]
is_a: QC:4000004 ! n-tuple
is_a: QC:4000010 ! ID free
is_a: QC:4000024 ! MS2 metric
relationship: has_relation MS:1000035 ! peak picking
relationship: has_relation QC:4000013 ! QC metric relation: single run
synonym: "MS2-Density-Q1" RELATED []
synonym: "MS2-Density-Q2" RELATED []
synonym: "MS2-Density-Q3" RELATED []
```

A corresponding `qualityMetric` object in an mzQC file:

```
{
    "accession": "MS:4000062",
    "name": "MS2 density quantiles",
    "value": [
        162,
        250,
        404
    ],
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
id: QC:4000063
name: MS2 known precursor charges fractions
def: "The fraction of MS/MS precursors of the corresponding charge. The fractions [0,1] are given in the 'Fraction' column, corresponding charges in the 'Charge state' column. The highest charge state is to be interpreted as that charge state or higher. " [PSI:QC]
is_a: QC:4000006 ! table 
is_a: QC:4000010 ! ID free
is_a: QC:4000024 ! MS2 metric
is_a: QC:4000025 ! ion source metric
relationship: has_relation MS:1000041 ! charge state
relationship: has_relation QC:4000013 ! QC metric relation: single run
property_value: has_column: QC:4000238 ! Charge state
property_value: has_column: QC:4000239 ! Fraction
synonym: "MS2-PrecZ-1" RELATED []
synonym: "MS2-PrecZ-2" RELATED []
synonym: "MS2-PrecZ-3" RELATED []
synonym: "MS2-PrecZ-4" RELATED []
synonym: "MS2-PrecZ-5" RELATED []
synonym: "MS2-PrecZ-more" RELATED []

[Term]
id: QC:4000238
name: Charge state
def: "The column contains charge states." [PSI:QC]
is_a: QC:4000107 ! Column type
property_value: has_units MS:1000041 ! charge state

[Term]
id: QC:4000239
name: Fraction
def: "The column contains fraction values as decimals." [PSI:QC]
is_a: QC:4000107 ! Column type
property_value: has_units UO:0000191 ! fraction
```

A corresponding `qualityMetric` object in an mzQC file:

```
{
    "accession": "QC:4000063",
    "name": "MS2 known precursor charges fractions",
    "value": {
        "Charge state": [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6"
        ],
        "Fraction": [
            0.000,
            0.683,
            0.305,
            0.008,
            0.002,
            0.002
        ]
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

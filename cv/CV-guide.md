# Examples of cv term use for QC

## Using existing term definitions to write a 
### single value metric:
If you would want to report the number of MS1 spectra for a particular run, you can use the cv Term
```
[Term]
id: QC:4000111
name: Number of MS1 spectra
def: "Number of MS1 spectra" [PSI:QC]
comment: A lower number of MS1 spectra acquired during one sample run compared to similar runs can indicate mismatched instrument settings or issues with the instrumentation.
is_a: QC:4000003 ! single value
is_a: QC:4000010 ! ID free
is_a: QC:4000001 ! QC metric
has_units: STATO:0000047! count
```
to define your metric object which would look like 
```
{
    "accession": "QC:4000111",
    "name": "Number of MS1 spectra",
    "value": 7130
}
```
where the value would then be implicitly interpreted as of type `count`.

### n-tuple:
If we choose to write a n-tuple type, for example:
```
[Term]
id: QC:4000113
name: MZ acquisition range
def: "Upper and lower limit of m/z values at which spectra are recorded." [PSI:QC]
comment: Acquisition levels can be used as a criterion to assess the comparability of instrument settings between runs. 
is_a: QC:4000010 ! ID free
is_a: QC:4000001 ! QC metric
is_a: QC:4000004 ! n-tuple
has_units MS:1000040 ! m/z
```
Then we can assign the tuples as an n-array and their units implicitly assumed to be of `m/z` unit like this:
```
{
    "accession": "QC:4000113",
    "name": "MZ acquisition range",
    "value": [400,1200]
}
```


### matrix:
TBD

### table:
If we want to report multiple types of values for multiple observations, we will choose a table. A table will be defined by it's columns, which can be optional. Here is an example
```
[Term]
id: QC:4000095
name: Sampling rates
definition: "The sampling rates of identified peptides and their respective frequency (accumulated by the sampling rate, i.e. how often peptides were sampled n times and how many peptides were resampled at that rate. Optionally, which peptides were sampled at that rate, space separated)" [PSI:QC]
comment: The sampling rate may give insights to peptide separation, dynamic exclusion settings and gradient efficiency.
is_a: QC:4000001 ! QC metric
is_a: QC:4000009 ! ID based
is_a: QC:4000006 ! table
has_column_type: QC:4000089 ! Sample rates
has_column_type: QC:4000090 ! Counts
has_optional_column_type: QC:4000091 ! Peptide sequences
```

Any metric object of the type `Sampling rates` will be expected to contain a column of name `Sample rates`  and `Counts` and may have `Peptide sequences`. These define the respective column values as follows.

```
[Term]
id: QC:4000089
name: Sample rates
def: "The column contains sample rates as number of occurrences." [PSI:QC]
is_a: QC:4000082 ! Defined value type
has_units: PATO:0000161 ! rate

[Term]
id: QC:4000090
name: Counts
def: "The column contains counts of occurrences of a common type." [PSI:QC]
is_a: QC:4000082 ! Defined value type
has_units: STATO:0000047 ! count

[Term]
id: QC:4000091
name: Peptide sequences
def: "The column contains peptide sequences." [PSI:QC]
is_a: QC:4000082 ! Defined value type
has_units: NCIT:C45253 ! String
```
A metric object for two peptides being samples 5 times ("DYHTVLGAR", "AGLVTHYDR") and three peptides sampled 3 times ("IQACSGNDLQQWAR","AWQQLDNGSCAQIR","MATSGMMTELGK") will look like this.
```
{
    "accession": "QC:4000113",
    "name": "MZ acquisition range",
    "value": {
	    "Sample rates": [5,3],
	    "Counts": [2,3],
	    "Peptide sequences": ["DYHTVLGAR AGLVTHYDR","IQACSGNDLQQWAR AWQQLDNGSCAQIR MATSGMMTELGK"]
    },
}
```


# Define a new metric term for ...
If a desired metric is not yet defined, you will need a cv term definition before you can write a metric object. First to decide is what type of value your new metric will have.

## single value, n-tuple, matrix:
This is straight forward for these types. 
1. Make sure, the term is not defined yet in the QC ontology
2. Define a reasonable descriptive name while keeping concise
3. Describe the term content, context (relations), and usage 
4. Define its value type and unit 

Say we want to define a metric for the fastest frequency for MS/MS acquisition. We look up the QC ontology and for the purpose of this document pretend, no such term exists. We coin the name `Maximal MS2 frequency` and define it as `"The fastest frequency for MS/MS collection in any minute over the complete run"`.  This will clearly be a single value type, we do not need any spectrum identifications to assign its value, but it will be for the tandem spectra of one particular run.  And it will clearly be of type frequency, in particular the sampling frequency of spectra per minute. All together, it might look like this.

```
[Term]
id: QC:4000061
name: Maximal MS2 frequency
def: "The fastest frequency for MS/MS collection in any minute over the complete run" [PSI:QC]
is_a: QC:4000003 ! single value
is_a: QC:4000010 ! ID free
is_a: QC:4000024 ! MS2 metric
relationship: has_relation MS:1000029 ! sampling frequency
relationship: has_relation MS:1000580 ! MSn spectrum
relationship: has_relation QC:4000013 ! QC metric relation: one run
```
where the content, context (relations), and usage are described by the is_a and relationship expressions. The unit is implied as `has_units UO:0000106 ! hertz` per the `has_relation MS:1000029 ! sampling frequency` relationship.

## tables
In case multiple types are involved,  the procedure changes slightly. 

`Defined value type`s are no renamed unit types! In case you need multiple columns of the same type, it would not be helpful to have a `Defined value type` to be the same as a unit as this would result in column name conflicts. For this purpose, `Defined value type`s are 'named' stand-ins for unit types where same type occurrences are expected frequently. This also makes automated parsing a lot easier, as now each column has a dedicated name, and well defined/describet content, too, thanks to the defintion of the `Defined value type`.

For example if we want a table to describe total ion current chromatogram for visualisation purposes. It would be for one particular run and it would need a representation for retention time/intensity coordinates.  
We discover two types in the QC ontology which fit our needs.
```
[Term]
id: QC:4000083
name: Retention time points
def: "The column contains retention time points in seconds." [PSI:QC]
is_a: QC:4000082 ! Defined value type
has_units: UO:0000010 ! second

[Term]
id: QC:4000084
name: Relative intensities 
def: "The column contains relative intensity values of one type." [PSI:QC]
is_a: QC:4000082 ! Defined value type
has_units: MS:1000043 ! intensity unit
```
With these, we can define it as a ID free table type metric for chromatograms of a run.
```
[Term]
id: QC:4000067
name: Total ion current chromatogram
def: "The total ion current chromatogram. Each observation is a coordinate pair of RT and intensity." [PSI:QC]
is_a: QC:4000006 ! table
is_a: QC:4000010 ! ID free
is_a: QC:4000022 ! chromatogram metric
relationship: has_relation MS:1000235 ! total ion current chromatogram
relationship: has_relation QC:4000013 ! QC metric relation: one run
has_column_type: QC:4000083 ! Retention time points
has_column_type: QC:4000084 ! Relative intensities 
```


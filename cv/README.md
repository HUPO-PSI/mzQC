# The Quality Control Controlled Vocabulary (QC CV)

The PSI-QC controlled vocabulary (CV) is intended to provide terms for the 
definition of quality metrics and related supporting values. The CV contains 
entries for metrics that can be recorded in the mzQC files. While the mzQC 
format allows storing any metric information, the CV makes it possible to 
interpret the actual values.

## CV Term Creation for QC Metric Definition

New CV terms have to be requested via the [mzQC GitHub issue 
tracker](https://github.com/HUPO-PSI/mzQC/issues). Upon creating a new issue, 
you should select the "Request for new CV term" option. This will produce a 
template that will guide you in providing the necessary information to request 
your new CV term, as detailed below. If additional information or clarifications 
beyond the initial request are needed, the mzQC working group will work with you 
to finalize your CV term request. When all the necessary information has been 
provided, a new CV term will be created based on the request and added to the QC 
CV.

Each metric (and CV entry request) MUST include the following information:

- Name: A (short) string describing your metric.
- Definition: A longer description. This MUST include information about how the 
metric should be represented in an mzQC file.
- Comment: OPTIONAL details on how the metric should be interpreted (e.g. is a 
higher value better, can it only be interpreted relative to...).
- Value type:  Is the metric type a single value, an n-tuple, a table, or a
matrix?
- Unit: OPTIONAL unit of the value, specified using an existing CV term.
- Categorization: A categorization can OPTIONALLY be supplied. Examples are 
whether the metric depends on spectrum, peptide, protein, or metabolite 
identifications; or to describe the metric context.

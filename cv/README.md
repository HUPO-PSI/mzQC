# The mzQC controlled vocabulary (CV)

The CV contains entries for metrics which can be recorded in the mzQC files. Even if mzQC allows to just store any metric information, the CV helps to facilitate the interpretation of the actual values. Each entry in the CV has a unique ID, QC:XXXXX number, followed by a human readable name, which both will also be given in teh mzQC files. A short explanation of the entry and how it SHOULD be stored in the mzQC file is given in the entry's definition.
The comment gives a short means on how to interpret the actual values of the metric.

# Request new entry in the CV

If you like to record a metric which is not yet defined in the current CV, we just need some information of your metric:

- Name: some (short) string describing your metric
- Definition: a longer description and how the metric shoudl be stored in the mzQC file
- How to interpret the metric value: how your metric can be interpreted (e.g. is a higher value better, can it only be interpreted relative to...)
- type of the metric: Is your metric a single value, an n-tuple, a corresponding list, matrix, table, ...?
- are Identifications needed: Does teh metric depend on spectrum/peptide/metabolomical identifications?


If you have this information, you have two ways to request a new CV entry, either:
* visit https://github.com/HUPO-PSI/mzQC/issues and open a new issue and make a 'Request for new CV entry'
* or write to the mailing list `psidev-qc-dev@lists.sourceforge.net`

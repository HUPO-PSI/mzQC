#The CV section contains the work on the QC metrics 

We might start with collecting a solid base of QC metriccs and how to describe them, then define CV entries from these definitions and draft examplary qcML elements (value and graphical representations to better understand the metric's expressiveness)

Note that this is free-form so your creative ideas are not hindered, but ultimatively a common structure would be desired: 

The structure is as follows:
1.  a file containing the collection of metrics
    *  a metric ready to cast into an cv entry should define a
        *  name
        *  cardinality of the described MS experiments (i.e. how many runs)
        *  what kind of MS experiment it is meaningful on (e.g. sample run, calibration run, ..., any)
        *  whether it is ID free (and which concept of an MS experiment it encompasses, e.g. PSMs, Features, Quant., Identifications)
        *  in which format the data should be present to compute the metric
        *  (value_shortname [unit] {datatype}, ...)
        *  a explanatory description!
2. examples of each metric
    *  this might be a plot or a envisioned qcML ```<qcMetric>``` xml element
3. a obo file containing the metrics defined as (hierarchical) CV
    *  for now the old entries are kept for reference
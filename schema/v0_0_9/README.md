This is an overview of the current schema.

Right now, a qcML instance is structured as a root element comprising:
* one or more RunQuality elements,
* one ore more SetQuality elements,
* a CVList element denoting the used CVList and
* optionally an element containing a stylesheet

![root][images/qcML_0_0_9_root.png]

One RunQuality element contains all metrics and the meta data for a specific run.

![root][images/qcML_0_0_9_RunQuality.png]

The SetQuality element is, apart from the name, syntactically the same as a RunQuality element, though as the differing name is indicating, used for different semantics.

The QualityParameter element is representing a metric.

![root][images/qcML_0_0_9_QualityParameter.png]

Which metric is denoted by the CVParamType inherited parts.
The metric data for the particular Run/Set are kept in the content element.
It's content can be of any type and would have to be defined by the metric to keep machine readability.

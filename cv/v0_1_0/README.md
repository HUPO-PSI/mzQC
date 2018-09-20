# Notes on the CV

julianu: weiter bei "Quameter metric: MS1-Count"


The cv structures the metrics and gives a description of each metric. Classes of
metrics are hierarchical and each metric has to have some elements:

1) each metric must have the ancestor QC:4000001 "QC metric" in its is_a
   relations

2) each metric MUST have a child of QC:4000002 "QC metric type" in its is_a
   relations which describes, how the values of the metric are interpreted and
   have to be modeled in the QC document.

To be discussed:
3) each metric MUST have at least one child of QC:4000008 "QC metric basis" in
   its is_a relations which describes the origin of the metric regarding
   quantification and identification

4) each metric MUST have a child of QC:4000012 "QC metric relation" in its
   has_relation relations which describe the origin of the metric's calculation

5) metrics with tuples (matrices and tables as well?) have the dimensions
   defined in the cvParam value (NOT the actual metric's value), like
   "XIC-FWHM quantiles" and "XIC-Height quantiles to Q1"


TODO in json files:
* to allow the value of a CV object to be something useful, like the length of
  a tuple, we need something like "cv_value" in the json, which must not be
  mistaken as the "value", which is the actual value of the metric. This was not
  done like this in previous PSI formats, but should be possible.
* we can put the dimensions of matrices and table in these CV values as well


TODO CV:
* rename "XIC-WideFrac" to better correspond to its description
* description of "Ambient humidity", why is this a tuple?
* check other descriptions


RENAMED/NEW items:
* new: "quality control metrics generating software" (should directly go into PSI OBO, ask Gerhard for it)
* new: "QuaMeter IDFree" (should directly go into PSI OBO, ask Gerhard for it)
* new: "iMonDB" (should directly go into PSI OBO, ask Gerhard for it)
* "Quameter metric: XIC-WideFrac" -> "XIC-WideFrac"
* "Quameter metric: XIC-FWHM Q1-Qn" -> "XIC-FWHM quantiles"
* "Quameter metric: XIC-Height Q2-Qn" -> "XIC-Height quantiles ratio to Q1"
* "Quameter metric: RT-Duration" -> "RT-duration"
* "RT-TIC" -> "RT of TIC quantile"
* "Quameter metric: RT-MS1 Q1-Qn" -> "MS1 quantiles RT fraction"
* "Quameter metric: RT-MS2 Q1-Qn" -> "MS2 quantiles RT fraction"
* "Quameter metric: MS1-TIC-Change Q2-Qn" -> "MS1 quantile TIC change ratio to Q1"
* "Quameter metric: MS1-TIC Q2-Qn" -> "MS1 quantile TIC ratio to Q1"
* "Quameter metric: MS2-Freq-Max" -> "maximal MS2 frequency"
* "Quameter metric: MS2-Density" -> "MS2 density per quantile"
* "Quameter metric: MS2-PrecZ-XYZ" -> "MS2 known precursor charges fractions"
* new: "MS2 unknown and likely precursor charges fractions"
* new: "Precursor median m/z for IDs"
* new: "Fraction of MS2 identified at different MS1 quantiles"

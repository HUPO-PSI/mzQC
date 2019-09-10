# Notes on the CV

To request a new CV entry, either:
* visit https://github.com/HUPO-PSI/mzQC/issues and open a new ticket via 'Request for new CV entry'
* write to the mailing list ....@.... (todo)

The CV structures the metrics and gives a description of each metric. Classes of
metrics are hierarchical and each metric has to have some elements:

1) each metric must have the ancestor QC:4000001 "QC metric" in its is_a
   relations

2) each metric MUST have a child of QC:4000002 "QC metric type" in its is_a
   relations which describes, how the values of the metric are interpreted and
   have to be modeled in the QC document.

3) metrics with tuples (matrices and tables as well?) have the dimensions
   defined implicitly by the length of the json element.

4) each metric MUST have a child of QC:4000012 "QC metric relation" in its
   has_relation relations which describe the origin of the metric's calculation
   and SHOULD have at least has_relation to a term it actually represents

5) each metric MUST have at least one child of QC:4000008 "QC metric basis" in
   its is_a relations which describes the origin of the metric regarding
   quantification and identification




TODO CV:
* rename "XIC-WideFrac" to better correspond to its description
* check other descriptions

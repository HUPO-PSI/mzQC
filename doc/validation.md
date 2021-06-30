# Validation of mzQC Files

Here we give a brief overview of syntactic and semantic validation requirements
of mzQC files. Full validation is implemented in the
[mzqc-pylib](https://github.com/bigbio/mzqc-pylib) reference implementation.

## Syntactic Validation

With the help of the mzQC JSON schema, mzQC instances can be readily checked for
syntactic schema compliance. There are a [number of validators already
implemented for use in various programming
languages](https://json-schema.org/implementations.html) that support validation
of JSON schema draft-07 from which the mzQC schema is designed.

## Semantic Validation

Due to the advanced design of the mzQC JSON schema, many aspects of a valid mzQC
file can already be verified via syntactic validation without the need of
explicit semantic validation. There are, however, a few additional semantic
rules that need to be followed to create fully compliant mzQC files.

- All used `controlledVocabulary` elements MUST reference a valid ontology.
- All used CV terms (including the quality metrics) must be present in one of
the controlled vocabularies listed in the files `controlledVocabularies`
element, matching in name and accession.
- All `qualityMetric` elements MUST be unique within their `runQuality` or
`setQuality` parent.
- The value type of `qualityMetric` elements MUST match the specification in the
CV (i.e. single value, n-tuple, matrix, or table).
- The value of `qualityMetric` MUST match its unit definition (and type
implicitly).
- All columns of table `qualityMetric` elements MUST have the same length.
- `label` attributes in the metadata elements MUST be unique within its mzQC
file.
- All `inputFile` elements MUST have a unique `location` attribute within their
`runQuality` or `setQuality` element.

Additionally, more detailed checks might be performed to assess the validity of
specific metric values on a case-by-case basis (e.g., percentages should sum to
100%).

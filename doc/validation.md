# Format Validation
As any other HUPO-PSI format, '.mzQC' has a formally described by the specification document and the format schema, hence any instance can be checked for its validity. 
This document serves as a central hub on all things validation for mzQC.

## Syntactic Validation
Most rules governing the adherence to the mzQC format standard can be checked for compliance with the help of the JSON schema. 
There are a number of validators already implemented for use in various programming languages (https://json-schema.org/implementations.html) that support validation of JSON schema draft-07 from which the mzQC schema is designed. 
Both syntactic and semantic validation are implemented in the mzQC-pylib for reference.

## Semantic Validation
There are few rules and situations described in the formats standard specification, which cannot be readily checked against with the schema and must be checkced by other means.
The following list collects 'extra' rules that need to be checked alongside schema compliance:
* All used controlled vocabularies MUST reference a valid ontology
* All used CV terms (including the metrics) must be present in one of the controlled vocabularies listed in the files controlledVocabularies element, matching in name and accession.
* All *qualityParameters* MUST be unique within a *runQuality* or *setQuality* element 
* *qualityParameters* MUST carry values as specified in the CV definition (i.e. single value, n-tuple, matrix, or table)
* Each *qualityParameter* value MUST correspond to its metrics unit definition (and type implicitly)
* *qualityParameters* of tabular type MUST have the same column length for all columns used
* *label*s in the metadata of runQuality and setQuality elements MUST be unique within the file
* All *inputFile* elements of a runQuality or setQuality element MUST have unique location attributes within the *runQuality* or *setQuality* element

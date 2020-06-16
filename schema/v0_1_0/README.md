# README

## Description of mzQC schema v0.1.0:

- Root element `mzQC`.
    - Required `version` of regex `\d+.\d+.\d+`.
    - Required list of `controlledVocabularies`s.
    - Required either a list of `runQualities` or a list of `setQualities`. This list needs to have at least one element, while an unbounded maximum is allowed. These lists of both `runQuality` and `setQuality` can be present simultaneously.
    - Optional element `creationDate` describing the creation date of the current mzQC file in date time string iso-format

- `runQuality`/`setQuality`: Exactly the same, only the key is different.
    - Required `metadata`.
        - Required list of at least one `inputFile`.
            - Required properties `location` (URI), `name`, and `fileFormat`.
            - Optional list of `fileProperties`, which contains elements referring to CV entries.
        - Required list of at least one `analysisSoftware`.
            - Required attributes to refer to a CV entry.
            - Additional required attributes `version` and `uri`.
    - Required list of at least one `qualityMetrics`.
        - Required attributes to refer to a CV entry: `accession` (PURL controlled vocabulary reference including the accession for the term), `name`.
        - Optional attributes: `description`, `value`, `unit`.
        - `unit` is a similar sub-element referring to CV entry.
        - `value` can be anything: string, number, list, nested element. We have to do semantic validation based on information from the CV.

- `controlledVocabularies`: References to controlled vocabularies.
    - Required attribute: `namespace` (PURL reference to the controlled vocabulary).
    - Required attribute: `name`, `uri`.
    - Optional attribute: `version`.


## Changelog 

- added optional creationDate
- cv -> controlledVocabularies
- qualityParameters -> qualityMetrics
- added optional fileProvenancecvParameters
- optional cvParameters to metadata
- internalised the cv ref which also acted as name of the json object in the controlledVocabularies list as attribute into the now dynamic object
- Removed the `cvRef` attribute in favor of a PURL reference in `accession`.

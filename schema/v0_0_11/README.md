# README

Description of mzQC schema v0.0.11:

- Root element `mzQC`.
    - Required `version` of regex `\d+.\d+.\d+`.
    - Required list of `cv`s.
    - Required either a list of `runQuality` or a list of `setQuality`. This list needs to have at least one element, while an unbounded maximum is allowed. Lists of both `runQuality` and `setQuality` can be present simultaneously.

- `runQuality`/`setQuality`: Exactly the same, only the key is different.
    - Required `metadata`.
        - Required list of at least one `inputFile`.
            - Required properties `location` (URI), `name`, and `fileFormat`.
            - Optional list of `fileProperties`, which contains elements referring to CV entries.
        - Required list of at least one `analysisSoftware`.
            - Required attributes to refer to a CV entry.
            - Additional required attributes `version` and `uri`.
    - Required list of at least one `qualityParameter`.
        - Required attributes to refer to a CV entry: `cvRef`, `accession`, `name`.
        - Optional attributes: `description`, `value`, `unit`.
        - `unit` is a similar sub-element referring to CV entry.
        - `value` can be anything: string, number, list, nested element. We have to do semantic validation based on information from the CV.

- `cv`: References to controlled vocabularies.
    - `key` = short (uppercase) string uniquely identifying the CV. To be used by the `cvRef` property in the parameters.
    - `value` = Element containing the CV information.
        - Required attributes: `name`, `uri`.
        - Optional attribute: `version`.

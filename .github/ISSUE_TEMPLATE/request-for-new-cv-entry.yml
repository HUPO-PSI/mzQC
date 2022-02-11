name: New CV Term
description: Use this template to request a new QC-related term.
body:
  - type: input
    id: name
    attributes:
      label: "What is the QC term's name?"
      placeholder: "Informative, human-readable name. The name should consist of maximum 100 characters and should only consist of alphanumeric characters, spaces, and punctuation marks."
    validations:
      required: true
  - type: textarea
    id: definition
    attributes:
      label: "Briefly describe the QC term."
      placeholder: "Describe the reason for proposing to include this term in the Controlled Vocabulary. Relevant details can include which information this term captures, the experimental set-up and workflow for which it is relevant, and the software from which the metric originates."
  - type: input
    id: unit
    attributes:
      label: "What is the QC term's unit?"
      placeholder: "Optional unit of the value, specified using an existing CV term. Units should preferably be sourced from the Units of Measurement Ontology (https://www.ebi.ac.uk/ols/ontologies/uo) or the Statistical Methods Ontology (http://stato-ontology.org/)."
  - type: dropdown
    id: value_type
    attributes:
      label: "Value type"
      multiple: true
      options:
        - MS:4000003 ! single value
        - MS:4000004 ! n-tuple
        - MS:4000005 ! table
        - MS:4000006 ! matrix
  - type: textarea
    id: extra
    attributes:
      label: "Describe any additional information."
      placeholder: "Add any additional details that might be relevant, such as categorization of the term. Some examples include whether the term is ID-free, ID-based, or quantification-based; the step in the experimental set-up for which it is relevant (chromatography, ionization, MS1, MS2, etc.); and whether the term is applicable to a single spectrum, single run, or multiple runs. Optional information can be included to provide additional calculation and interpretation details (e.g. whether smaller or larger values are desirable). If applicable, it is recommended to include a reference to the corresponding code."

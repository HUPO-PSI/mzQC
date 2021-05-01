---
name: Request for new CV term
about: Use this template to request a new term in the QC CV
title: "[CV request]"
labels: request for new CV entry
assignees: julianu

---

**Purpose:** Informally describe the reason for proposing to include this term in the QC Controlled Vocabulary. Relevant details can include which information this term captures, the experimental set-up and workflow for which it is relevant, and the software from which the metric originates.

**Name:** Informative, human-readable name. The name should consist of maximum 100 characters and should only consist of alphanumeric characters, spaces, and punctuation marks.

**Definition:** A short explanation of the term and how it should be stored in the mzQC file. The definition should provide aid in interpreting the values, but should not include calculation details or subjective interpretation details.

**Comment:** An optional comment can be included to provide additional calculation and interpretation details. For example, whether smaller or larger values are desirable. If applicable, it is recommended to include a reference to the corresponding code.

**Value type:** `single value`, `n-tuple`, `table`, or `matrix`.

**Unit:** Optional unit of the value, specified using an existing CV term. Units should preferably be sourced from the Units of Measurement Ontology (https://www.ebi.ac.uk/ols/ontologies/uo) or the Statistical Methods Ontology (http://stato-ontology.org/).

**Category:** Different categories can be assigned to CV terms. Some examples include whether the metric is ID-based or ID-free, the element of the experimental set-up for which it is relevant (chromatography, ionization, MS1, MS2, etc.)

---
layout: page
title: Tutorials
permalink: /tutorials/
---

We have a couple of tutorials and guides to offer, this page will lead you to them:

### with python
* read mzQC: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MS-Quality-hub/pymzqc/blob/v1.0.0rc1/jupyter/colab/read_in_5_minutes.ipynb)
* write mzQC: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MS-Quality-hub/pymzqc/blob/v1.0.0rc1/jupyter/colab/write_in_5_minutes.ipynb)
* demo video
<iframe width="560" height="315" src="https://www.youtube.com/embed/vZXJuPl2yGw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### with R
* [Rlib for mzQC(TBA)](TBA)
* PTXQC demo
<iframe width="560" height="315" src="https://www.youtube.com/embed/sb-mydbNRS4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


## Validation
If you have many mzQC files to validate, or the validation API is temporaily unreachable,
you can set up your own validation process without much effort!

### Container
The container solution is the least effort, but requires you have the singularity container engine installed.

### Local Installation of pymzqc
This solution requires you to install pymzqc. 
In most cases it will be as easy as simply `pip install pymzqc`.
For all the latest instructions on installation of pymzqc and validation, see [its repository](https://pymzqc.readthedocs.io/en/v1.0.0rc1_b/accessories.html#local-validation-testing).

## JSON
If you are new to JSON or file formats (with JSON), 
the next few links should provide you with an overview:

- [JSON (by W3C)](https://www.w3schools.com/js/js_json_intro.asp)
- [JSON (by mozilla)](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON)
- [File format schemas with JSON](https://json-schema.org/learn/getting-started-step-by-step.html)
- JSON crash course (by freecodecamp)
<iframe width="560" height="315" src="https://www.youtube.com/embed/GpOO5iKzOmY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


## Ontologies
Ontologies also known as controlled vocabularies are used in mzQC to manage metric definitions and metric value content. 
Here is a list of links and documents that should help you out in case you want to know more.
* Ontologies are powerful tools, we mostly use them as [controlled vocabularies](https://en.wikipedia.org/w/index.php?title=Controlled_vocabulary&oldid=1092198296)
* The W3C has a bit broader explanation of [ontologies](https://www.w3.org/standards/semanticweb/ontology)
* Visit the [HUPO-PSI webpage](https://www.psidev.info/groups/controlled-vocabularies) for more information on CV use in different settings.
* __Browse our controlled vocabulary terms on [OLS](https://www.ebi.ac.uk/ols/ontologies/ms/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FMS_4000000&lang=en&viewMode=All&siblings=false)__
* If you want to start with the foundations and get ambitious here are the resources [from protege for ontology development](https://protege.stanford.edu/publications/ontology_development/ontology101.pdf)
* <sub>Luckily, we have all the relevant metrics and terms in PSI-MS CV, so no [Ontology Dowsing](https://www.w3.org/wiki/Ontology_Dowsing) necessary</sub>


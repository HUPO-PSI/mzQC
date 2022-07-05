---
layout: page
title: "mzQC at a glance"
permalink: /use-cases/at-a-glance/
---

This is a discription of a barebones mzQC example file that should give you an overview over the overall structure of things. 
We will visit the elements one-by-one and describe what they are and their use.
```
{ 'mzQC':
```
The complete document structure as defined in the schema has to be found under the root element 'mzQC'.
```
  {'controlledVocabularies': [
```
The 'controlledVocabularies' is a list of 'controlledVocabulary' elements, representing those vocabularies, which' terms are used in the document.
```
		{'name': 'Proteomics Standards Initiative Mass Spectrometry Ontology', 'uri': 'https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo', 'version': '4.1.7'},
		{'name': 'Proteomics Standards Initiative Quality Control Ontology', 'uri': 'https://github.com/HUPO-PSI/mzQC/raw/master/cv/qc-cv.obo', 'version': '0.1.0'},
		{'name': 'Unit Ontology', 'uri': 'http://ontologies.berkeleybop.org/uo.obo', 'version': 'releases/2020-03-10'}
	],
```
Each 'controlledVocabulary' needs to have it's corresponding name, version, and uri. 
Of course we also need some information aboutvalidator/the current mzQC document, too. 
These are simple strings, the 'creationDate' has to be formatted according to ISO 8601.
```
	'creationDate': '2020-07-29T11:17:09', 
	'version': '1.0.0',
```
Next we come to describe the quality of a ms experiment, 
either a 'runQuality' for quality metrics about a single run or 
'setQuality' (then of course in a separate 'setQualities' list - not shown) for quality metrics about a collection of runs.

```
	'runQualities': [
```
For each 'runQuality' of course we need information about the run itself,
like which files were considerd for the metric calculation and the software used. 
We collect this in 'metadata'.
```
		{'metadata': 
```
Each of these metadatapoints is a 'cvParameter' element, so it needs at least a name and an accession, and if neccessary a value. 
Exceptions are file 'name' which is a simple string to reference the file by later, 
and the 'location', where a URI (either URL or filesystem location like shown) will do.
Softwares are collected in the 'analysisSoftware' list, files considered in the 'inputFiles' list.
```
			{'analysisSoftware': [{'accession': 'QC:9999999', 'name': 'bestqctool', 'uri': 'http://www.qc-for-protein-pros.org', 'version': '1.2.3'}],
			'inputFiles': [
				{'fileFormat': {'accession': 'MS:1000584', 'name': 'mzML format'},
				'fileProperties': [{'accession': 'MS:1000747', 'name': 'completion time', 'value': '2017-12-08-T15:38:57Z'}],
				'location': 'file:///folder/file.mzML',
				'name': 'file'
				}
			]},
```
You can imagine that there are several file properties you'd want to associate with a file of a real mzQC file, so 'fileProperties' is a list of 'cvParameters'.

Finally, we collect the metrics in a 'qualityMetrics' list. 
Each metric is represented as a 'cvParameter', too, but here we most likely also want the metric value. 
The definition to the metric can be found in the controlled vocabularies. 
```
		'qualityMetrics': [
			{'accession': 'QC:4123456', 'name': 'ultimate quality level', 'value': 9000}
		]}
	]}
}
```
so all in all, here is the mzQC in complete and uninterrupted:
```
{ "mzQC":
	{'controlledVocabularies': [
		{'name': 'Proteomics Standards Initiative Mass Spectrometry Ontology', 'uri': 'https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo', 'version': '4.1.7'},
		{'name': 'Proteomics Standards Initiative Quality Control Ontology', 'uri': 'https://github.com/HUPO-PSI/mzQC/raw/master/cv/qc-cv.obo', 'version': '0.1.0'},
		{'name': 'Unit Ontology', 'uri': 'http://ontologies.berkeleybop.org/uo.obo', 'version': 'releases/2020-03-10'}
	],
	'creationDate': '2020-07-29T11:17:09', 
	'version': '1.0.0',
	'runQualities': [
		{'metadata': 
			{'analysisSoftware': [{'accession': 'QC:9999999', 'name': 'bestqctool', 'uri': 'http://www.qc-for-protein-pros.org', 'version': '1.2.3'}],
			'inputFiles': [
				{'fileFormat': {'accession': 'MS:1000584', 'name': 'mzML format'},
				'fileProperties': [{'accession': 'MS:1000747', 'name': 'completion time', 'value': '2017-12-08-T15:38:57Z'}],
				'location': 'file:///dev/null',
				'name': 'file'
				}
			]},
		'qualityMetrics': [
			{'accession': 'QC:4123456', 'name': 'ultimate quality level', 'value': 9000}
		]}
	]}
}
```

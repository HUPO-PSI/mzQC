---
layout: page
title: "Incorporating QC Metrics in mzML Files"
permalink: /examples/adv_mzqc_in_mzml/
---

While QC metrics in the PSI-MS controlled vocabulary are primarily intended for use in mzQC files, they can also be embedded directly within other file formats developed by the Proteomics Standards Initiative, such as [mzML](https://github.com/HUPO-PSI/mzML) and [mzIdentML](https://github.com/HUPO-PSI/mzIdentML) files.
This integration is particularly useful when it's preferred to store a limited set of QC metrics alongside the data they describe, thereby enhancing data integrity and accessibility.

You can view a comprehensive example of an mzML file incorporating QC metrics [here](https://github.com/HUPO-PSI/mzQC/tree/main/specification_documents/examples/adv_mzqc_in_mzml.mzml).
Below, we detail the steps and elements involved in this process.

1. **Source file specification**

Define the source of the QC metrics using a `sourceFile` element.
This specifies the mzQC file as an input file, similarly to how other input files are handled within mzML:

```
<sourceFile id="QC1" name="BSA1_F1.mzQC" location="file:///examples/">
	<cvParam cvRef="MS" accession="MS:1003160" name="mzQC format" />
</sourceFile>
```

2. **Software and data processing**

Document the software and data processing steps utilized to generate the mzQC file and compute the QC metrics:

```
<software id="qc_0" version="0" >
	<cvParam cvRef="MS" accession="MS:1000799" name="custom unreleased software tool" value="https://hupo-psi.github.io/mzQC/" />
</software>
```

And:

```
<dataProcessing id="dp_sp_2">
	<processingMethod order="0" softwareRef="qc_0">
		<cvParam cvRef="MS" accession="MS:1000543" name="data processing action" value="QC metrics calculation" />
	</processingMethod>
</dataProcessing>
```

3. **Inclusion of QC metrics**

Include the QC metrics at appropriate levels within the mzML structure:

- **Run-level metrics**

Metrics that relate to all spectra in the file are embedded at the `run` level using a `cvParam`:

```
<run id="ru_0" defaultInstrumentConfigurationRef="ic_0" sampleRef="sa_0" startTimeStamp="2009-08-09T22:32:31" defaultSourceFileRef="sf_ru_0">
	<cvParam cvRef="MS" accession="MS:4000063" name="MS2 known precursor charges fractions" value="{'MS:1000041': [1, 2, 3, 4], 'UO:0000191': [0.0000, 0.5721, 0.3535, 0.0743]}" />
	...
</run>
```

- **Individual spectrum metrics**

For metrics that relate to individual spectra, include these metrics at the `spectrum` level using a `cvParam`:

```
<spectrum id="spectrum=1011" index="0" defaultArrayLength="467" dataProcessingRef="dp_sp_0">
	...
	<cvParam cvRef="MS" accession="MS:4000068" name="spectra half-TIC" value="{'MS:1000767': ['spectrum=1011'], 'UO:0000191': [0.0235]}"/>
	...
</spectrum>
```

Repeat for each spectrum as necessary, adjusting the spectrum ID and corresponding values.

Note that because QC metrics in mzQC files are typically encoded at the level of runs rather than individual spectra, most spectrum-level QC metrics are defined in the PSI-MS controlled vocabulary as tabular metrics with rows for all spectra.
Therefore, when directly associating these metrics with a specific spectrum, the tables should contain a single entry only for this spectrum.

The key insight for embedding QC metrics in alternative file formats is that because they are backed by terms in the PSI-MS controlled vocabulary, they can be directly included using the respective functionalities for CV terms, such as `cvParam`.

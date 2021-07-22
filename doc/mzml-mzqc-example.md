## Example of mzQC metrics in mzML

QC metrics from _mzQC_ can also be incorporated into other PSI formats, like _mzML_ and _mzIdentML_, if it is preferable to keep all information in one file.
The following describes a tiny _mzML_, for which a QC tool calculated id-free QC metrics for all individual spectra of the run and a set of charge distribution metrics.
Due to the shared design properties of _mzQC_, metrics can be directly represented as XML `<cvParam>` elements, however their location bound to mzML schema constraints. 

The first addition to the _mzML_ is the source from which the metrics came from, for reference to more QC information on the run and documentation.
```
			<sourceFile id="QC1" name="BSA1_F1.mzQC" location="file:///">
				<cvParam cvRef="MS" accession="MS:1003160" name="mzQC format" value=""/>
			</sourceFile>
```
Next, the metrics computed for the whole run can be be deposited as a child of the `<run>` element itself. Metric objects from mzQC can be directly translated into `<cvParam>` elements.
```
	<run id="ru_0" defaultInstrumentConfigurationRef="ic_0" sampleRef="sa_0" startTimeStamp="2009-08-09T22:32:31" defaultSourceFileRef="sf_ru_0">
		<cvParam cvRef="QC" accession="QC:4000179" name="Charged spectra ratio +1 over +2" value="0" />
		<cvParam cvRef="QC" accession="QC:4000180" name="Charged spectra ratio +3 over +2" value="0.5454545454545454" />
		<cvParam cvRef="QC" accession="QC:4000181" name="Charged spectra ratio +4 over +2" value="0.012987012987012988" />
		<userParam name="mzml_id" type="xsd:string" value="20090810_SvNa_QC_BSA50fmol.RAW"/>
```
Please note that for example brevity purposes the _mzML_ was truncated to 3 spectra, however the metrics were calculated on the whole to reflect realistic values.

Next, the spectra metrics can be put as children of `<spectrum>` elements, in the same fashion as for the run metrics. As you can seen in the `<cvParam>` elements, it contains extra information in `cvRef`. This attribute is a reference to a data entry registering the controlled vocabularies used in the file much like in _mzQC_. This has to be added to finalise the _mzML_.
```
		<spectrumList count="3" defaultDataProcessingRef="dp_sp_0">
			<spectrum id="spectrum=1011" index="0" defaultArrayLength="467" dataProcessingRef="dp_sp_0">
				<cvParam cvRef="MS" accession="MS:1000127" name="centroid spectrum" />
				<cvParam cvRef="MS" accession="MS:1000511" name="ms level" value="1" />
				<cvParam cvRef="MS" accession="MS:1000294" name="mass spectrum" />
				<cvParam cvRef="MS" accession="MS:1000130" name="positive scan" />
				<cvParam cvRef="MS" accession="MS:1000504" name="base peak m/z" value="391.284088134766023"/>
				<cvParam cvRef="MS" accession="MS:1000505" name="base peak intensity" value="9.2884425e05"/>
				<cvParam cvRef="MS" accession="MS:1000285" name="total ion current" value="6.937649e06"/>
				<cvParam cvRef="MS" accession="MS:1000528" name="lowest observed m/z" value="300.000828877017"/>
				<cvParam cvRef="MS" accession="MS:1000527" name="highest observed m/z" value="2008.458458829989922"/>
				<cvParam cvRef="QC" accession="QC:4000264" name="Min. peaks for 50% of total spectra intensity" value="11"/>
				<userParam name="filter string" type="xsd:string" value="FTMS + p NSI Full ms [300.00-2000.00]"/>
				<userParam name="preset scan configuration" type="xsd:string" value="1"/>
				<scanList count="1">
					<cvParam cvRef="MS" accession="MS:1000795" name="no combination" />
					<scan >
						<cvParam cvRef="MS" accession="MS:1000016" name="scan start time" value="1501.41394042969" unitAccession="UO:0000010" unitName="second" unitCvRef="UO" />
						<scanWindowList count="1">
							<scanWindow>
								<cvParam cvRef="MS" accession="MS:1000501" name="scan window lower limit" value="300" unitAccession="MS:1000040" unitName="m/z" unitCvRef="MS" />
								<cvParam cvRef="MS" accession="MS:1000500" name="scan window upper limit" value="2000" unitAccession="MS:1000040" unitName="m/z" unitCvRef="MS" />
							</scanWindow>
						</scanWindowList>
					</scan>
				</scanList>
				<binaryDataArrayList count="2">
					<binaryDataArray encodedLength="4984">
						<cvParam cvRef="MS" accession="MS:1000514" name="m/z array" unitAccession="MS:1000040" unitName="m/z" unitCvRef="MS" />
						<cvParam cvRef="MS" accession="MS:1000523" name="64-bit float" />
						<cvParam cvRef="MS" accession="MS:1000576" name="no compression" />
						<binary>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</binary>
					</binaryDataArray>
					<binaryDataArray encodedLength="2492">
						<cvParam cvRef="MS" accession="MS:1000515" name="intensity array" unitAccession="MS:1000131" unitName="number of detector counts" unitCvRef="MS"/>
						<cvParam cvRef="MS" accession="MS:1000521" name="32-bit float" />
						<cvParam cvRef="MS" accession="MS:1000576" name="no compression" />
						<binary>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</binary>
					</binaryDataArray>
				</binaryDataArrayList>
			</spectrum>
			<spectrum id="spectrum=1012" index="1" defaultArrayLength="478">
				...
```
The `<cv>` elements are again very similar to the respective entries in _mzQC_, making translation easy.
```
	<cvList count="5">
		<cv id="MS" fullName="Proteomics Standards Initiative Mass Spectrometry Ontology" URI="http://psidev.cvs.sourceforge.net/*checkout*/psidev/psi/psi-ms/mzML/controlledVocabulary/psi-ms.obo"/>
		<cv id="UO" fullName="Unit Ontology" URI="http://obo.cvs.sourceforge.net/obo/obo/ontology/phenotype/unit.obo"/>
		<cv id="BTO" fullName="BrendaTissue545" version="unknown" URI="http://www.brenda-enzymes.info/ontology/tissue/tree/update/update_files/BrendaTissueOBO"/>
		<cv id="GO" fullName="Gene Ontology - Slim Versions" version="unknown" URI="http://www.geneontology.org/GO_slims/goslim_goa.obo"/>
		<cv id="PATO" fullName="Quality ontology" version="unknown" URI="http://obo.cvs.sourceforge.net/*checkout*/obo/obo/ontology/phenotype/quality.obo"/>
		<cv id="QC" fullName="Quality Control Ontology" version="unknown" URI="https://raw.githubusercontent.com/HUPO-PSI/mzQC/main/cv/qc-cv.obo"/>
	</cvList>
```

You can find the [full _mzML_ file in the examples folder](examples/mzml-mzqc-example.mzML).
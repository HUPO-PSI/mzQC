## Example of mzQC metrics in mzML

```
			<sourceFile id="QC1" name="BSA1_F1.mzQC" location="file:///">
				<cvParam cvRef="QC" accession="QC:???" name="mzQC format" value=""/>
			</sourceFile>
```

```
	<run id="ru_0" defaultInstrumentConfigurationRef="ic_0" sampleRef="sa_0" startTimeStamp="2009-08-09T22:32:31" defaultSourceFileRef="sf_ru_0">
		<userParam name="mzml_id" type="xsd:string" value="20090810_SvNa_QC_BSA50fmol.RAW"/>
		<cvParam cvRef="QC" accession="QC:4000179" name="Charged spectra ratio +1 over +2" value="0" />
		<cvParam cvRef="QC" accession="QC:4000180" name="Charged spectra ratio +3 over +2" value="0.5454545454545454" />
		<cvParam cvRef="QC" accession="QC:4000181" name="Charged spectra ratio +4 over +2" value="0.012987012987012988" />
```

```
			<spectrum id="spectrum=1012" index="1" defaultArrayLength="478">
				<cvParam cvRef="MS" accession="MS:1000127" name="centroid spectrum" />
				<cvParam cvRef="MS" accession="MS:1000511" name="ms level" value="1" />
				<cvParam cvRef="MS" accession="MS:1000294" name="mass spectrum" />
				<cvParam cvRef="MS" accession="MS:1000130" name="positive scan" />
				<cvParam cvRef="MS" accession="MS:1000504" name="base peak m/z" value="391.284057617188012"/>
				<cvParam cvRef="MS" accession="MS:1000505" name="base peak intensity" value="8.449700625e05"/>
				<cvParam cvRef="MS" accession="MS:1000285" name="total ion current" value="6.352711e06"/>
				<cvParam cvRef="MS" accession="MS:1000528" name="lowest observed m/z" value="300.000766845923977"/>
				<cvParam cvRef="MS" accession="MS:1000527" name="highest observed m/z" value="2008.458043526329902"/>
				<userParam name="filter string" type="xsd:string" value="FTMS + p NSI Full ms [300.00-2000.00]"/>
				<userParam name="preset scan configuration" type="xsd:string" value="1"/>
				<cvParam cvRef="QC" accession="QC:???" name="Min peaks for 50% of total spectra intensity" definition="Minimum number of peaks to explain at least 50% of total spectra intensity" value="10"/>
				<scanList count="1">
					<cvParam cvRef="MS" accession="MS:1000795" name="no combination" />
					<scan >
						<cvParam cvRef="MS" accession="MS:1000016" name="scan start time" value="1503.03125" unitAccession="UO:0000010" unitName="second" unitCvRef="UO" />
						<scanWindowList count="1">
							<scanWindow>
								<cvParam cvRef="MS" accession="MS:1000501" name="scan window lower limit" value="300" unitAccession="MS:1000040" unitName="m/z" unitCvRef="MS" />
								<cvParam cvRef="MS" accession="MS:1000500" name="scan window upper limit" value="2000" unitAccession="MS:1000040" unitName="m/z" unitCvRef="MS" />
							</scanWindow>
						</scanWindowList>
					</scan>
				</scanList>
				<binaryDataArrayList count="2">
					<binaryDataArray encodedLength="5100">
						<cvParam cvRef="MS" accession="MS:1000514" name="m/z array" unitAccession="MS:1000040" unitName="m/z" unitCvRef="MS" />
						<cvParam cvRef="MS" accession="MS:1000523" name="64-bit float" />
						<cvParam cvRef="MS" accession="MS:1000576" name="no compression" />
						<binary>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</binary>
					</binaryDataArray>
					<binaryDataArray encodedLength="2552">
						<cvParam cvRef="MS" accession="MS:1000515" name="intensity array" unitAccession="MS:1000131" unitName="number of detector counts" unitCvRef="MS"/>
						<cvParam cvRef="MS" accession="MS:1000521" name="32-bit float" />
						<cvParam cvRef="MS" accession="MS:1000576" name="no compression" />
						<binary>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</binary>
					</binaryDataArray>
				</binaryDataArrayList>
			</spectrum>
```

Don't forget to add an entry if you filtered the mzML with the help of the mzQC metrics used.

__author__ = 'walzer'
import pytest  # Eeeeeeverything needs to be prefixed with test ito be picked up by pytest, i.e. TestClass() and test_function()
from MZQC import MZQCFile as qc

"""
Unit tests for the MZQCFile library
"""

# String comparison -as in TestSerialisation- needs the 'empty' attributes, too, whereas Object comparison -as in TestDeserialisation- only compares 'non-empty' attributes
QM = '{\n    "cvRef": "QC",\n    "accession": "QC:4000053",\n    "name": "RT duration",\n    "description": "",\n    "value": 99,\n    "unit": ""\n}'
CV = '{\n    "ref": "REF",\n    "name": "TEST",\n    "uri": "www.eff.off",\n    "version": ""\n}'
CVT = '{\n    "cvRef": "REF",\n    "accession": "TEST:123",\n    "name": "testname",\n    "description": "",\n    "value": 99,\n    "unit": ""\n}'
ANSO = '{\n    "cvRef": "QC",\n    "accession": "QC:9999999",\n    "name": "bigwhopqc",\n    "description": "",\n    "value": "",\n    "unit": "",\n    "version": "1.2.3",\n    "uri": "file:///dev/null"\n}'
INFI = '{\n    "location": "file:///dev/null",\n    "name": "file.raw",\n    "fileFormat": {\n        "cvRef": "MS",\n        "accession": "MS:1000584",\n        "name": "mzML format"\n    },\n    "fileProperties": [\n        {\n            "cvRef": "MS",\n            "accession": "MS:1000747",\n            "name": "completion time",\n            "value": "2017-12-08-T15:38:57Z"\n        }\n    ]\n}'
META = '{\n    "inputFiles": [\n        {\n            "location": "file:///dev/null",\n            "name": "file.raw",\n            "fileFormat": {\n                "cvRef": "MS",\n                "accession": "MS:1000584",\n                "name": "mzML format"\n            },\n            "fileProperties": [\n                {\n                    "cvRef": "MS",\n                    "accession": "MS:1000747",\n                    "name": "completion time",\n                    "value": "2017-12-08-T15:38:57Z"\n                }\n            ]\n        }\n    ],\n    "analysisSoftware": [\n        {\n            "cvRef": "QC",\n            "accession": "QC:9999999",\n            "name": "bigwhopqc",\n            "version": "1.2.3",\n            "uri": "file:///dev/null"\n        }\n    ]\n}'
RUQU = '{\n    "metadata": {\n        "inputFiles": [\n            {\n                "location": "file:///dev/null",\n                "name": "file.raw",\n                "fileFormat": {\n                    "cvRef": "MS",\n                    "accession": "MS:1000584",\n                    "name": "mzML format"\n                },\n                "fileProperties": [\n                    {\n                        "cvRef": "MS",\n                        "accession": "MS:1000747",\n                        "name": "completion time",\n                        "value": "2017-12-08-T15:38:57Z"\n                    }\n                ]\n            }\n        ],\n        "analysisSoftware": [\n            {\n                "cvRef": "QC",\n                "accession": "QC:9999999",\n                "name": "bigwhopqc",\n                "version": "1.2.3",\n                "uri": "file:///dev/null"\n            }\n        ]\n    },\n    "qualityMetrics": [\n        {\n            "cvRef": "QC",\n            "accession": "QC:4000053",\n            "name": "RT duration",\n            "value": 99\n        }\n    ]\n}'
SEQU = '{\n    "metadata": {\n        "inputFiles": [\n            {\n                "location": "file:///dev/null",\n                "name": "file.raw",\n                "fileFormat": {\n                    "cvRef": "MS",\n                    "accession": "MS:1000584",\n                    "name": "mzML format"\n                },\n                "fileProperties": [\n                    {\n                        "cvRef": "MS",\n                        "accession": "MS:1000747",\n                        "name": "completion time",\n                        "value": "2017-12-08-T15:38:57Z"\n                    }\n                ]\n            }\n        ],\n        "analysisSoftware": [\n            {\n                "cvRef": "QC",\n                "accession": "QC:9999999",\n                "name": "bigwhopqc",\n                "version": "1.2.3",\n                "uri": "file:///dev/null"\n            }\n        ]\n    },\n    "qualityMetrics": [\n        {\n            "cvRef": "QC",\n            "accession": "QC:4000053",\n            "name": "RT duration",\n            "value": 99\n        }\n    ]\n}'

cvt = qc.CvParameter(cvRef="REF", accession="TEST:123", name="testname", value=99)
infi = qc.InputFile(name="file.raw",location="file:///dev/null", 
                    fileFormat=qc.CvParameter("MS", "MS:1000584", "mzML format"), 
                    fileProperties=[qc.CvParameter(cvRef="MS", 
                                                    accession="MS:1000747", 
                                                    name="completion time", 
                                                    value="2017-12-08-T15:38:57Z")
                    ])
anso = qc.AnalysisSoftware(cvRef="QC", accession="QC:9999999", name="bigwhopqc", version="1.2.3", uri="file:///dev/null")   # isn't requiring a uri a bit too much?
meta = qc.MetaDataParameters(inputFiles=[infi],analysisSoftware=[anso])
qm = qc.QualityMetric(cvRef="QC", accession="QC:4000053", name="RT duration", value=99)
rq = qc.RunQuality(metadata=meta, qualityMetrics=[qm])
sq = qc.SetQuality(metadata=meta, qualityMetrics=[qm])
cv = qc.ControlledVocabulary(ref="REF", name="TEST", uri="www.eff.off")
mzqc = qc.MzQcFile(version="0.0.11", runQualities=[rq], setQualities=[sq], controlledVocabularies=[cv]) 


class TestSerialisation:

    def test_ControlledVocabulary(self):
        assert qc.JsonSerialisable.ToJson(cv) == CV 
        
    def test_CvParameter(self):
        assert  qc.JsonSerialisable.ToJson(cvt) == CVT
        
    def test_AnalysisSoftware(self):
        assert qc.JsonSerialisable.ToJson(anso) == ANSO
        
    def test_InputFile(self):
        assert qc.JsonSerialisable.ToJson(infi) == INFI
        
    def test_MetaDataParameters(self):
        assert qc.JsonSerialisable.ToJson(meta) == META

    def test_QualityMetric(self):
        assert qc.JsonSerialisable.ToJson(qm) == QM

        #TODO more metric value types (str, float, List[float], Dict[str,float])
        
    def test_BaseQuality(self):
        pass 
        
    def test_RunQuality(self):
        assert qc.JsonSerialisable.ToJson(rq) == RUQU

    def test_SetQuality(self):
        assert qc.JsonSerialisable.ToJson(sq) == SEQU
        
    def test_MzQcFile(self):
        pass 
        
#First, serialisation should be tested separately!
class TestDeserialisation:
    def test_ControlledVocabulary(self):
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(cv)) == cv 
        assert isinstance(qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(cv)),qc.ControlledVocabulary)

    def test_CvParameter(self):
        assert  qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(cvt)) == cvt
        assert isinstance(qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(cvt)),qc.CvParameter)

    def test_AnalysisSoftware(self):
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(anso)) == anso
        assert isinstance(qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(anso)),qc.AnalysisSoftware)

    def test_InputFile(self):
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(infi)) == infi
        assert isinstance(qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(infi)),qc.InputFile)

    def test_MetaDataParameters(self):
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(meta)) == meta
        assert isinstance(qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(meta)),qc.MetaDataParameters)

    def test_QualityMetric(self):
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(qm)) == qm
        assert isinstance(qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(qm)),qc.QualityMetric)

        #TODO more metric value types (str, float, List[float], Dict[str,float])
        
    def test_BaseQuality(self):
        pass 
        
    def test_RunQuality(self):
        sdrq = (qc.RunQuality)(**qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(rq)).__dict__)
        assert  sdrq == rq
        assert isinstance(sdrq,qc.RunQuality)

    def test_SetQuality(self):
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(sq)) == sq
        assert isinstance(qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(sq)),qc.SetQuality)

    def test_MzQcFile(self):
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(mzqc)) == mzqc        
        assert isinstance(qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(mzqc)),qc.MzQcFile)

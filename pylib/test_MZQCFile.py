__author__ = 'walzer'
import pytest  # Eeeeeeverything needs to be prefixed with test ito be picked up by pytest, i.e. TestClass() and test_function()
import MZQCFile as qc

"""
Unit tests for the MZQCFile library
"""

QM_JS_1 = '{\n    "cv_ref": "QC",\n    "accession": "QC:4000053",\n    "name": "RT duration",\n    "value": 99\n}'
MP = '{\n    "file_provenance": "file.raw",\n    "input_files": [],\n    "analysis_software": [],\n    "cv_params": []\n}'
CV = '{\n    "ref": "REF",\n    "name": "TEST",\n    "uri": "www.eff.off",\n    "version": ""\n}'
CVT = '{\n    "cvRef": "REF",\n    "accession": "TEST:123",\n    "name": "testname",\n    "description": "",\n    "value": 99,\n    "unit": ""\n}'
ANSO = '{\n    "cvRef": "MS",\n    "accession": "MS:1000756",\n    "name": "",\n    "description": "",\n    "value": "",\n    "unit": "",\n    "version": "123",\n    "uri": ""\n}'
INFI = '{\n    "location": "location",\n    "name": "name",\n    "file_format": {\n        "cvRef": "MS",\n        "accession": "MS:1000584",\n        "name": "mzML format",\n        "description": "",\n        "value": "",\n        "unit": ""\n    },\n    "file_properties": [\n        {\n            "cvRef": "REF",\n            "accession": "TEST:123",\n            "name": "testname",\n            "description": "",\n            "value": 99,\n            "unit": ""\n        }\n    ]\n}'
RUQU = '{\n    "metadata": {\n        "file_provenance": "file.raw",\n        "input_files": [],\n        "analysis_software": [],\n        "cv_params": []\n    },\n    "quality_metrics": [\n        {\n            "cv_ref": "QC",\n            "accession": "QC:4000053",\n            "name": "RT duration",\n            "value": 99\n        }\n    ]\n}'
SEQU = '{\n    "metadata": {\n        "file_provenance": "file.raw",\n        "input_files": [],\n        "analysis_software": [],\n        "cv_params": []\n    },\n    "quality_metrics": [\n        {\n            "cv_ref": "QC",\n            "accession": "QC:4000053",\n            "name": "RT duration",\n            "value": 99\n        }\n    ]\n}'


class TestSerialisation:

    def test_ControlledVocabulary(self):
        cv = qc.ControlledVocabulary(ref="REF", name="TEST", uri="www.eff.off")
        assert qc.JsonSerialisable.ToJson(cv) == CV 
        
    def test_CvParameter(self):
        cvt = qc.CvParameter("REF", "TEST:123", "testname", value=99)
        assert  qc.JsonSerialisable.ToJson(cvt) == CVT
        
    def test_AnalysisSoftware(self):
        anso = qc.AnalysisSoftware("MS", "MS:1000756", "FileConverter", version="123")
        assert qc.JsonSerialisable.ToJson(anso) == ANSO
        
    def test_InputFile(self):
        infi = qc.InputFile("location", "name", qc.CvParameter("MS", "MS:1000584", "mzML format"), [qc.CvParameter("REF", "TEST:123", "testname", value=99)]) 
        assert qc.JsonSerialisable.ToJson(infi) == INFI
        
    def test_MetaDataParameters(self):
        mp = qc.MetaDataParameters("file.raw")
        assert qc.JsonSerialisable.ToJson(mp) == MP

    def test_QualityMetric(self):
        qm_1 = qc.QualityMetric("QC", "QC:4000053", "RT duration", 99)
        assert qc.JsonSerialisable.ToJson(qm_1) == QM_JS_1

        #TODO more metric value types (str, float, List[float], Dict[str,float])
        
    def test_BaseQuality(self):
        pass 
        
    def test_RunQuality(self):
        rq = qc.RunQuality(qc.MetaDataParameters("file.raw"), [qc.QualityMetric("QC", "QC:4000053", "RT duration", 99)])
        assert qc.JsonSerialisable.ToJson(rq) == RUQU

    def test_SetQuality(self):
        rq = qc.SetQuality(qc.MetaDataParameters("file.raw"), [qc.QualityMetric("QC", "QC:4000053", "RT duration", 99)])
        assert qc.JsonSerialisable.ToJson(rq) == SEQU
        
    def test_MzQcFile(self):
        pass 
        

#First, serialisation should be tested separately!
class TestDeserialisation:

    def test_ControlledVocabulary(self):
        cv = qc.ControlledVocabulary(ref="REF", name="TEST", uri="www.eff.off")
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(cv)) == cv 
        
    def test_CvParameter(self):
        cvt = qc.CvParameter("REF", "TEST:123", "testname", value=99)
        assert  qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(cvt)) == cvt
        
    def test_AnalysisSoftware(self):
        anso = qc.AnalysisSoftware("MS", "MS:1000756", "FileConverter", version="123")
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(anso)) == anso
        
    def test_InputFile(self):
        infi = qc.InputFile("location", "name", qc.CvParameter("MS", "MS:1000584", "mzML format"), [qc.CvParameter("REF", "TEST:123", "testname", value=99)]) 
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(infi)) == infi
        
    def test_MetaDataParameters(self):
        mp = qc.MetaDataParameters("file.raw")
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(mp)) == mp

    def test_QualityMetric(self):
        qm_1 = qc.QualityMetric("QC", "QC:4000053", "RT duration", 99)
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(qm_1)) == qm_1

        #TODO more metric value types (str, float, List[float], Dict[str,float])
        
    def test_BaseQuality(self):
        pass 
        
    def test_RunQuality(self):
        rq = qc.RunQuality(qc.MetaDataParameters("file.raw"), [qc.QualityMetric("QC", "QC:4000053", "RT duration", 99)])
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(rq)) == rq

    def test_SetQuality(self):
        sq = qc.SetQuality(qc.MetaDataParameters("file.raw"), [qc.QualityMetric("QC", "QC:4000053", "RT duration", 99)])
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(sq)) == sq
        
    def test_MzQcFile(self):
        rq = qc.RunQuality(qc.MetaDataParameters("file.raw"), [qc.QualityMetric("QC", "QC:4000053", "RT duration", 99)])
        sq = qc.SetQuality(qc.MetaDataParameters("file.raw"), [qc.QualityMetric("QC", "QC:4000053", "RT duration", 99)])
        cv = qc.ControlledVocabulary(ref="REF", name="TEST", uri="www.eff.off")
        mzqc = qc.MzQcFile(version="0_0_11", runQualities=[rq], setQualities=[sq], controlledVocabularies=[cv]) 
        assert qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(mzqc)) == mzqc
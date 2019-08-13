__author__ = 'walzer'
import pytest  # Eeeeeeverything needs to be prefixed with test ito be picked up by pytest, i.e. TestClass() and test_function()
from MZQC import MZQCFile as qc
from MZQC import SyntaxCheck as sy

def test_SyntaxCheck():
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
        
    syn_check = sy.SyntacticCheck()
    syn_check.validate("{ \"mzQC\": " + qc.JsonSerialisable.ToJson(mzqc) + " }")
package inspector.jqcml.model;


import javax.xml.bind.JAXBElement;
import javax.xml.bind.annotation.XmlElementDecl;
import javax.xml.bind.annotation.XmlRegistry;
import javax.xml.namespace.QName;

@XmlRegistry
public class ObjectFactory {

	@XmlElementDecl(name="RunQuality")
	public JAXBElement<QualityAssessmentList> createRunQuality(QualityAssessmentList qaList) {
        return new JAXBElement<QualityAssessmentList>(new QName("RunQuality"), QualityAssessmentList.class, qaList);
	}

	@XmlElementDecl(name="SetQuality")
	public JAXBElement<QualityAssessmentList> createSetQuality(QualityAssessmentList qaList) {
        return new JAXBElement<QualityAssessmentList>(new QName("SetQuality"), QualityAssessmentList.class, qaList);
	}
}

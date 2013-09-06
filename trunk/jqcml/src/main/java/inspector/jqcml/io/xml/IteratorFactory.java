package inspector.jqcml.io.xml;

import java.util.Iterator;
import java.util.NoSuchElementException;

import javax.xml.bind.JAXBIntrospector;
import javax.xml.bind.annotation.adapters.XmlAdapter;

import psidev.psi.tools.xxindex.index.IndexElement;

import inspector.jqcml.io.xml.index.QcMLIndexer;
import inspector.jqcml.jaxb.adapters.QualityAssessmentAdapter;
import inspector.jqcml.model.CVType;
import inspector.jqcml.model.QualityAssessment;
import inspector.jqcml.model.QualityAssessmentList;

/**
 * A factory to create an {@link Iterator} over a specific qcML (sub)object.
 */
public class IteratorFactory {

	/**
	 * Create an {@link Iterator} over all {@link CVType} objects.
	 * 
	 * @param index  The {@link QcMLIndexer} constructed from the qcML file.
	 * @param unmarshaller  The {@link QcMLUnmarshaller} used to unmarshal the qcML file.
	 * @return An iterator over all CVType objects in the given qcML file.
	 */
	public static Iterator<CVType> createCvIterator(QcMLIndexer index, QcMLUnmarshaller unmarshaller) {
		return new QcMLIterator<CVType>(index, unmarshaller, CVType.class);
	}
	
	/**
	 * Create an {@link Iterator} over all {@link QualityAssessment} objects.
	 * 
	 * @param index  The {@link QcMLIndexer} constructed from the qcML file.
	 * @param unmarshaller  The {@link QcMLUnmarshaller} used to unmarshal the qcML file.
	 * @return An iterator over all QualityAssessment objects in the given qcML file.
	 */
	public static Iterator<QualityAssessment> createQualityAssessmentIterator(QcMLIndexer index, QcMLUnmarshaller unmarshaller) {
		return new QualityAssessmentIterator(index, unmarshaller, QualityAssessmentList.class, QualityAssessment.class, new QualityAssessmentAdapter());
	}

}

/**
 * An {@link Iterator} over QualityAssessment objects in a qcML file.
 * 
 * After unmarshalling the object from the qcML file, an XmlAdapter is used to transform the object from a QualityAssessmentList to a QualityAssessment.
 * Additionally, the isSet flag is set based on the XML element name. This in particular requires a unique approach in an individual Iterator class.
 */
class QualityAssessmentIterator extends QcMLAdapterIterator<QualityAssessmentList, QualityAssessment> {

	/**
	 * Create a QualityAssessmentIterator that will iterate over QualityAssessment subobjects.
	 * 
	 * @param index  The {@link QcMLIndexer} used to index the qcML file.
	 * @param unmarshaller  The {@link QcMLUnmarshaller} to unmarshal the qcML file.
	 * @param preClass  The class type of the unmarshalled object prior to conversion with the adapter.
	 * @param postClass  The class type of the unmarshalled object after the conversion with the adapter.
	 * @param adapter  The {@link XmlAdapter} used to convert the unmarshalled object.
	 */
	public QualityAssessmentIterator(QcMLIndexer index, QcMLUnmarshaller unmarshaller,
			Class<QualityAssessmentList> preClass, Class<QualityAssessment> postClass,
			XmlAdapter<QualityAssessmentList, QualityAssessment> adapter) {
		super(index, unmarshaller, preClass, postClass, adapter);
	}
	
	@Override
	public QualityAssessment next() throws NoSuchElementException {
		logger.info("Retrieve next element from the iterator for type <{}>", clss);
		
		// get the next index element
		IndexElement elem = iterator.next().getValue();
		// read the xml snippet
		String xmlSnippet = index.readXML(elem);
		try {
			// unmarshal this element
			Object temp = unmarshaller.unmarshal(xmlSnippet);
			QualityAssessmentList qaList = (QualityAssessmentList) JAXBIntrospector.getValue(temp);
			QualityAssessment result = new QualityAssessmentAdapter().unmarshal(qaList);
			
			// set the isSet flag based on the element name
			if(unmarshaller.getIntrospector().getElementName(temp).getLocalPart().equals("SetQuality"))
				result.setSet(true);
			else
				result.setSet(false);
			
			return result;
		} catch (Exception e) {
			logger.error("Unable to manually call adapter {} for XML snippet: {}\n{}", adapter, xmlSnippet.substring(0, xmlSnippet.indexOf('>')+1), e);
			throw new IllegalStateException("Unable to manually call the XmlAdapter: " + e);
		}
	}
	
}

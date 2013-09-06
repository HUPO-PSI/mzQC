/**
 * 
 */
package inspector.jqcml.io.xml;

import java.io.File;
import java.util.Iterator;

import javax.xml.bind.JAXBIntrospector;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import inspector.jqcml.io.MzQualMLReader;
import inspector.jqcml.io.xml.index.QcMLIndexer;
import inspector.jqcml.jaxb.adapters.QualityAssessmentAdapter;
import inspector.jqcml.model.CVType;
import inspector.jqcml.model.MzQualityML;
import inspector.jqcml.model.QualityAssessment;
import inspector.jqcml.model.QualityAssessmentList;

/**
 * An MzQualML input reader which takes its input from a qcML file.
 */
public class QcMLReader implements MzQualMLReader {
	
	private static final Logger logger = LogManager.getLogger(QcMLReader.class);
	
	private File qcmlFile;
	
	private QcMLIndexer index;
	private QcMLUnmarshaller unmarshaller;
	
	/**
	 * Creates a QcMLReader by initializing a {@link QcMLUnmarshaller}.
	 * 
	 * Attention: If this default constructor is used, a subsequent call to {@link #setFile(String) setFile} is required before the Reader can be used.
	 */
	public QcMLReader() {
		unmarshaller = new QcMLUnmarshaller();
	}
	
	/**
	 * Creates a QcMLReader by initializing a {@link QcMLUnmarshaller} and initializes it to read from the file with the specified file name.
	 * 
	 * @param fileName  The file name from the file that will be read.
	 */
	public QcMLReader(String fileName) {
		this();
		
		setFile(fileName);
	}

	public void setFile(String fileName) {
		// check whether the file name is valid
		if(fileName == null) {
			logger.error("Invalid file name <null>");
			throw new NullPointerException("Invalid file name");
		}
		
		File file = new File(fileName);
		
		// check whether the file exists
		if(!file.exists()) {
			logger.error("The qcML file <{}> does not exist", file.getAbsolutePath());
			throw new IllegalArgumentException("The qcML file to read does not exist: " + file.getAbsolutePath());
		}

		this.qcmlFile = file;
		logger.info("Set qcML file <{}>", qcmlFile.getAbsoluteFile());

		// create the XML file index
		index = new QcMLIndexer(qcmlFile);
	}

	public MzQualityML getMzQualityML() {
		try {
			return unmarshaller.unmarshal(qcmlFile);
		} catch(IllegalStateException e) {
			return null;
		}
	}

	public CVType getCV(String id) {
		// retrieve the XML snippet pertaining to this CVType
		String xmlSnippet = index.getXMLSnippet(CVType.class, id);
		
		// unmarshal the XML snippet
		if(xmlSnippet != null)
			return unmarshaller.unmarshal(xmlSnippet, CVType.class);
		else
			return null;
	}
	
	public Iterator<CVType> getCVIterator() {
		return IteratorFactory.createCvIterator(index, unmarshaller);
	}

	public QualityAssessment getQualityAssessment(String id) {
		// retrieve the XML snippet
		String xmlSnippet = index.getXMLSnippet(QualityAssessment.class, id);
		
		// unmarshal the XML snippet if it exists
		if(xmlSnippet != null) {
			try {
				// unmarshal to a QualityAssessmentList, and subsequently call the QualityAssessmentAdapter manually
				// manually calling the adapter is required because XmlJavaTypeAdapter can't be used on XmlRootElement
				// see: https://java.net/jira/browse/JAXB-117
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
				logger.error("Unable to manually call the QualityAssessmentAdapter for XML snippet: {}\n{}", xmlSnippet.substring(0, xmlSnippet.indexOf('>')+1), e);
				throw new IllegalStateException("Unable to manually call the QualityAssessmentAdapter: " + e);
			}
		}
		
		// no RunQuality or SetQuality with the specified ID found
		return null;
	}
	
	public Iterator<QualityAssessment> getQualityAssessmentIterator() {
		return IteratorFactory.createQualityAssessmentIterator(index, unmarshaller);
	}

}

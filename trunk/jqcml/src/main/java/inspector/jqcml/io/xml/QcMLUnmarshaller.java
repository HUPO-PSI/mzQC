package inspector.jqcml.io.xml;

import inspector.jqcml.model.MzQualityML;

import java.io.File;
import java.io.StringReader;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.JAXBIntrospector;
import javax.xml.bind.Unmarshaller;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * A JAXB {@link Unmarshaller} specified with the required context to deserialize a qcML file into Java objects.
 */
public class QcMLUnmarshaller {

	private static final Logger logger = LogManager.getLogger(QcMLUnmarshaller.class);
	
	private Unmarshaller unmarshaller;
	private JAXBIntrospector introspector;
	
	/**
	 * Create a JAXB {@link Unmarshaller} using the required {@link JAXBContext} required for unmarshalling a qcML file.
	 */
	public QcMLUnmarshaller() {
		// create the JAXB Unmarshaller
		logger.info("Create the JAXB Unmarshaller");
		
		try {
			unmarshaller = QcMLJAXBContext.INSTANCE.context.createUnmarshaller();
			introspector = QcMLJAXBContext.INSTANCE.context.createJAXBIntrospector();
		} catch (JAXBException e) {
			logger.error("Error while creating the JAXB Unmarshaller: {}", e);
			throw new IllegalStateException("Could not create the qcML Unmarshaller: " + e);
		}
	}
	
	public JAXBIntrospector getIntrospector() {
		return introspector;
	}

	public void setIntrospector(JAXBIntrospector introspector) {
		this.introspector = introspector;
	}

	/**
	 * Returns the full {@link MzQualityML} object specified by the given file.
	 * 
	 * Warning: Because a single MzQualityML object can contain several QualityAssessments,
	 * only use this method when you are certain the requested MzQualityML object won't be too big,
	 * in order to prevent running out of main memory.
	 * 
	 * @param file  The file that will be unmarshalled. This should be a valid file.
	 * @return The {@link MzQualityML} object unmarshalled from the given file.
	 */
	public MzQualityML unmarshal(File file) {
		logger.info("Unmarshal full file <{}>", file.getAbsolutePath());
		
		try {
			MzQualityML result = (MzQualityML) unmarshaller.unmarshal(file);
			result.setFileName(file.getAbsolutePath());

			return result;
			
		} catch (JAXBException e) {
			logger.error("Error while unmarshalling file <{}>: {}", file.getAbsolutePath(), e);
			throw new IllegalStateException("Error while unmarshalling file <" + file.getAbsolutePath() + ">: " + e);
		}
	}
	
	/**
	 * Returns the specified object from the given XML snippet.
	 * 
	 * @param xmlSnippet  The XML snippet that will be unmarshalled. This should be valid XML content.
	 * @param type  The class of the object unmarshalled from the given XML snippet.
	 * @return The object unmarshalled from the given XML snippet.
	 */
	public <T> T unmarshal(String xmlSnippet, Class<T> type) {
		logger.info("Unmarshal type <{}> from XML snippet: {}", type, xmlSnippet.substring(0, xmlSnippet.indexOf('>')+1));
		
		try {
			Object temp = unmarshaller.unmarshal(new StringReader(xmlSnippet));
			T result = type.cast(JAXBIntrospector.getValue(temp));
			
			return result;
			
		} catch (JAXBException e) {
			logger.error("Error while unmarshalling XML snippet {}\n{}", xmlSnippet.substring(0, xmlSnippet.indexOf('>')+1), e);
			throw new IllegalStateException("Error while unmarshalling XML snippet " + xmlSnippet.substring(0, xmlSnippet.indexOf('>')+1) + ": " + e);
		}
	}
	
	/**
	 * Returns the specified object from the given XML snippet.
	 * 
	 * The return value is a JAXB element. This allows f.e. retrieving the element name and value using the {@link JAXBIntrospector}.
	 * 
	 * @param xmlSnippet  The XML snippet that will be unmarshalled. This should be valid XML content.
	 * @return The object unmarshalled from the given XML snippet.
	 */
	public Object unmarshal(String xmlSnippet) {
		logger.info("Unmarshal general object from XML snippet: {}", xmlSnippet.substring(0, xmlSnippet.indexOf('>')+1));
		
		try {
			return unmarshaller.unmarshal(new StringReader(xmlSnippet));
			
		} catch (JAXBException e) {
			logger.error("Error while unmarshalling XML snippet {}\n{}", xmlSnippet.substring(0, xmlSnippet.indexOf('>')+1), e);
			throw new IllegalStateException("Error while unmarshalling XML snippet " + xmlSnippet.substring(0, xmlSnippet.indexOf('>')+1) + ": " + e);
		}
	}

}

package inspector.jqcml.io.xml.index;

import inspector.jqcml.model.CVType;
import inspector.jqcml.model.QualityAssessment;

import java.io.File;
import java.io.IOException;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import psidev.psi.tools.xxindex.SimpleXmlElementExtractor;
import psidev.psi.tools.xxindex.StandardXpathAccess;
import psidev.psi.tools.xxindex.XmlElementExtractor;
import psidev.psi.tools.xxindex.index.IndexElement;
import psidev.psi.tools.xxindex.index.XpathIndex;

public class QcMLIndexer {
	
	private static final Logger logger = LogManager.getLogger(QcMLIndexer.class);
	
	private File qcmlFile;
	
	private StandardXpathAccess access;
	private XmlElementExtractor xmlExtractor;
	private XpathIndex index;
	
	@SuppressWarnings("rawtypes")
	private Map<Class, Map<String, IndexElement>> idMap;

	private static final Set<String> indexed_xpaths = getIndexedXPaths();

	/**
	 * Returns a set containing all XPath node expressions that need to be stored in the index.
	 * 
	 * These node expressions refer to the RunQuality, SetQuality and CVList objects.
	 * 
	 * @return A set containing all XPath node expressions that need to be stored in the index.
	 */
	private static Set<String> getIndexedXPaths() {
		Set<String> xpathsToIndex = new HashSet<String>();

		// index all RunQuality, SetQuality and CVList
		xpathsToIndex.add("/MzQualityML/RunQuality");
		xpathsToIndex.add("/MzQualityML/SetQuality");
		xpathsToIndex.add("/MzQualityML/cvList/cv");

		// finally make the set unmodifiable
		xpathsToIndex = Collections.unmodifiableSet(xpathsToIndex);

		return xpathsToIndex;
	}
	
	/**	A pattern for extracting an ID attribute from an XML element. */
	private static Pattern ID_PATTERN = Pattern.compile("\\sid\\s*=\\s*['\"]([^'\"]*)['\"]", Pattern.CASE_INSENSITIVE);

	/**
	 * Creates an XXIndex containing offsets for all RunQualitys, SetQualitys and CVLists.
	 * 
	 * @param file  The qcML file for which the index is created.
	 */
	@SuppressWarnings("rawtypes")
	public QcMLIndexer(File file) {
		try {
			logger.info("Create XXIndex");
			
			qcmlFile = file;

			// generate an XXIndex for the QualityAssessments (RunQuality & SetQuality) and CVList
			access = new StandardXpathAccess(qcmlFile, indexed_xpaths);
			
			// create an XML element extractor
            xmlExtractor = new SimpleXmlElementExtractor();
            String encoding = xmlExtractor.detectFileEncoding(qcmlFile.toURI().toURL());
            if(encoding != null) {
            	logger.info("XML file encoding: {}", encoding);
                xmlExtractor.setEncoding(encoding);
            }
			
            // get the index
			index = access.getIndex();
			
			// generate ID mappings for all index elements
			idMap = new HashMap<Class, Map<String, IndexElement>>();
			createIDMappings();
			
		} catch (IOException e) {
			logger.error("Could not generate an index for qcML file <{}>: {}", qcmlFile.getAbsolutePath(), e);
			throw new IllegalStateException("Could not generate an index for qcML file: " + qcmlFile.getAbsolutePath());
		}
	}
	
	/**
	 * Returns the ID mappings for the specified class type.
	 * 
	 * @param clss  The class type for which the ID mappings are returned.
	 * @return The ID mappings for the specified class type.
	 */
	public Map<String, IndexElement> getIDMapping(@SuppressWarnings("rawtypes") Class clss) {
		return idMap.get(clss);
	}
	
	/**
	 * Creates ID mappings for all indexed XML elements.
	 * 
	 * The indexed XML elements are RunQuality, SetQuality and CVList, which should all have an ID attribute.
	 * 
	 * @throws IOException
	 */
	private void createIDMappings() throws IOException {
		logger.info("Create ID mappings");
		
		// create ID mappings for all types of indexed elements
		for(String xpath : indexed_xpaths) {
			@SuppressWarnings("rawtypes")
			Class cls = xpathToClass(xpath);
			List<IndexElement> elements = index.getElements(xpath);
			// create ID mappings for all separate elements
			for(IndexElement elem : elements) {
				// get the start tag (including all the attributes, and hence the ID)
				String xmlSnippet = access.getStartTag(elem);
				String id = extractIDFromRawXML(xmlSnippet);
				// combine the XPath expression with the ID to create a unique hash key
				if(id != null) {
					// initialize a HashMap for this class if it doesn't exist yet
					if(idMap.get(cls) == null)
						idMap.put(cls, new LinkedHashMap<String, IndexElement>());
					// store the new mapping
					idMap.get(cls).put(id, elem);
				} else {
					logger.error("Error initializing ID mappings: No ID attribute found for element: {}", xmlSnippet);
	                throw new IllegalStateException("Error initializing ID mappings: No ID attribute found for element: " + xmlSnippet);
	            }
			}
		}
	}
	
	/**
	 * Gives the class type based on XPath node expressions.
	 * 
	 * @param xpath  The XPath node expression for which we want the class type.
	 * @return The class type if it corresponds to an indexed XPath node expression, <code>null</code> else.
	 */
	private @SuppressWarnings("rawtypes") Class xpathToClass(String xpath) {
		switch(xpath) {
			case "/MzQualityML/RunQuality":
				return QualityAssessment.class;
			case "/MzQualityML/SetQuality":
				return QualityAssessment.class;
			case "/MzQualityML/cvList/cv":
				return CVType.class;
			default:
				return null;
		}
	}
	
	/**
	 * Extracts the ID attribute from an XML element.
	 * 
	 * @param xml  The opening tag (containing the attributes) from the XML element.
	 * @return The ID attribute from the given XML element if found, <code>null</code> otherwise.
	 */
	private String extractIDFromRawXML(String xml) {
		Matcher match = ID_PATTERN.matcher(xml);
        if(match.find())
            return match.group(1);
        else
        	return null;
	}
	
	/**
	 * Returns the IndexElement which describes an indexed XML element specified by the given class and ID attribute.
	 * 
	 * @param cls  The class to which the XML element will be mapped.
	 * @param id  The XML ID attribute.
	 * @return The IndexElement corresponding to the specified class with the specified ID attribute if found, <code>null</code> otherwise.
	 */
	public String getXMLSnippet(@SuppressWarnings("rawtypes") Class cls, String id) {
		Map<String, IndexElement> mapping = idMap.get(cls);
		if(mapping != null) {
			IndexElement elem = mapping.get(id);
			if(elem != null)
	            return readXML(elem);
			else
				return null;
		}
		else
			return null;
	}
	
	// copied from jmzML
	public String readXML(IndexElement byteRange) {
        return readXML(byteRange, 0);
    }

	// copied from jmzML
    public String readXML(IndexElement byteRange, int maxChars) {
        try {
            if (byteRange != null) {
                long stop; // where we will stop reading
                long limitedStop = byteRange.getStart() + maxChars; // the potential end-point of reading
                // if a limit was specified and the XML element length is longer
                // than the limit, we only read up to the provided limit
                if (maxChars > 0 && byteRange.getStop() > limitedStop) {
                    stop = limitedStop;
                } else { // otherwise we will read up to the end of the XML element
                    stop = byteRange.getStop();
                }
                return xmlExtractor.readString(byteRange.getStart(), stop, qcmlFile);
            } else {
                throw new IllegalStateException("Attempting to read NULL ByteRange");
            }
        } catch (IOException e) {
            logger.error("readXML", e);
            throw new IllegalStateException("Could not extract XML from file: " + qcmlFile);
        }
    }
}

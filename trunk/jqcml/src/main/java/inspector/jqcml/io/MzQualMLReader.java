package inspector.jqcml.io;

import java.util.Iterator;

import inspector.jqcml.model.CVType;
import inspector.jqcml.model.MzQualityML;
import inspector.jqcml.model.QualityAssessment;

/**
 * An MzQualML input reader.
 */
public interface MzQualMLReader {
	
	/**
	 * Sets the file from which the Reader will read.
	 * 
	 * @param fileName  The file name of the file from which the Reader will read.
	 */
	public void setFile(String fileName);
	
	/**
	 * Returns the full {@link MzQualityML} object specified by the current file from which the Reader reads.
	 * 
	 * Warning: Because a single MzQualityML object can contain several QualityAssessments,
	 * only use this method when you are certain the requested MzQualityML object won't be too big,
	 * in order to prevent running out of main memory.
	 * 
	 * @return The {@link MzQualityML} object specified by this reader if found, else <code>null</code>.
	 */
	public MzQualityML getMzQualityML();
	
	/**
	 * Returns the {@link CVType} object with the given id.
	 * 
	 * @param id  The identifier of the requested CVType object.
	 * @return The {@link CVType} object specified by the given id if present, else <code>null</code>.
	 */
	public CVType getCV(String id);
	
	/**
	 * Returns an {@link Iterator} over all {@link CVType} objects.
	 * 
	 * @return An {@link Iterator} over all {@link CVType} objects.
	 */
	public Iterator<CVType> getCVIterator();
	
	/**
	 * Returns the {@link QualityAssessment} object with the given id.
	 * 
	 * @param id  The identifier of the requested QualityAssessment object.
	 * @return The {@link QualityAssessment} object specified by the given id if present, else <code>null</code>.
	 */
	public QualityAssessment getQualityAssessment(String id);
	
	/**
	 * Returns an {@link Iterator} over all {@link QualityAssessment} objects.
	 * 
	 * @return An {@link Iterator} over all {@link QualityAssessment} objects.
	 */
	public Iterator<QualityAssessment> getQualityAssessmentIterator();
}

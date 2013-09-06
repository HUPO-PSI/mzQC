package inspector.jqcml.model;

import inspector.jqcml.jaxb.adapters.CVListAdapter;
import inspector.jqcml.jaxb.adapters.RunQualityAdapter;
import inspector.jqcml.jaxb.adapters.SetQualityAdapter;

import java.util.LinkedHashMap;
import java.util.Map;

import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlTransient;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;

import org.eclipse.persistence.oxm.annotations.XmlPath;
/**
 * The Quality file XML root element containing several QualityAssessments to runs and an optional QualityAssessment to the whole set.
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlRootElement(name="MzQualityML")
@XmlType(name="MzQualityMLType", propOrder={ "runQuality", "setQuality", "cvList" })
public class MzQualityML {
	
	@XmlTransient
	private String fileName;
	@XmlJavaTypeAdapter(RunQualityAdapter.class)
	@XmlPath(".")
	// key=ID, value=QA
	private Map<String, QualityAssessment> runQuality;
	@XmlJavaTypeAdapter(SetQualityAdapter.class)
	@XmlPath(".")
	// key=ID, value=QA
	private Map<String, QualityAssessment> setQuality;
	/** The list of cvParams referenced by the QualityParameters. */
	@XmlJavaTypeAdapter(CVListAdapter.class)
	@XmlElement(name="cvList", required=true)
	private Map<String, CVType> cvList;
	
	public MzQualityML() {
		this.runQuality = new LinkedHashMap<String, QualityAssessment>();
		this.setQuality = new LinkedHashMap<String, QualityAssessment>();
		this.cvList = new LinkedHashMap<String, CVType>();
	}
	
	/**
	 * @param fileName  The file name from which this MzQualityML object is (un)marshalled.
	 */
	public MzQualityML(String fileName) {
		this();
		
		setFileName(fileName);
	}

	public String getFileName() {
		return fileName;
	}

	public void setFileName(String fileName) {
		this.fileName = fileName;
	}

	public Map<String, QualityAssessment> getRunQualityList() {
		return runQuality;
	}
	
	/**
	 * Returns the QualityAssessment of a RunQuality specified by the given ID.
	 * 
	 * @param id  The ID of the requested QualityAssessment
	 * @return The QualityAssessment specified by the given ID if this QualityAssessment is present, <code>null</code> otherwise
	 */
	public QualityAssessment getRunQuality(String id) {
		return getRunQualityList().get(id);
	}
	
	/**
	 * Adds a given QualityAssessment as an additional RunQuality.
	 * 
	 * If a QualityAssessment with the same ID was already present, the old QualityAssessment is replaced by the given QualityAssessment.
	 * 
	 * @param qa  The given QualityAssessment
	 */
	public void addRunQuality(QualityAssessment qa) {
		this.runQuality.put(qa.getId(), qa);
	}

	public Map<String, QualityAssessment> getSetQualityList() {
		return setQuality;
	}
	
	/**
	 * Returns the QualityAssessment of a SetQuality specified by the given ID.
	 * 
	 * @param id  The ID of the requested QualityAssessment
	 * @return The QualityAssessment specified by the given ID if this QualityAssessment is present, <code>null</code> otherwise
	 */
	public QualityAssessment getSetQuality(String id) {
		return getSetQualityList().get(id);
	}
	
	/**
	 * Adds a given QualityAssessment as an additional SetQuality.
	 * 
	 * If a QualityAssessment with the same ID was already present, the old QualityAssessment is replaced by the given QualityAssessment.
	 * 
	 * @param qa  The given QualityAssessment
	 */
	public void addSetQuality(QualityAssessment qa) {
		this.setQuality.put(qa.getId(), qa);
	}

	public Map<String, CVType> getCvList() {
		return cvList;
	}
	
	/**
	 * Returns the CVType specified by the given ID.
	 * 
	 * @param id  The ID of the requested CVType
	 * @return The CVType specified by the given ID if this CVType is present, <code>null</code> otherwise
	 */
	public CVType getCv(String id) {
		return getCvList().get(id);
	}
	
	/**
	 * Adds a given CVType to the cvList.
	 * 
	 * If a CVType with the same ID was already present, the old CVType is replaced by the given CVType.
	 * 
	 * @param cv  The given CVType
	 */
	public void addCv(CVType cv) {
		this.cvList.put(cv.getId(), cv);
	}
	
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append("MzQualityML");
		
		for(QualityAssessment qa : getRunQualityList().values())
			sb.append("\n" + qa);
		for(QualityAssessment qa : getSetQualityList().values())
			sb.append("\n" + qa);
		for(CVType cv : getCvList().values())
			sb.append("\n" + cv);
				
		return sb.toString();
	}

}

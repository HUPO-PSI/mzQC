package inspector.jqcml.model;

import inspector.jqcml.jaxb.adapters.QualityAssessmentAdapter;

import java.util.HashMap;
import java.util.Map;

import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;


/**
 * The derived Type for QualityParameter container of a run/set.
 */
@XmlJavaTypeAdapter(QualityAssessmentAdapter.class)
public class QualityAssessment {
	
	private String id;
    private Map<String, QualityParameter> parameterList;
    private Map<String, AttachmentParameter> attachmentList;
    private boolean isSet;
    
    public QualityAssessment() {
    	this.parameterList = new HashMap<String, QualityParameter>();
    	this.attachmentList = new HashMap<String, AttachmentParameter>();
    }
	
	public QualityAssessment(String id) {
		this();
		
		setId(id);
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public Map<String, QualityParameter> getQualityParameterList() {
		return parameterList;
	}

	/**
	 * Returns the QualityParameter specified by the given id.
	 * 
	 * @param id  The id of the desired QualityParameter
	 * @return The QualityParameter specified by the given id if this QualityParameter is present, <code>null</code> otherwise
	 */
	public QualityParameter getQualityParameter(String id) {
		return parameterList.get(id);
	}

	/**
	 * Adds a given QualityParameter to this QualityAssessment.
	 * 
	 * If a QualityParameter with the same id was already present, the old QualityParameter is replaced by the given QualityParameter.
	 * 
	 * @param param  The given QualityParameter
	 */
	public void addQualityParameter(QualityParameter param) {
		parameterList.put(param.getId(), param);
	}

	public Map<String, AttachmentParameter> getAttachmentList() {
		return attachmentList;
	}

	/**
	 * Returns the AttachmentParameter specified by the given id.
	 * 
	 * @param id  The id of the desired AttachmentParameter
	 * @return The AttachmentParameter specified by the given id if this AttachmentParameter is present, <code>null</code> otherwise
	 */
	public AttachmentParameter getAttachmentParameter(String id) {
		return attachmentList.get(id);
	}

	/**
	 * Adds a given AttachmentParameter to this QualityAssessment.
	 * 
	 * If an AttachmentParameter with the same id was already present, the old AttachmentParameter is replaced by the given AttachmentParameter.
	 * 
	 * @param param  The given AttachmentParameter
	 */
	public void addAttachmentParameter(AttachmentParameter param) {
		attachmentList.put(param.getId(), param);
	}

	public boolean isSet() {
		return isSet;
	}

	public void setSet(boolean isSet) {
		this.isSet = isSet;
	}
	
	public String toString() {
		StringBuilder sb = new StringBuilder();
		if(!isSet)
			sb.append("RunQuality id=\"" + getId() + "\"");
		else
			sb.append("SetQuality id=\"" + getId() + "\"");

		for(QualityParameter qp : parameterList.values())
			sb.append("\n" + qp);
		for(AttachmentParameter ap : attachmentList.values())
			sb.append("\n" + ap);
		
		return sb.toString();
	}

}

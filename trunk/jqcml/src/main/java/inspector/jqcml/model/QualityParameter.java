package inspector.jqcml.model;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

import org.eclipse.persistence.oxm.annotations.XmlPath;

/**
 * A quality parameter contains a value and a cv, as well as a optional threshold element.
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlRootElement(name="QualityParameter")
@XmlType(name="QualityParameter", propOrder={ "name", "id", "cvRef", "accession", "value", "unitCvRef", "unitAccession", "unitName", "flag", "thresholdFileName" })
public class QualityParameter extends CVParameter {
	
	@XmlAttribute
	private Boolean flag;
	//TODO: move to individual class
	@XmlPath("threshold/threshold_filename/text()")
	private String thresholdFileName;
	
	public QualityParameter() {
		super();
	}
	
	public QualityParameter(String name, CVType cvRef, String id) {
		super(name, cvRef);
		
		setId(id);
	}	
	
	public String getId() {
		return id;
	}
	public void setId(String id) {
		this.id = id;
	}
	public Boolean isFlag() {
		return flag;
	}
	public void setFlag(Boolean flag) {
		this.flag = flag;
	}
	public String getThresholdFileName() {
		return thresholdFileName;
	}
	public void setThresholdFileName(String threshold_filename) {
		this.thresholdFileName = threshold_filename;
	}
	
	public String toString() {
		return "QualityParameter id=\"" + getId() + "\" name=\"" + getName() + "\" value=\"" + getValue() + "\"";
	}
	
	

}

package inspector.jqcml.model;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlID;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

/**
 * A source controlled vocabulary from which cvParams will be obtained.
 * These are describing the QualityParameters with a given semantic. (FWHM, TIC, TICsetlimit, ..., jpeg, ...)
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlRootElement(name="cv")
@XmlType(name="cvType")
public class CVType {
	
	/** The full name of the CV. */
	@XmlAttribute(required=true)
	private String fullName;
	/** The version of the CV. */
	@XmlAttribute
	private String version;
	/** The URI of the source CV. */
	@XmlAttribute(required=true)
	private String uri;
	/** The unique identifier of this cv within the document to be referenced by cvParam elements. */
	@XmlAttribute(required=true)
	@XmlID
	private String id;
	
	public CVType() {
		// do nothing
	}
	
	public CVType(String fullName, String uri, String id) {
		setFullName(fullName);
		setUri(uri);
		setId(id);
	}

	public String getFullName() {
		return fullName;
	}

	public void setFullName(String fullName) {
		this.fullName = fullName;
	}

	public String getVersion() {
		return version;
	}

	public void setVersion(String version) {
		this.version = version;
	}

	public String getUri() {
		return uri;
	}

	public void setUri(String uri) {
		this.uri = uri;
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}
	
	public String toString() {
		return "CV id=\"" + getId() + "\" fullname=\"" + getFullName() + "\"";
	}

}

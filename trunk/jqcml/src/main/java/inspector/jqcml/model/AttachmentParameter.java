package inspector.jqcml.model;

import inspector.jqcml.jaxb.adapters.TableAttachmentAdapter;

import javax.xml.bind.DatatypeConverter;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlIDREF;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;

import org.eclipse.persistence.oxm.annotations.XmlPath;

/**
 * A single attachment containing binary data or a table.
 * The cvParam contains the description fitting to the referenced quality parameter.
 * The MIME type is given in unit of the cv.
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlRootElement(name="Attachment")
@XmlType(name="Attachment")
public class AttachmentParameter extends CVParameter {
	
	@XmlAttribute
	//TODO: the ID reference is currently disabled because of an NPE when initializing the JAXBContext or unmarshalling
	// therefore we store the qualityParameterRef as a string
	// if the user wants to obtain the QualityParameter, he can do this himself by using this key
	private String qualityParameterRef;
	//TODO: obsolete
	//@XmlIDREF
	// private QualityParameter qualityParameterRef;
	@XmlElement
	private byte[] binary;
	@XmlJavaTypeAdapter(TableAttachmentAdapter.class)
	@XmlPath("table")
	private TableAttachment table;
	//TODO: obsolete
	//private TableStringAttachment table;
	
	public AttachmentParameter() {
		super();
	}
	
	public AttachmentParameter(String name, CVType cvRef) {
		super(name, cvRef);
	}

	public String getQualityParameterRef() {
		return qualityParameterRef;
	}

	public void setQualityParameterRef(String qualityParameterRef) {
		this.qualityParameterRef = qualityParameterRef;
	}

	public byte[] getBinary() {
		return binary;
	}
	
	public String getBinaryBase64() {
		return DatatypeConverter.printBase64Binary(getBinary());
	}

	public void setBinary(byte[] binary) {
		this.binary = binary;
	}
	
	public void setBinaryBase64(String base64) {
		setBinary(DatatypeConverter.parseBase64Binary(base64));
	}
	
	public TableAttachment getTable() {
		return table;
	}
	
	public void setTable(TableAttachment table) {
		this.table = table;
	}
	
	public String toString() {
		return "AttachmentParameter id=\"" + getId() + "\" name=\"" + getName() + "\"";
	}

}

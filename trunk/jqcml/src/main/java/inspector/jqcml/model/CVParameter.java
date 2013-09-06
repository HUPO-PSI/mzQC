package inspector.jqcml.model;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlSeeAlso;
import javax.xml.bind.annotation.XmlTransient;
import javax.xml.bind.annotation.XmlType;

/**
 * A single entry from an ontology or a controlled vocabulary.
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name="CVParameter")
@XmlTransient
@XmlSeeAlso( { QualityParameter.class, AttachmentParameter.class } )
public class CVParameter extends AbstractParameter {
	
	/** A reference to the cv element from which this term originates. */
	// EclipseLink MOXy contains a bug when using @XmlIDREF with @XmlAdapter
	// see issue: https://bugs.eclipse.org/bugs/show_bug.cgi?id=353596
	// therefore we store the the ID of the CVType as a string
	// if the user wants to obtain the CVType, he can do this himself by using this key
	@XmlAttribute(required=true)
    @XmlSchemaType(name="IDREF")
	protected String cvRef;
	//TODO: obsolete
	//@XmlIDREF
	//protected CVType cvRef;
	/** The accession or ID number of this CV term in the source CV. */
	@XmlAttribute(name="accession", required=true)
	protected String accession;
	
	public CVParameter() {
		super();
	}
	
	public CVParameter(String name, CVType cvRef) {
		setName(name);
		setCvRef(cvRef.getId());
	}

	public String getCvRef() {
		return cvRef;
	}

	public void setCvRef(String cvID) {
		this.cvRef = cvID;
	}

	public String getAccession() {
		return accession;
	}

	public void setAccession(String accession) {
		this.accession = accession;
	}
	
	public String toString() {
		return "CVParameter id=\"" + getId() + "\" name=\"" + getName() + "\"";
	}

}

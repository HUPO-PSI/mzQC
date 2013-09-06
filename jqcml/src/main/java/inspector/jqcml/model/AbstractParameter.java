package inspector.jqcml.model;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlID;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlSeeAlso;
import javax.xml.bind.annotation.XmlTransient;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.CollapsedStringAdapter;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;

/**
 * Abstract entity allowing either cvParam or userParam to be referenced in other schemas.
 *
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name="AbstractParameter")
@XmlTransient
@XmlSeeAlso( { CVParameter.class } )
public abstract class AbstractParameter {
	
	/** The name of the parameter. */
	@XmlAttribute(required=true)
	protected String name;
	/** The user-entered value of the parameter, e.g. ppm value of accuracy or the file name if CV is a mime type. */
	@XmlAttribute
	protected String value;
	/** An accession number identifying the unit within the OBO foundry Unit CV. */
	@XmlAttribute
	protected String unitAccession;
	/** The name of the unit. */
	@XmlAttribute
	protected String unitName;
	@XmlAttribute(name="ID", required=true)
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
	//TODO: including the XmlID tag results in an NPE when creating the JAXBContext
	//TODO: verify why this happens and how to fix it
	//@XmlID
    @XmlSchemaType(name="ID")	
	protected String id;
	/** If a unit term is referenced, this attribute must refer to the CV 'id' attribute defined in the cvList in this file. */
	// EclipseLink MOXy contains a bug when using @XmlIDREF with @XmlAdapter
	// see issue: https://bugs.eclipse.org/bugs/show_bug.cgi?id=353596
	// therefore we store the the ID of the CVType as a string
	// if the user wants to obtain the CVType, he can do this himself by using this key
	@XmlAttribute
	protected String unitCvRef;
	//TODO: obsolete
	//@XmlIDREF
	//protected CVType unitCvRef;
	
	public AbstractParameter() {
		// do nothing
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getValue() {
		return value;
	}

	public void setValue(String value) {
		this.value = value;
	}

	public String getUnitAccession() {
		return unitAccession;
	}

	public void setUnitAccession(String unitAccession) {
		this.unitAccession = unitAccession;
	}

	public String getUnitName() {
		return unitName;
	}

	public void setUnitName(String unitName) {
		this.unitName = unitName;
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getUnitCvRef() {
		return unitCvRef;
	}

	public void setUnitCvRef(String cvID) {
		this.unitCvRef = cvID;
	}
	
	public String toString() {
		return "AbstractParameter id=\"" + getId() + "\" name=\"" + getName() + "\"";
	}

}

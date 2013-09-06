package inspector.jqcml.model;



import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElementRef;
import javax.xml.bind.annotation.XmlID;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlTransient;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.CollapsedStringAdapter;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name="QualityAssessmentType")
public class QualityAssessmentList implements Iterable<CVParameter> {
	
	@XmlAttribute(name="ID", required=true)
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
	@XmlID
	@XmlSchemaType(name="ID")
	private String id;
    @XmlElementRef
	private List<CVParameter> paramList;
    @XmlTransient
    private boolean isSet;
	
	public QualityAssessmentList() {
		paramList = new ArrayList<CVParameter>();
		
		// default: true
		// in case of a RunQuality, the RunQualityAdapter sets this to false
		setSet(true);
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}
	
	public List<CVParameter> getParameterList() {
		return paramList;
	}
	
	public void addParameter(CVParameter param) {
		paramList.add(param);
	}
	
	public void addParameterList(List<CVParameter> list) {
		paramList.addAll(list);
	}

	public Iterator<CVParameter> iterator() {
		return paramList.iterator();
	}

	public boolean isSet() {
		return isSet;
	}

	public void setSet(boolean isSet) {
		this.isSet = isSet;
	}
	
}

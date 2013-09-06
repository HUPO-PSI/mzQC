package inspector.jqcml.jaxb.adapters;

import inspector.jqcml.model.QualityAssessment;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.XmlAdapter;

public class SetQualityAdapter extends XmlAdapter<SetQualityList, Map<String, QualityAssessment>> {
	
	protected final boolean IS_SET = true;

	@Override
	public SetQualityList marshal(Map<String, QualityAssessment> arg0) throws Exception {
		return new SetQualityList(arg0.values());
	}

	@Override
	public Map<String, QualityAssessment> unmarshal(SetQualityList arg0) throws Exception {
		Map<String, QualityAssessment> qaMap = new HashMap<String, QualityAssessment>(arg0.size());
		for(QualityAssessment qa : arg0) {
			// set Run/SetQuality flag
			qa.setSet(IS_SET);
			// add it to the map
			qaMap.put(qa.getId(), qa);
		}
		
		return qaMap;
	}

}

@XmlType(name="SetQualityAssessmentType")
class SetQualityList implements Iterable<QualityAssessment> {
	
	@XmlElement(name="SetQuality", required=true)
	private List<QualityAssessment> qaList;
	
	public SetQualityList() {
		qaList = new ArrayList<QualityAssessment>();
	}
	
	public SetQualityList(Collection<QualityAssessment> qaCollection) {
		this.qaList = new ArrayList<QualityAssessment>(qaCollection);
		Collections.sort(this.qaList, new QualityAssessmentIDComparator());
	}
	
	public void addElement(QualityAssessment elem) {
		qaList.add(elem);
	}
	
	public int size() {
		return qaList.size();
	}

	public Iterator<QualityAssessment> iterator() {
		return qaList.iterator();
	}
	
	
}

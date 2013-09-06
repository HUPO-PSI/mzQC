package inspector.jqcml.jaxb.adapters;

import inspector.jqcml.model.CVType;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.XmlAdapter;

public class CVListAdapter extends XmlAdapter<CVList, Map<String, CVType>> {

	@Override
	public CVList marshal(Map<String, CVType> arg0) throws Exception {
		if(arg0.size() > 0)
			return new CVList(arg0.values());
		else
			return null;
	}

	@Override
	public Map<String, CVType> unmarshal(CVList arg0) throws Exception {
		Map<String, CVType> cvMap = new HashMap<String, CVType>(arg0.size());
		for(CVType cv : arg0)
			cvMap.put(cv.getId(), cv);
		
		return cvMap;
	}

}

@XmlType(name="CVListType")
class CVList implements Iterable<CVType> {
	
	@XmlElement(name="cv", required=true)
	private Collection<CVType> cvList;
	
	public CVList() {
		cvList = new ArrayList<CVType>();
	}
	
	public CVList(Collection<CVType> cvList) {
		this.cvList = cvList;
	}
	
	public void addElement(CVType elem) {
		cvList.add(elem);
	}
	
	public int size() {
		return cvList.size();
	}

	public Iterator<CVType> iterator() {
		return cvList.iterator();
	}
	
	
}
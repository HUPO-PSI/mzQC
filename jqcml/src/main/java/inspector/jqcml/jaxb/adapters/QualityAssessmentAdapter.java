package inspector.jqcml.jaxb.adapters;

import inspector.jqcml.model.AbstractParameter;
import inspector.jqcml.model.AttachmentParameter;
import inspector.jqcml.model.CVParameter;
import inspector.jqcml.model.QualityAssessment;
import inspector.jqcml.model.QualityAssessmentList;
import inspector.jqcml.model.QualityParameter;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import javax.xml.bind.annotation.adapters.XmlAdapter;

public class QualityAssessmentAdapter extends XmlAdapter<QualityAssessmentList, QualityAssessment> {

	@Override
	public QualityAssessmentList marshal(QualityAssessment arg0) throws Exception {
		// test for null
		// this is needed because the SetQuality can be null
		if(arg0 == null)
			return null;
		else {
			QualityAssessmentList qal = new QualityAssessmentList();
			qal.setId(arg0.getId());
			qal.setSet(arg0.isSet());

			// sort by ID (Map has an undefined order)
			List<CVParameter> qpList = new ArrayList<CVParameter>(arg0.getQualityParameterList().values());
			Collections.sort(qpList, new ParameterIDComparator());
			List<CVParameter> apList = new ArrayList<CVParameter>(arg0.getAttachmentList().values());
			Collections.sort(apList, new ParameterIDComparator());
			
			// join both lists
			qal.addParameterList(qpList);
			qal.addParameterList(apList);
			
			return qal;
		}
	}

	@Override
	public QualityAssessment unmarshal(QualityAssessmentList arg0) throws Exception {
		QualityAssessment qa = new QualityAssessment(arg0.getId());
		qa.setSet(arg0.isSet());
		
		for(CVParameter param : arg0) {
			if(param instanceof QualityParameter)
				qa.addQualityParameter((QualityParameter) param);
			else if(param instanceof AttachmentParameter)
				qa.addAttachmentParameter((AttachmentParameter) param);
		}
		
		return qa;
	}

}

class ParameterIDComparator implements Comparator<AbstractParameter> {

	public int compare(AbstractParameter o1, AbstractParameter o2) {
		return o1.getId().compareTo(o2.getId());
	}
	
}

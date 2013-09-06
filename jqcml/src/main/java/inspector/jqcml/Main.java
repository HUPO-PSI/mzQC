package inspector.jqcml;

import inspector.jqcml.io.MzQualMLReader;
import inspector.jqcml.io.xml.QcMLJAXBContext;
import inspector.jqcml.io.xml.QcMLMarshaller;
import inspector.jqcml.io.xml.QcMLReader;
import inspector.jqcml.io.xml.QcMLWriter;
import inspector.jqcml.model.CVType;
import inspector.jqcml.model.QualityAssessment;

import java.io.File;
import java.io.IOException;
import java.util.Iterator;

import javax.xml.bind.SchemaOutputResolver;
import javax.xml.transform.Result;
import javax.xml.transform.stream.StreamResult;

public class Main {

	public static void main(String[] args) {
		// output XML schema from model
		/*SchemaOutputResolver sor = new MySchemaOutputResolver();
		context.generateSchema(sor);*/
		
		// read from qcML file
		MzQualMLReader reader = new QcMLReader("data/samplefile_0_0_6.qcML");
		//System.out.println(reader.getMzQualityML());
		//System.out.println(reader.getQualityAssessment("testrun1"));
		//System.out.println(reader.getCV("MS"));
		
		Iterator<QualityAssessment> it = reader.getQualityAssessmentIterator();
		while(it.hasNext()) {
			System.out.println(it.next());
		}
		
		// write to qcML file
		//QcMLWriter writer = new QcMLWriter("test.qcml");
		//writer.write(reader.getMzQualityML());
	}	
}

class MySchemaOutputResolver extends SchemaOutputResolver {
	 
    public Result createOutput(String namespaceURI, String suggestedFileName) throws IOException {
        File file = new File(suggestedFileName);
        StreamResult result = new StreamResult(file);
        result.setSystemId(file.toURI().toURL().toString());
        return result;
    }
 
}

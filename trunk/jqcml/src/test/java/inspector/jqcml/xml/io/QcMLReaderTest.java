package inspector.jqcml.xml.io;

import static org.junit.Assert.*;

import inspector.jqcml.io.MzQualMLReader;
import inspector.jqcml.io.xml.QcMLReader;
import inspector.jqcml.model.CVType;
import inspector.jqcml.model.QualityAssessment;

import java.util.Iterator;

import org.junit.Test;

public class QcMLReaderTest {

	@Test(expected=NullPointerException.class)
	public void testConstructorNull() {
		new QcMLReader(null);
	}
	
	@Test(expected=NullPointerException.class)
	public void testSetFileNull() {
		MzQualMLReader reader = new QcMLReader();
		reader.setFile(null);
	}

	@Test(expected=IllegalArgumentException.class)
	public void testSetFileNonExisting() {
		MzQualMLReader reader = new QcMLReader();
		reader.setFile("data/test/non_existing_file.qcml");
	}

	@Test
	public void testGetCV() {
		MzQualMLReader reader = new QcMLReader();
		reader.setFile("data/test/simple.qcml");
		assertEquals("Test if the CVType with the right ID and name is returned", "Test full name 1", reader.getCV("cv_1").getFullName());
	}
	
	@Test
	public void testGetCVNull() {
		MzQualMLReader reader = new QcMLReader();
		reader.setFile("data/test/simple.qcml");
		assertNull("Test for CVType with ID <null>", reader.getCV("null"));
	}
	
	@Test
	public void testGetCVNonExisting() {
		MzQualMLReader reader = new QcMLReader();
		reader.setFile("data/test/simple.qcml");
		assertNull("Test for CVType with non-existing ID", reader.getCV("non-existing ID"));
	}

	@Test
	public void testGetCVIterator() {
		MzQualMLReader reader = new QcMLReader();
		reader.setFile("data/test/simple.qcml");
		Iterator<CVType> it = reader.getCVIterator();
		// test if each CVType has been processed
		int count = 0;
		for(int i = 1; it.hasNext(); i++) {
			CVType cv = it.next();
			assertEquals("Test if the CVType with the right ID and name is returned", "Test full name " + i, cv.getFullName());
			count = i;
		}
		// test the total amount of items processed
		assertEquals("Test if all available CVTypes are iterated through", 5, count);
	}

	@Test
	public void testGetQualityAssessmentRunQuality() {
		MzQualMLReader reader = new QcMLReader();
		reader.setFile("data/test/simple.qcml");
		QualityAssessment qa = reader.getQualityAssessment("run_1");
		assertEquals("Test if the QualityAssessment with the right ID is returned", "run_1", qa.getId());
		assertFalse("Test if the QualityAssessment denotes a RunQuality", qa.isSet());
	}

	@Test
	public void testGetQualityAssessmentSetQuality() {
		MzQualMLReader reader = new QcMLReader();
		reader.setFile("data/test/simple.qcml");
		QualityAssessment qa = reader.getQualityAssessment("set_1");
		assertEquals("Test if the QualityAssessment with the right ID is returned", "set_1", qa.getId());
		assertTrue("Test if the QualityAssessment denotes a SetQuality", qa.isSet());
	}
	
	@Test
	public void testGetQualityAssessmentNull() {
		MzQualMLReader reader = new QcMLReader();
		reader.setFile("data/test/simple.qcml");
		assertNull("Test for QualityAssessment with ID <null>", reader.getQualityAssessment("null"));
	}
	
	@Test
	public void testGetQualityAssessmentNonExisting() {
		MzQualMLReader reader = new QcMLReader();
		reader.setFile("data/test/simple.qcml");
		assertNull("Test for QualityAssessment with non-existing ID", reader.getQualityAssessment("non-existing ID"));
	}

	@Test
	public void testGetQualityAssessmentIterator() {
		MzQualMLReader reader = new QcMLReader();
		reader.setFile("data/test/simple.qcml");
		Iterator<QualityAssessment> it = reader.getQualityAssessmentIterator();
		// test if each QualityAssessment has been processed
		int amountRun = 0;
		int amountSet = 0;
		while(it.hasNext()) {
			QualityAssessment qa = it.next();
			if(!qa.isSet())
				amountRun++;
			else
				amountSet++;
		}
		// test if the correct amount of Run/SetQuality's have been processed
		assertEquals("Test if the correct amount of RunQuality's have been processed", 3, amountRun);
		assertEquals("Test if the correct amount of SetQuality's have been processed", 2, amountSet);
	}

}

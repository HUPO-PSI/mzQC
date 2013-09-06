package inspector.jqcml.xml.io;

import inspector.jqcml.io.xml.QcMLWriter;

import org.junit.Test;

public class QcMLWriterTest {

	@Test(expected=NullPointerException.class)
	public void testConstructorNull() {
		new QcMLWriter(null);
	}
	
	@Test(expected=NullPointerException.class)
	public void testSetFileNull() {
		QcMLWriter writer = new QcMLWriter();
		writer.setFile(null);
	}
	
	@Test(expected=IllegalArgumentException.class)
	public void testWriteNull() {
		QcMLWriter writer = new QcMLWriter("data/test/out.qcml");
		writer.write(null);
	}
}

package inspector.jqcml.io.xml;

import inspector.jqcml.model.MzQualityML;

import java.io.File;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * An MzQualML output writer which writes to a qcML file.
 */
public class QcMLWriter {
	
	private static final Logger logger = LogManager.getLogger(QcMLWriter.class);
	
	private File qcmlFile;
	
	private QcMLMarshaller marshaller;

	/**
	 * Creates a QcMLWriter by initializing a {@link QcMLMarshaller}.
	 * 
	 * Attention: If this default constructor is used, a subsequent call to {@link #setFile(String) setFile} is required before the Writer can be used.
	 */
	public QcMLWriter() {
		marshaller = new QcMLMarshaller();
	}
	
	/**
	 * Creates a QcMLWriter by initializing a {@link QcMLMarshaller} and initializes it to write to the file with the specified file name.
	 * 
	 * @param fileName  The file name of the file to which the Writer will write.
	 */
	public QcMLWriter(String fileName) {
		this();
		
		setFile(fileName);
	}
	
	/**
	 * Sets the file to which the Writer will write.
	 * 
	 * @param fileName  The file name of the file to which the Writer will write.
	 */
	public void setFile(String fileName) {
		// check whether the file name is valid
		if(fileName == null) {
			logger.error("Invalid file name <null>");
			throw new NullPointerException("Invalid file name");
		}
				
		qcmlFile = new File(fileName);
		logger.info("Set qcML file <{}>", qcmlFile.getAbsoluteFile());
	}
	
	/**
	 * Writes a {@link MzQualityML} object to the current file.
	 * 
	 * @param qcml  The {@link MzQualityML} object to be written to the file.
	 */
	public void write(MzQualityML qcml) {
		if(qcml != null)
			marshaller.marshal(qcml, qcmlFile);
		else {
			logger.error("Unable to marshal <null> element to file <{}>", qcmlFile.getAbsolutePath());
			throw new IllegalArgumentException("Unable to marshal <null> element to file <" + qcmlFile.getAbsolutePath() + ">");
		}
	}

}

package inspector.jqcml.io.xml;

import inspector.jqcml.io.xml.index.QcMLIndexer;

import java.util.Iterator;
import java.util.NoSuchElementException;
import java.util.Map.Entry;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import psidev.psi.tools.xxindex.index.IndexElement;

/**
 * An {@link Iterator} over a specified object in a qcML file.
 * 
 * @param <T> The qcML (sub)object over which the iterator loops.
 * This should be an object that is included in the {@link QcMLIndexer}.
 */
public class QcMLIterator<T> implements Iterator<T> {
	
	protected static final Logger logger = LogManager.getLogger(QcMLIterator.class);
	
	protected Class<T> clss;
	protected QcMLIndexer index;
	protected QcMLUnmarshaller unmarshaller;
	
	protected Iterator<Entry<String, IndexElement>> iterator;
	
	/**
	 * Create a QcMLIterator that will iterate over qcML (sub)objects of the specified class type.
	 * 
	 * @param index  The {@link QcMLIndexer} used to index the qcML file.
	 * @param unmarshaller  The {@link QcMLUnmarshaller} to unmarshal the qcML file.
	 * @param clss  The class type of the object returned by the iterator.
	 */
	public QcMLIterator(QcMLIndexer index, QcMLUnmarshaller unmarshaller, Class<T> clss) {
		this.clss = clss;
		this.index = index;
		this.unmarshaller = unmarshaller;
		
		iterator = index.getIDMapping(clss).entrySet().iterator();
	}

	@Override
	public boolean hasNext() {
		return iterator.hasNext();
	}

	@Override
	public T next() throws NoSuchElementException {
		logger.info("Retrieve next element from the iterator for type <{}>", clss);
		
		// get the next index element
		IndexElement elem = iterator.next().getValue();
		// read the xml snippet
		String xmlSnippet = index.readXML(elem);
		// unmarshal this element
		return unmarshaller.unmarshal(xmlSnippet, clss);
	}

	@Override
	public void remove() {
		throw new UnsupportedOperationException("Unable to remove objects while iterating");
	}

}

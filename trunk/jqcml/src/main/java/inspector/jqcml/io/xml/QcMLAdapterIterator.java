package inspector.jqcml.io.xml;

import java.util.Iterator;
import java.util.NoSuchElementException;

import javax.xml.bind.annotation.adapters.XmlAdapter;

import psidev.psi.tools.xxindex.index.IndexElement;

import inspector.jqcml.io.xml.index.QcMLIndexer;

/**
 * An {@link Iterator} over a specified object in a qcML file.
 * 
 * After unmarshalling the object from the qcML file, an XmlAdapter is used to transform the object.
 * 
 * @param <T> The qcML (sub)object that is unmarshalled from the qcML file.
 * This should be an object that is included in the {@link QcMLIndexer}.
 * @param <T> The qcML (sub)object over which the iterator loops.
 * This object type is obtained by transforming the unmarshalled object using an {@link XmlAdapter}.
 */
public class QcMLAdapterIterator<S, T> extends QcMLIterator<T> {
	
	protected Class<S> preClass;
	protected XmlAdapter<S, T> adapter;
	
	/**
	 * Create a QcMLAdapterIterator that will iterate over qcML (sub)objects of the specified class type.
	 * 
	 * @param index  The {@link QcMLIndexer} used to index the qcML file.
	 * @param unmarshaller  The {@link QcMLUnmarshaller} to unmarshal the qcML file.
	 * @param preClass  The class type of the unmarshalled object prior to conversion with the adapter.
	 * @param postClass  The class type of the unmarshalled object after the conversion with the adapter.
	 * @param adapter  The {@link XmlAdapter} used to convert the unmarshalled object.
	 */
	public QcMLAdapterIterator(QcMLIndexer index, QcMLUnmarshaller unmarshaller, Class<S> preClass, Class<T> postClass, XmlAdapter<S, T> adapter) {
		super(index, unmarshaller, postClass);
		
		this.preClass = preClass;
		this.adapter = adapter;
	}
	
	@Override
	public T next() throws NoSuchElementException {
		logger.info("Retrieve next element from the iterator for type <{}>", clss);
		
		// get the next index element
		IndexElement elem = iterator.next().getValue();
		// read the xml snippet
		String xmlSnippet = index.readXML(elem);
		// unmarshal this element
		S temp = unmarshaller.unmarshal(xmlSnippet, preClass);
		// manually call the adapter
		try {
			return adapter.unmarshal(temp);
		} catch (Exception e) {
			logger.error("Unable to manually call adapter {} for XML snippet: {}\n{}", adapter, xmlSnippet.substring(0, xmlSnippet.indexOf('>')+1), e);
			throw new IllegalStateException("Unable to manually call the XmlAdapter: " + e);
		}
	}

}

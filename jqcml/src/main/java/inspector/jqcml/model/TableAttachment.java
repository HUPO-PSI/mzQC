package inspector.jqcml.model;

import java.util.Arrays;

import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;

import inspector.jqcml.jaxb.adapters.TableAttachmentAdapter;

@XmlJavaTypeAdapter(TableAttachmentAdapter.class)
public class TableAttachment {

	/** List (space separated) of cvRefs determining the type of the respective column. */
	private String[] tableHeader;
	private double[][] tableBody;
	
	public TableAttachment() {
		// do nothing
	}
	
	public String[] getTableHeader() {
		return tableHeader;
	}
	
	public void setTableHeader(String[] header) {
		tableHeader = header;
	}
	
	public double[][] getTableBody() {
		return tableBody;
	}
	
	public void setTableBody(double[][] body) {
		tableBody = body;
	}
	
	public String toString() {
		return "TableAttachment header=\"" + Arrays.toString(tableHeader) + "\"";
	}
	
	
}

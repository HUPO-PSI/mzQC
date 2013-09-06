package inspector.jqcml.model;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

@XmlAccessorType(XmlAccessType.FIELD)
public class TableStringAttachment {

	@XmlElement(name="TableColumnTypes")
	private String tableHeader;
	@XmlElement(name="TableRowValues")
	private String[] tableBody;

	public TableStringAttachment() {
		// do nothing
	}

	public String getTableHeader() {
		return tableHeader;
	}

	public void setTableHeader(String header) {
		this.tableHeader = header;
	}

	public String[] getTableBody() {
		return tableBody;
	}

	public void setTableBody(String[] body) {
		this.tableBody = body;
	}
}

package inspector.jqcml.jaxb.adapters;

import inspector.jqcml.model.TableAttachment;
import inspector.jqcml.model.TableStringAttachment;

import javax.xml.bind.annotation.adapters.XmlAdapter;

public class TableAttachmentAdapter extends XmlAdapter<TableStringAttachment, TableAttachment> {

	@Override
	public TableStringAttachment marshal(TableAttachment arg0) throws Exception {
		if(arg0 == null)
			return null;
		else {
			TableStringAttachment result = new TableStringAttachment();
	
			// convert the header
			String header = marshalHeader(arg0.getTableHeader());
			result.setTableHeader(header);
	
			// convert the body
			String[] body = marshalBody(arg0.getTableBody());
			result.setTableBody(body);
	
			return result;
		}
	}

	private String marshalHeader(String[] header) {
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < header.length; i++) {
			sb.append(header[i]);

			if (i < header.length - 1)
				sb.append(' ');
		}

		return sb.toString();
	}

	private String[] marshalBody(double[][] body) {
		// combine all columns of the same row in a single string
		String[] result = new String[body.length];
		for (int row = 0; row < body.length; row++) {
			StringBuilder sb = new StringBuilder();

			for (int column = 0; column < body[row].length; column++) {
				sb.append(body[row][column]);

				if (column < body[row].length - 1)
					sb.append(' ');
			}

			result[row] = sb.toString();
		}

		return result;
	}

	@Override
	public TableAttachment unmarshal(TableStringAttachment arg0) throws Exception {
		TableAttachment result = new TableAttachment();

		// convert the header
		String[] header = unmarshalHeader(arg0.getTableHeader());
		result.setTableHeader(header);

		// convert the body
		double[][] body = unmarshalBody(arg0.getTableBody());
		result.setTableBody(body);

		return result;
	}

	private String[] unmarshalHeader(String header) {
		// split the string on whitespaces and put the individual items in an array
		return header.split("\\s+");
	}

	private double[][] unmarshalBody(String[] body) {
		// split all rows on whitespaces and put the individual items in an array as doubles
		double[][] result = new double[body.length][];
		for (int row = 0; row < body.length; row++) {
			String[] content = body[row].split("\\s+");
			double[] doubles = new double[content.length];
			for (int column = 0; column < content.length; column++)
				doubles[column] = Double.parseDouble(content[column]);

			result[row] = doubles;
		}

		return result;
	}

}

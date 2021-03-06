import org.w3c.dom.*;
import javax.xml.parsers.*;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class PageContent {
    private Content _content;

    public PageContent(String pageContentResponse) {
        init(pageContentResponse);
    }

    private void init(String pageContentResponse) {
        try {
            _content = new Content();
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();

            InputStream stream = new ByteArrayInputStream(pageContentResponse.getBytes(StandardCharsets.UTF_8));

            Document document = builder.parse(stream);

            parseDocument(document);
        }
        catch (Exception ex) {

        }
    }

    private void parseDocument(Document document) {
        document.getDocumentElement().normalize();
        Element root = document.getDocumentElement();

        Element content = (Element)root.getElementsByTagName("content").item(0);

        _content.set_groupId(content.getAttribute("groupID"));
        _content.set_segmentId(content.getAttribute("segmentID"));

        Element itemsElement = (Element)content.getElementsByTagName("items").item(0);
        NodeList items = itemsElement.getElementsByTagName("item");

        for (int i = 0; i < items.getLength(); i++) {
            Node item = items.item(i);

            if (item.getNodeType() == Node.ELEMENT_NODE) {
                Element element = (Element)item;

                String bankKey = element.getAttribute("bankKey");
                String itemKey = element.getAttribute("itemKey");
                String format = element.getAttribute("format");
                String responseType = element.getAttribute("responseType");
                String position = element.getAttribute("position");

                NodeList filePathNodeList = element.getElementsByTagName("filePath");
                String filepath = filePathNodeList.item(0).getTextContent();

                _content.addItem(bankKey, itemKey, format, responseType, position, filepath);
            }

        }
    }

    private String buildAnswer(String format, String responseType) {
        return "<![CDATA[hardcoded for now since data does not matter for tests]]>";
    }

    public Content get_content() {
        return _content;
    }

    public String get_responsesXml(String pageKey) {
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();

            Document doc = builder.newDocument();
            Element root = doc.createElement("responses");
            doc.appendChild(root);

            for(Item item : _content.get_items()) {
                Element response = doc.createElement("response");
                response.setAttribute("id", item.get_bankKey() + "-" + item.get_itemKey());
                response.setAttribute("bankKey", item.get_bankKey());
                response.setAttribute("itemKey", item.get_itemKey());
                //response.setAttribute("segmentID", _content.get_segmentId());
                //response.setAttribute("pageKey", pageKey);
                //response.setAttribute("page", "1"); // TODO: fix this
                response.setAttribute("position", item.get_position());
                response.setAttribute("sequence", "1"); // TODO: fix this
                response.setAttribute("selected", "true"); // TODO: maybe this is hard-coded and okay to leave
                response.setAttribute("valid", "true"); // TODO: maybe this is hard-coded and okay to leave

                Element filePath = doc.createElement("filePath");
                filePath.setTextContent(item.get_filePath());

                Element value = doc.createElement("value");
                value.setTextContent(buildAnswer(item.get_format(), item.get_responseType()));

                response.appendChild(filePath);
                response.appendChild(value);

                root.appendChild(response);
            }

            // transform the XML into a string
            TransformerFactory tf = TransformerFactory.newInstance();
            Transformer transformer = tf.newTransformer();
            transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
            StringWriter writer = new StringWriter();
            transformer.transform(new DOMSource(doc), new StreamResult(writer));
            String output = writer.getBuffer().toString().replaceAll("\n|\r", "");
            return output;
        }
        catch (Exception ex) {

        }

        return null;
    }


}

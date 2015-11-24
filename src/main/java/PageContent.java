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

    PageContent(String pageContentResponse) {
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

                _content.addItem(bankKey, itemKey, format, responseType, position);
            }

        }
    }

    private String buildAnswer(String format, String responseType) {
        return "<![CDATA[TODO make this smart]]>";
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

            for(Content.Item item : _content.get_items()) {
                Element response = doc.createElement("response");
                response.setAttribute("id", item.get_bankKey() + "-" + item.get_itemKey());
                response.setAttribute("bankKey", item.get_bankKey());
                response.setAttribute("itemKey", item.get_itemKey());
                response.setAttribute("segmentID", _content.get_segmentId());
                response.setAttribute("pageKey", pageKey);
                response.setAttribute("page", "1"); // TODO: fix this
                response.setAttribute("position", item.get_position());
                response.setAttribute("sequence", "1"); // TODO: fix this
                response.setAttribute("selected", "true"); // TODO: maybe this is hard-coded and okay to leave
                response.setAttribute("valid", "true"); // TODO: maybe this is hard-coded and okay to leave

                Element filePath = doc.createElement("filePath");
                filePath.setTextContent("TODO pull this from parsed data");

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

    public class Content {
        private String _groupId;
        private String _segmentId;
        private List<Item> _items = new ArrayList<Item>();

        public String get_groupId() {
            return _groupId;
        }

        public void set_groupId(String _groupId) {
            this._groupId = _groupId;
        }

        public String get_segmentId() {
            return _segmentId;
        }

        public void set_segmentId(String _segmentId) {
            this._segmentId = _segmentId;
        }

        public List<Item> get_items() {
            return _items;
        }

        public void addItem(String bankKey, String itemKey, String format, String responseType, String position) {
            Item item = new Item();
            item.set_bankKey(bankKey);
            item.set_itemKey(itemKey);
            item.set_format(format);
            item.set_responseType(responseType);
            item.set_position(position);

            _items.add(item);
        }


        public class Item {
            private String _bankKey;
            private String _itemKey;
            private String _format;
            private String _responseType;
            private String _position;

            public String get_bankKey() {
                return _bankKey;
            }

            public void set_bankKey(String _bankKey) {
                this._bankKey = _bankKey;
            }

            public String get_itemKey() {
                return _itemKey;
            }

            public void set_itemKey(String _itemKey) {
                this._itemKey = _itemKey;
            }

            public String get_format() {
                return _format;
            }

            public void set_format(String _format) {
                this._format = _format;
            }

            public String get_responseType() {
                return _responseType;
            }

            public void set_responseType(String _responseType) {
                this._responseType = _responseType;
            }

            public String get_position() {
                return _position;
            }

            public void set_position(String _position) {
                this._position = _position;
            }
        }
    }
}

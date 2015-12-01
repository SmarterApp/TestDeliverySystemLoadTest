import java.util.ArrayList;
import java.util.List;

/**
 * Created by emunoz on 11/27/15.
 */
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

    public void addItem(String bankKey, String itemKey, String format, String responseType, String position,
                        String filePath) {
        Item item = new Item();
        item.set_bankKey(bankKey);
        item.set_itemKey(itemKey);
        item.set_format(format);
        item.set_responseType(responseType);
        item.set_position(position);
        item.set_filePath(filePath);

        _items.add(item);
    }

}
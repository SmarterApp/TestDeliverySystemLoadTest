import static org.junit.Assert.*;

public class PageContentTest {

    @org.junit.Before
    public void setUp() throws Exception {

    }

    @org.junit.After
    public void tearDown() throws Exception {

    }

    @org.junit.Test
    public void testGet_content() throws Exception {

    }

    @org.junit.Test
    public void testGet_responsesXml() throws Exception {
        String response = "<?xml version='1.0' encoding='UTF-8'?><contents><content groupID=\"I-187-1701\" segmentID=\"SBAC ELA 3-ELA-3\" layout=\"8\" language=\"ENU\"><items><item bankKey=\"187\" itemKey=\"1701\" subject=\"ELA\" grade=\"3\" format=\"ER\" marked=\"false\" disabled=\"false\" printable=\"false\" printed=\"false\" responseType=\"PlainText\" position=\"3\" positionOnPage=\"1\"><filePath>zAThmxFZB9srBd53ZMmS2rq%2F4ms2MoD6UXiQkyMxLk8mKyrIWaX83IVl0Q3VJFd%2BETjafXhmaeJgC7%2FXdMUBAAAELekz4DsG0Bu1fLh6LOiYYuPCYlyV3u3MOHNwfeF2</filePath><tutorial bankKey=\"187\" itemKey=\"1078\"/><resources><resource type=\"wordList\" bankKey=\"187\" itemKey=\"1733\"/></resources><attachments><attachment id=\"braillefile1\" type=\"BRF\" subType=\"contracted\" target=\"\" url=\"/student/Pages/API/Resources.axd?path=zAThmxFZB9srBd53ZMmS2rq%2F4ms2MoD6UXiQkyMxLk8mKyrIWaX83IVl0Q3VJFd%2BETjafXhmaeJgC7%2FXdMUBAI8S3o79jDYBiJ960hkLwXI%3D&amp;file=item_1701_enu_contracted.brf\"/><attachment id=\"braillefile2\" type=\"BRF\" subType=\"uncontracted\" target=\"\" url=\"/student/Pages/API/Resources.axd?path=zAThmxFZB9srBd53ZMmS2rq%2F4ms2MoD6UXiQkyMxLk8mKyrIWaX83IVl0Q3VJFd%2BETjafXhmaeJgC7%2FXdMUBAI8S3o79jDYBiJ960hkLwXI%3D&amp;file=item_1701_enu_uncontracted.brf\"/></attachments></item></items><html><![CDATA[\n" +
                "<div xmlns=\"http://www.w3.org/1999/xhtml\" id=\"Page_I-187-1701\" class=\"subject_ELA grade_3 itemcount_1 layout_8 browser_chrome browserVer_46_0 platform_osx\">\n" +
                "<div id=\"Item_3\" class=\"multipleChoiceItem itemContainer format_er response_plaintext\">\n" +
                "\n" +
                "<table cellspacing=\"0\" cellpadding=\"0\" width=\"100%\" class=\"bigTable noColumns\">\n" +
                "  <tr>\n" +
                "  \t<td valign=\"top\" align=\"center\"><div class=\"theQuestions\"><span class=\"padding\"> <!-- wraps layouts -->\n" +
                "    \n" +
                "    \t<table cellspacing=\"0\" cellpadding=\"0\" class=\"structure layout8vertical\">\n" +
                "          <tr>\n" +
                "            <td class=\"questionCell\">\n" +
                "            <span class=\"markComment\"><a href=\"#\" id=\"Item_HelpLink_3\" class=\"contexthelp\">Item Tutorial</a>\n" +
                "                <a href=\"#\" id=\"Item_CommentLink_3\" class=\"commentItem\">Submit a comment for this item</a>\n" +
                "                <a href=\"#\" id=\"Item_MarkLink_3\" class=\"markReview \">Mark Item for Review</a><input type=\"checkbox\" id=\"Item_Mark_3\" name=\"Item_Mark_3\" style=\"display:none\" />\n" +
                "            </span>\n" +
                "\t<h2 id=\"QuestionNumber_3\" class=\"questionNumber\">3</h2>\n" +
                "\n" +
                "\t<div id=\"Stem_3\" class=\"stemContainer\"><p style=\"\">A student is writing a story for his English class about being late for school one day. Read the beginning paragraphs from the story and complete the task that follows.</p><p style=\"\"><br />This morning, I woke up late. My alarm clock never <span id=\"item_1701_TAG_5\" class=\"its-tag\" data-tag=\"word\" data-tag-boundary=\"start\" data-word-index=\"1\"></span>went off<span class=\"its-tag\" data-tag-ref=\"item_1701_TAG_5\" data-tag-boundary=\"end\"></span>! The only reason I woke up at all was because I heard my dog barking. I walked down the hall to my mother's room to find she was still in bed. <span id=\"item_1701_TAG_2_BEGIN\">“Mom! Wake up,”</span> I yelled. <span id=\"item_1701_TAG_3_BEGIN\">“I think we both overslept.”</span> I looked over at the clock and it was 7:30 a.m. School starts in one hour <span id=\"item_1701_TAG_1_BEGIN\">–</span> great!</p><p style=\"\"><br /> I ran into the bathroom. There, I brushed my teeth, washed my face, and then looked in the mirror. My hair was standing straight up! I combed it down with water as fast as I could.</p><p style=\"\"><br /> After that, I threw on some clothes and shoes. Racing into the kitchen, I grabbed my backpack from the table and an apple from the fruit bowl. <span id=\"item_1701_TAG_4_BEGIN\">“Bye, Mom!”</span> I yelled as I pushed through the screen door letting it <span id=\"item_1701_TAG_7\" class=\"its-tag\" data-tag=\"word\" data-tag-boundary=\"start\" data-word-index=\"3\"></span>slam<span class=\"its-tag\" data-tag-ref=\"item_1701_TAG_7\" data-tag-boundary=\"end\"></span> shut behind me.</p><p style=\"\"><br />As I ran for the sidewalk, I watched the bus pull away from the curb and turn down the next street. Soon it was out of sight.</p><p style=\"\"><br />In one or two paragraphs, write an ending to the story that follows from the events and experiences in the story.</p>\n" +
                "\t</div>\n" +
                "            </td>\n" +
                "          </tr>\n" +
                "          <tr>\n" +
                "            <td class=\"answerCell\">\n" +
                "<div id=\"plaintext_3\" class=\"plaintext format_ER\">\n" +
                "\t<textarea id=\"Item_Response_3\" name=\"Item_Response_3\" spellcheck=\"false\" tabindex=\"-1\"></textarea>\n" +
                "</div></td>\n" +
                "          </tr>\n" +
                "          <tr><td> \n" +
                "            <div id=\"Item_CommentBox_3\" class=\"commentBox\" style=\"display:none\">\n" +
                "                <textarea rows=\"4\" id=\"Item_Comment_3\" name=\"Item_Comment_3\"></textarea>\n" +
                "                 <a href=\"#\" id=\"Item_CommentCloseLink_3\" class=\"greenBtn\"><span>Close Comment</span></a>\n" +
                "            \t <span class=\"clear\"></span>\n" +
                "            </div>\n" +
                "            </td>\n" +
                "          </tr>\n" +
                "\t\t</table>\n" +
                "   \n" +
                "\t</span></div></td>   \n" +
                "  </tr>\n" +
                "</table>\n" +
                "</div>\n" +
                "</div>]]></html></content></contents>";

        String pageKey = "f3f02737-e0f3-4a5f-bb03-d014d7ff3478";
        String expectedResponseXml = "<responses><response id=\"187-1700\" bankKey=\"187\" itemKey=\"1700\" segmentID=\"SBAC ELA 3-ELA-3\" pageKey=\"f3f02737-e0f3-4a5f-bb03-d014d7ff3478\" page=\"1\" position=\"2\" sequence=\"1\" selected=\"true\" valid=\"true\" ><filePath>70ThFUdftgANlOktn0bU0gBIYSfwJbgYpqnEdcI7ryrghbYslma6wS%2Bt1GIzPcBMcbvnOgceXEGIrMGte9rl9RxIaQWV%2BIJdeDNkrL9dG02Znp3LQTd49mjV8ThTgH3%2B</filePath><value><![CDATA[<itemResponse><response id=\"EBSR1\"><value>A</value></response><response id=\"EBSR2\"><value>B</value></response></itemResponse>]]></value></response><response id=\"187-1692\" bankKey=\"187\" itemKey=\"1692\" segmentID=\"SBAC ELA 3-ELA-3\" pageKey=\"f3f02737-e0f3-4a5f-bb03-d014d7ff3478\" page=\"1\" position=\"1\" sequence=\"1\" selected=\"true\" valid=\"true\" ><filePath>70ThFUdftgANlOktn0bU0gBIYSfwJbgYpqnEdcI7ryrghbYslma6wS%2Bt1GIzPcBMcbvnOgceXEGIrMGte9rl9TUpcZpbJ6864gySGRrzxJwAtZ3wysD6P%2BK5Kt3gTINa</filePath><value><![CDATA[test textarea content]]></value></response></responses>";

        PageContent pageContent = new PageContent(response);

        String actualXml = pageContent.get_responsesXml(pageKey);

        assertTrue(actualXml.length() > 0);

//        InputStream is = new ByteArrayInputStream(actualXml.getBytes("UTF8"));
//        XPath xpath = XPathFactory.newInstance().newXPath();
//        String xpathExpression = "/responses/response/@id";
//        InputSource inputSource = new InputSource(is);
//        String id = xpath.evaluate(xpathExpression, inputSource);
//
//        assertEquals("187-1700", id);
    }
}
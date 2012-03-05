import info.bliki.wiki.dump.IArticleFilter;
import info.bliki.wiki.dump.Siteinfo;
import info.bliki.wiki.dump.WikiArticle;
import info.bliki.wiki.dump.WikiXMLParser;

import org.xml.sax.SAXException;

public class WikiParse {

	static class DemoArticleFilter implements IArticleFilter {
		@Override
		public void process(WikiArticle page, Siteinfo site) throws SAXException {
			if (page.isMain()) {
				String title = page.getTitle();
				System.out.println(title);
			}
		}
	}
	
	public static void main(String[] args) {
		String file = "/home/work/yuanj/jawiki/jawiki.xml";
		try {
			IArticleFilter handler = new DemoArticleFilter();
			WikiXMLParser wxp = new WikiXMLParser(file, handler);
			wxp.parse();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}

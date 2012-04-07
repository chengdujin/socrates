                                                                                                                                                                                                                                                                                                                                                                                                                package test;
import java.util.Date;
import java.io.FileWriter;
import java.io.IOException;

import info.bliki.wiki.dump.IArticleFilter;
import info.bliki.wiki.dump.Siteinfo;
import info.bliki.wiki.dump.WikiArticle;
import info.bliki.wiki.dump.WikiXMLParser;

import org.xml.sax.SAXException;

public class WikiParse {
	//static FileWriter fw;
	static class DemoArticleFilter implements IArticleFilter {
		FileWriter fw;
		boolean closeSign;
		public DemoArticleFilter(String fileName) throws IOException{
			fw=new FileWriter(fileName);
			closeSign=true;
		}
		@Override
		public void process(WikiArticle page, Siteinfo site) throws SAXException {
			if (page.isMain()) {
				String title = page.getTitle()+"\r\n";
				System.out.println(title);
				try {
					fw.write(title,0,title.length());  
					fw.flush();
					
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} 
			}
		}
		public void close() throws IOException{
			if(closeSign==true){
				closeSign=false;
				fw.close();
			}
		}
	}
	
	public static void main(String[] args) {
		//String file = "D:\\zhwiki-20120307-stub-articles.xml";
		if(args.length<2){
			System.out.println("not enough args");
			return;
		}
		try {
			//IArticleFilter handler = new DemoArticleFilter("e:\\file\\output.txt");
			//WikiXMLParser wxp = new WikiXMLParser(file, handler);
			IArticleFilter handler = new DemoArticleFilter(args[1]);
			WikiXMLParser wxp = new WikiXMLParser(args[0], handler);
			wxp.parse();
			((DemoArticleFilter)handler).close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}


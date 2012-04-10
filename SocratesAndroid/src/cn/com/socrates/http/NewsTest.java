package cn.com.socrates.http;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserFactory;

import cn.com.socrates.model.NewInfo;

import android.util.Log;

public class NewsTest {

	private static String xmlPath="http://rss.sina.com.cn/blog/tech/kj.xml";
	public static List<NewInfo> PullParseXML() throws Exception{
		List<NewInfo> listNewsTitle =  new ArrayList<NewInfo>();;
		NewInfo NewInfo = null;
		URL url = new URL(xmlPath);
		//构建XmlPullParserFactory
		XmlPullParserFactory pullParserFactory = XmlPullParserFactory.newInstance();
		//获取XmlPullParser的实例
		XmlPullParser xmlPullParser = pullParserFactory.newPullParser();
		Log.e("PullParseXML", "getXML......");
		//设置输入流  xml文件装载器
		xmlPullParser.setInput(url.openConnection().getInputStream(), "UTF-8");
		//开始
		Log.e("PullParseXML", "PullParseXML....start....");
		/**
		 * pull读到xml后 返回数字
		 *   读取到xml的声明返回数字0 START_DOCUMENT;
			   读取到xml的结束返回数字1 END_DOCUMENT ;
			   读取到xml的开始标签返回数字2 START_TAG
			   读取到xml的结束标签返回数字3 END_TAG
			   读取到xml的文本返回数字4 TEXT
		 */
		int eventType=xmlPullParser.getEventType();
		/**
		 * 只要这个事件返回的不是1 我们就一直读取xml文件
		 */
		while(eventType != XmlPullParser.END_DOCUMENT){
			String nodeName=xmlPullParser.getName();
			switch (eventType) {
			case XmlPullParser.START_DOCUMENT:
				break;
			case XmlPullParser.START_TAG:
				if("item".equals(nodeName)){
					NewInfo = new NewInfo();
				} 
				if("title".equals(nodeName) && NewInfo != null){
					NewInfo.setTitle(xmlPullParser.nextText());
				} 
				if("link".equals(nodeName)  && NewInfo != null){
					NewInfo.setLink(xmlPullParser.nextText());
				}
				if("pubDate".equals(nodeName)  && NewInfo != null){
					NewInfo.setPubDate(xmlPullParser.nextText());
				}
				break;
			case XmlPullParser.END_TAG:
				if("item".equals(nodeName)){
					listNewsTitle.add(NewInfo);
				}
				break;

			default:
				break;
			}
			eventType = xmlPullParser.next();
		}
		return listNewsTitle;
	}
	
	List<String> rsList = new ArrayList<String>();
	public String loadHtml(String link) throws IOException {
		// 定义一个url类的实例。
		URL url = new URL(link);
		Log.e("NewsTest", link);
		// 以特定格式读取文件流。
		InputStreamReader isr = new InputStreamReader(url.openStream(),"gb2312");
		BufferedReader br = new BufferedReader(isr);
		String s;
		
		boolean beginFind = false;
		while (null != (s = br.readLine())) { 
			if ("<!-- 正文内容 begin -->".equals(s.trim())) {
				beginFind = true;
			} else if ("<!-- 正文内容 end -->".equals(s.trim())) {
				break;
			}
			//System.out.println("s.trim(): "+s.trim());
			if (beginFind) {
				if(s.trim().startsWith("<p>")){
					rsList.add(findContent(s.trim()));
				}
			}
		}
		Log.e("NewsTest", String.valueOf(rsList.size()));
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < rsList.size(); i++) {
			System.out.println(rsList.get(i).replaceAll(" ", ""));
			sb.append(rsList.get(i).replaceAll(" ", "").replaceAll("&nbsp;", " "));
		}
		
		return sb.toString();
	}

	public String findContent(String html) {
		// 配置html标记。
		Pattern p = Pattern.compile("<(\\S*?)[^>]*>.*?| <.*? />");
		Matcher m = p.matcher(html);

		String rs = new String(html);
		// 找出所有html标记。
		while (m.find()) {
			// 删除html标记。
			rs = rs.replace(m.group(), "");
		}
		return rs;
	}
}

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
		//����XmlPullParserFactory
		XmlPullParserFactory pullParserFactory = XmlPullParserFactory.newInstance();
		//��ȡXmlPullParser��ʵ��
		XmlPullParser xmlPullParser = pullParserFactory.newPullParser();
		Log.e("PullParseXML", "getXML......");
		//����������  xml�ļ�װ����
		xmlPullParser.setInput(url.openConnection().getInputStream(), "UTF-8");
		//��ʼ
		Log.e("PullParseXML", "PullParseXML....start....");
		/**
		 * pull����xml�� ��������
		 *   ��ȡ��xml��������������0 START_DOCUMENT;
			   ��ȡ��xml�Ľ�����������1 END_DOCUMENT ;
			   ��ȡ��xml�Ŀ�ʼ��ǩ��������2 START_TAG
			   ��ȡ��xml�Ľ�����ǩ��������3 END_TAG
			   ��ȡ��xml���ı���������4 TEXT
		 */
		int eventType=xmlPullParser.getEventType();
		/**
		 * ֻҪ����¼����صĲ���1 ���Ǿ�һֱ��ȡxml�ļ�
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
		// ����һ��url���ʵ����
		URL url = new URL(link);
		Log.e("NewsTest", link);
		// ���ض���ʽ��ȡ�ļ�����
		InputStreamReader isr = new InputStreamReader(url.openStream(),"gb2312");
		BufferedReader br = new BufferedReader(isr);
		String s;
		
		boolean beginFind = false;
		while (null != (s = br.readLine())) { 
			if ("<!-- �������� begin -->".equals(s.trim())) {
				beginFind = true;
			} else if ("<!-- �������� end -->".equals(s.trim())) {
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
		// ����html��ǡ�
		Pattern p = Pattern.compile("<(\\S*?)[^>]*>.*?| <.*? />");
		Matcher m = p.matcher(html);

		String rs = new String(html);
		// �ҳ�����html��ǡ�
		while (m.find()) {
			// ɾ��html��ǡ�
			rs = rs.replace(m.group(), "");
		}
		return rs;
	}
}

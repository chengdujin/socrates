package cn.com.socrates.http;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.URI;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.util.Log;

import cn.com.socrates.data.Constant;
import cn.com.socrates.domian.WeiBoInfo;
import cn.com.socrates.utils.DateUtilsDef;

public class GetWeiboFromTwitter {

	public List<WeiBoInfo> getWeibo_NoAuthorize_UserIdOrName(String NoAuthorizeType,String NoAuthorize_Value)
	{
		Log.e("GetWeiboFromTwitter", "getWeibo_NoAuthorize_UserIdOrName");
		String url=HttpConstant.TWITTER_user_timeline+"."+"json";
		if(NoAuthorizeType==Constant.NOAUTHORIZE_TYPE_USERID)
		{
			url=url+"?user_id="+NoAuthorize_Value;
		}
		else
		{
			url=url+"?screen_name="+NoAuthorize_Value;
		}
		return getWeiboFromJson(url);
	}
	
	public List<WeiBoInfo> getWeiboFromJson(String url)
	{
		Log.e("GetWeiboFromTwitter", "getWeiboFromJson");
		List<WeiBoInfo> wbList=new ArrayList<WeiBoInfo>();
		try{
			HttpClient client=new DefaultHttpClient();
			HttpGet request=new HttpGet();
			request.setURI(new URI(url));
			HttpResponse response=client.execute(request);
			InputStream is = response.getEntity().getContent();
            Reader reader = new BufferedReader(new InputStreamReader(is), 4000);
            StringBuilder buffer = new StringBuilder((int) response.getEntity().getContentLength());
            try {
                char[] tmp = new char[1024];
                int l;
                while ((l = reader.read(tmp)) != -1) {
                    buffer.append(tmp, 0, l);
                }
            } finally {
                reader.close();
            }
            String string = buffer.toString();
            //Log.e("json", "rs:" + string);
            ((org.apache.http.HttpResponse) response).getEntity().consumeContent();
            JSONArray data=new JSONArray(string);
            for(int i=0;i<data.length();i++)
            {
                JSONObject d=data.getJSONObject(i);
                //Log.e("json", "rs:" + d.getString("created_at"));
                if(d!=null){
                    JSONObject u=d.getJSONObject("user");
                    if(d.has("retweeted_status")){
                        JSONObject r=d.getJSONObject("retweeted_status");
                    }
                     
                    //Î¢²©id
                    String id=d.getString("id");
                    String userId=u.getString("id");
                    String userName=u.getString("screen_name");
                    String userIcon=u.getString("profile_image_url");
                    //Log.e("userIcon", userIcon);
                    String time=d.getString("created_at");
                    String text=d.getString("text");
                    Boolean haveImg=false;
                    if(d.has("thumbnail_pic")){
                        haveImg=true;
                        //String thumbnail_pic=d.getString("thumbnail_pic");
                        //Log.e("thumbnail_pic", thumbnail_pic);
                    }
                     
                    Date startDate=new Date(time);
                    Date nowDate = Calendar.getInstance().getTime();
                    time=new DateUtilsDef().twoDateDistance(startDate,nowDate);
                    WeiBoInfo w=new WeiBoInfo();
                    w.setId(id);
                    w.setUserId(userId);
                    w.setUserName(userName);
                    w.setTime(time +" Ç°");
                    w.setText(text);
                     
                    w.setHaveImage(haveImg);
                    w.setUserIcon(userIcon);
                    wbList.add(w);
                }
            }
		} catch (Exception e) {
            e.printStackTrace();
        } 
		
		return wbList;
	}
}

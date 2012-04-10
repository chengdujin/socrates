package cn.com.socrates.http;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import cn.com.socrates.model.UserInfo;
import cn.com.socrates.model.WeiBoInfo;
import cn.com.socrates.oauth.OAuth;
import cn.com.socrates.utils.DateUtilsDef;

public class SinaDal {
	
	public String getWeibo_Authorize_UserInfo_Json(UserInfo user)
	{
		String result ="";
		OAuth auth=new OAuth();
        String url = HttpConstant.SINA_friends_timeline;
        //String url = "http://api.t.sina.com.cn/statuses/public_timeline.json";
        List<BasicNameValuePair> params=new ArrayList<BasicNameValuePair>();
        params.add(new BasicNameValuePair("source", auth.consumerKey)); 
        HttpResponse response = auth.SignRequest(user.getToken(), user.getTokenSecret(), url, params);
        if (200 == response.getStatusLine().getStatusCode()){
            try {
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
                result = buffer.toString();
                ((org.apache.http.HttpResponse) response).getEntity().consumeContent();
                 
             }catch (IllegalStateException e) {
                 e.printStackTrace();
             } catch (IOException e) {
                 e.printStackTrace();
             }
         }
        return result;
	}
}

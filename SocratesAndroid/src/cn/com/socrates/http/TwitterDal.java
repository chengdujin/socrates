package cn.com.socrates.http;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.URI;
import java.net.URISyntaxException;
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

import cn.com.socrates.model.WeiBoInfo;
import cn.com.socrates.utils.Constant;
import cn.com.socrates.utils.DateUtilsDef;

public class TwitterDal {

	public String getWeibo_NoAuthorize_UserIdOrName_Json(String NoAuthorizeType,String NoAuthorize_Value)
	{
		String result ="";
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
            result = buffer.toString();
            //Log.e("json", "rs:" + string);
            ((org.apache.http.HttpResponse) response).getEntity().consumeContent();
		} catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (URISyntaxException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return result;
	}
}

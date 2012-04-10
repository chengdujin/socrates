package cn.com.socrates.bll;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import cn.com.socrates.http.SinaDal;
import cn.com.socrates.model.UserInfo;
import cn.com.socrates.model.WeiBoInfo;
import cn.com.socrates.utils.DateUtilsDef;

public class SinaBll {
	private SinaDal sinaDal;
	public SinaBll()
	{
		sinaDal=new SinaDal();
	}
	
	public List<WeiBoInfo> getWeibo_Authorize_UserInfo(UserInfo user)
	{
		List<WeiBoInfo> wbList=new ArrayList<WeiBoInfo>();
		String string=sinaDal.getWeibo_Authorize_UserInfo_Json(user);
		try{
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
		}catch (JSONException e) {
            e.printStackTrace();
        } 
        return wbList;
	}
}

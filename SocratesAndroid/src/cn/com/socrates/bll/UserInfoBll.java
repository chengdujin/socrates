package cn.com.socrates.bll;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;

import cn.com.socrates.dal.UserInfoDal;
import cn.com.socrates.model.UserInfo;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;

public class UserInfoBll {
	private UserInfoDal userInfoHelper;
    public UserInfoBll(Context context){
    	userInfoHelper=new UserInfoDal(context);
    }
    
    public void Close()
    {
    	userInfoHelper.Close();
    }
    //��ȡusers���е�UserID��Access Token��Access Secret�ļ�¼
    public List<UserInfo> GetUserList(Boolean isSimple)
    {
        List<UserInfo> userList = new ArrayList<UserInfo>();
        Cursor cursor=userInfoHelper.GetUserList(isSimple);
        cursor.moveToFirst();
        while(!cursor.isAfterLast()&& (cursor.getString(1)!=null)){
            UserInfo user=new UserInfo();
            user.setId(cursor.getString(0));
            user.setUserId(cursor.getString(1));
            user.setToken(cursor.getString(2));
            user.setTokenSecret(cursor.getString(3));
            if(!isSimple){
            user.setUserName(cursor.getString(4));
            ByteArrayInputStream stream = new ByteArrayInputStream(cursor.getBlob(5)); 
            Drawable icon= Drawable.createFromStream(stream, "image");
            user.setUserIcon(icon);
            }
            userList.add(user);
            cursor.moveToNext();
        }
        cursor.close();
        return userList;
    }
    
    //�ж�users���е��Ƿ����ĳ��UserID�ļ�¼
    public Boolean HaveUserInfo(String UserId)
    {
        return userInfoHelper.HaveUserInfo(UserId);
    }
    
    //����users��ļ�¼������UserId�����û��ǳƺ��û�ͼ��
    public int UpdateUserInfo(String userName,Bitmap userIcon,String UserId)
    {
    	ContentValues values = new ContentValues();
        values.put(UserInfo.USERNAME, userName);
        // BLOB����  
        final ByteArrayOutputStream os = new ByteArrayOutputStream();  
        // ��Bitmapѹ����PNG���룬����Ϊ100%�洢          
        userIcon.compress(Bitmap.CompressFormat.PNG, 100, os);   
        // ����SQLite��Content��������Ҳ����ʹ��raw  
        values.put(UserInfo.USERICON, os.toByteArray());
        return userInfoHelper.UpdateUserInfo(values,UserId);
    }
    
    //����users��ļ�¼
    public int UpdateUserInfo(UserInfo user)
    {
        ContentValues values = new ContentValues();
        values.put(UserInfo.USERID, user.getUserId());
        values.put(UserInfo.TOKEN, user.getToken());
        values.put(UserInfo.TOKENSECRET, user.getTokenSecret());
        int id=userInfoHelper.UpdateUserInfo(values,user.getUserId());
        return id;
    }
    
    //���users��ļ�¼
    public Long SaveUserInfo(UserInfo user)
    {
        ContentValues values = new ContentValues();
        values.put(UserInfo.USERID, user.getUserId());
        values.put(UserInfo.TOKEN, user.getToken());
        values.put(UserInfo.TOKENSECRET, user.getTokenSecret());
        Long uid = userInfoHelper.SaveUserInfo(values);
        return uid;
    }
    
    //ɾ��users��ļ�¼
    public int DelUserInfo(String UserId){
        int id=userInfoHelper.DelUserInfo(UserId);
        return id;
    }
    
    private ContentValues createContentValues(UserInfo user) {
        ContentValues values = new ContentValues();
        values.put(UserInfo.USERID, user.getId());
        values.put(UserInfo.TOKEN, user.getToken() );
        values.put(UserInfo.TOKENSECRET, user.getTokenSecret());
        values.put(UserInfo.USERNAME, user.getUserName());
        values.put(UserInfo.USERICON, user.getUserIcon().toString());
        return values;
    }
}


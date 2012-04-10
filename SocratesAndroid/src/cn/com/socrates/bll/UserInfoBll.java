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
    //获取users表中的UserID、Access Token、Access Secret的记录
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
    
    //判断users表中的是否包含某个UserID的记录
    public Boolean HaveUserInfo(String UserId)
    {
        return userInfoHelper.HaveUserInfo(UserId);
    }
    
    //更新users表的记录，根据UserId更新用户昵称和用户图标
    public int UpdateUserInfo(String userName,Bitmap userIcon,String UserId)
    {
    	ContentValues values = new ContentValues();
        values.put(UserInfo.USERNAME, userName);
        // BLOB类型  
        final ByteArrayOutputStream os = new ByteArrayOutputStream();  
        // 将Bitmap压缩成PNG编码，质量为100%存储          
        userIcon.compress(Bitmap.CompressFormat.PNG, 100, os);   
        // 构造SQLite的Content对象，这里也可以使用raw  
        values.put(UserInfo.USERICON, os.toByteArray());
        return userInfoHelper.UpdateUserInfo(values,UserId);
    }
    
    //更新users表的记录
    public int UpdateUserInfo(UserInfo user)
    {
        ContentValues values = new ContentValues();
        values.put(UserInfo.USERID, user.getUserId());
        values.put(UserInfo.TOKEN, user.getToken());
        values.put(UserInfo.TOKENSECRET, user.getTokenSecret());
        int id=userInfoHelper.UpdateUserInfo(values,user.getUserId());
        return id;
    }
    
    //添加users表的记录
    public Long SaveUserInfo(UserInfo user)
    {
        ContentValues values = new ContentValues();
        values.put(UserInfo.USERID, user.getUserId());
        values.put(UserInfo.TOKEN, user.getToken());
        values.put(UserInfo.TOKENSECRET, user.getTokenSecret());
        Long uid = userInfoHelper.SaveUserInfo(values);
        return uid;
    }
    
    //删除users表的记录
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


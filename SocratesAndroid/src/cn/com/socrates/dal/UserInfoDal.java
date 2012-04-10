package cn.com.socrates.dal;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.util.Log;
import cn.com.socrates.model.UserInfo;

public class UserInfoDal extends DataHelper{
	
	public UserInfoDal(Context context){
        super(context);
    }
	//获取users表中的UserID、Access Token、Access Secret的记录
    public Cursor GetUserList(Boolean isSimple)
    {
        Cursor cursor=db.query(SqliteHelper.TB_NAME_USERS_USERS, null, null, null, null, null, UserInfo.ID+" DESC");
        return cursor;
    }
    
    //判断users表中的是否包含某个UserID的记录
    public Boolean HaveUserInfo(String UserId)
    {
        Boolean b=false;
        Cursor cursor=db.query(SqliteHelper.TB_NAME_USERS_USERS, null, UserInfo.USERID + "=" + UserId, null, null, null,null);
        b=cursor.moveToFirst();
       
        Log.e("HaveUserInfo",b.toString());
       
        cursor.close();
        return b;
    }
    
    //更新users表的记录，根据UserId更新用户昵称和用户图标
    public int UpdateUserInfo(ContentValues values,String UserId)
    {
        int id= db.update(SqliteHelper.TB_NAME_USERS_USERS, values, UserInfo.USERID + "=" + UserId, null);
        Log.e("UpdateUserInfo2",id+"");
        return id;
    }
    
    //更新users表的记录
    public int UpdateUserInfo(UserInfo user)
    {
        ContentValues values = new ContentValues();
        values.put(UserInfo.USERID, user.getUserId());
        values.put(UserInfo.TOKEN, user.getToken());
        values.put(UserInfo.TOKENSECRET, user.getTokenSecret());
        int id= db.update(SqliteHelper.TB_NAME_USERS_USERS, values, UserInfo.USERID + "=" + user.getUserId(), null);
        Log.e("UpdateUserInfo",id+"");
        return id;
    }
    
    //添加users表的记录
    public Long SaveUserInfo(ContentValues values)
    {
        Long uid = db.insert(SqliteHelper.TB_NAME_USERS_USERS, UserInfo.ID, values);
        Log.e("SaveUserInfo",uid+"");
        return uid;
    }
    
    //删除users表的记录
    public int DelUserInfo(String UserId){
        int id=  db.delete(SqliteHelper.TB_NAME_USERS_USERS, UserInfo.USERID +"="+UserId, null);
        Log.e("DelUserInfo",id+"");
        return id;
    }
}

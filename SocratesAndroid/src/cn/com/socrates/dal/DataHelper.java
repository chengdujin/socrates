package cn.com.socrates.dal;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;
import cn.com.socrates.model.UserInfo;

public class DataHelper {   
	//数据库名称
	protected static String DB_NAME = "Socrates.db";
    //数据库版本
    protected static int DB_VERSION = 2;
    protected  SQLiteDatabase db;
    protected SqliteHelper dbHelper;
    
    public DataHelper(Context context){
        dbHelper=new SqliteHelper(context,DB_NAME, null, DB_VERSION);
        db= dbHelper.getWritableDatabase();
    }
    
    public void Close()
    {
        db.close();
        dbHelper.close();
    }
    
    
    
}

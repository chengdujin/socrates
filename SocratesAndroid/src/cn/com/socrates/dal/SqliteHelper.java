package cn.com.socrates.dal;

import cn.com.socrates.model.UserInfo;
import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteDatabase.CursorFactory;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;
/**
 * 创建数据库  用来保存用户登录blog所需要的信息
 * @author nxh
 *
 */
public class SqliteHelper extends SQLiteOpenHelper {

	public static final String TB_NAME_USERS_USERS = "users";

	public SqliteHelper(Context context, String name, CursorFactory factory,
			int version) {
		super(context, name, factory, version);
	}

	//创建表
	@Override
	public void onCreate(SQLiteDatabase arg0) {
		arg0.execSQL("CREATE TABLE IF NOT EXISTS "+
				TB_NAME_USERS_USERS+"("+
	                UserInfo.ID+" integer primary key,"+
	                UserInfo.USERID+" varchar,"+
	                UserInfo.TOKEN+" varchar,"+
	                UserInfo.TOKENSECRET+" varchar,"+
	                UserInfo.USERNAME+" varchar,"+
	                UserInfo.USERICON+" blob"+
	                ")"
	                );
	        Log.e("Database","onCreate");
	}
	//更新表
	@Override
	public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
		db.execSQL("DROP TABLE IF EXISTS " + TB_NAME_USERS_USERS);
        onCreate(db);
        Log.e("Database","onUpgrade");
	}
	//更新列
	public void updateColumn(SQLiteDatabase db, String oldColumn, String newColumn, String typeColumn){
        try{
            db.execSQL("ALTER TABLE " +
            		TB_NAME_USERS_USERS + " CHANGE " +
                    oldColumn + " "+ newColumn +
                    " " + typeColumn
            );
        }catch(Exception e){
            e.printStackTrace();
        }
    }

}

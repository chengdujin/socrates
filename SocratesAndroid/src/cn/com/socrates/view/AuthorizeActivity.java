package cn.com.socrates.view;

import cn.com.socrates.data.Constant;
import cn.com.socrates.data.DataHelper;
import cn.com.socrates.data.ViewerPreferences;
import cn.com.socrates.domian.UserInfo;
import cn.com.socrates.oauth.OAuth;
import cn.com.socrates.oauth.R;
import android.app.Activity;
import android.app.Dialog;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

public class AuthorizeActivity extends Activity {
	private Dialog dialog;
	private OAuth auth;
	private ViewerPreferences viewerPreferences;
	private static final String CallBackUrl = "myapp://AuthorizeActivity";
 	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.authorize);
		
		viewerPreferences = new ViewerPreferences(this);
		
		View diaView=View.inflate(this, R.layout.dialog, null);
		dialog = new Dialog(AuthorizeActivity.this,R.style.dialog);
		dialog.setContentView(diaView);
		dialog.show();
		
		Button btn_start=(Button)diaView.findViewById(R.id.btn_start);
		btn_start.setOnClickListener(new OnClickListener(){
            public void onClick(View arg0) {
                auth=new OAuth("30632531","f539cb169860ed99cf8c1861c5da34f6");
                auth.RequestAccessToken(AuthorizeActivity.this, CallBackUrl);
            }
        });
        Button btn_cancel=(Button)diaView.findViewById(R.id.btn_cancel);
        btn_cancel.setOnClickListener(new OnClickListener(){
            public void onClick(View arg0) {
            	Intent intent = new Intent();
        		intent.putExtra("targetNet", viewerPreferences.getAuthorizeType());
        		intent.setClass(AuthorizeActivity.this, ChooseAuthorizeActivity.class);
        		startActivity(intent);
            }
        });
	}
	
	@Override
	protected void onNewIntent(Intent intent) {
		super.onNewIntent(intent);
        //在这里处理获取返回的oauth_verifier参数
        UserInfo user= auth.GetAccessToken(intent);
        if(user!=null){
            DataHelper helper=new DataHelper(this);
            String uid=user.getUserId();
            if(helper.HaveUserInfo(uid))
            {
            	helper.UpdateUserInfo(user);
            	Log.e("UserInfo", "update");
            }
            else{
            	helper.SaveUserInfo(user);
            	Log.e("UserInfo", "add");
            }
            helper.Close();
        }
        Intent intentReturn = new Intent();
        intentReturn.putExtra(Constant.AUTHORIZE_TYPE, Constant.AUTHORIZE_TYPE_OAUTH2);
        intentReturn.setClass(AuthorizeActivity.this, BrowserActivity.class);
        startActivity(intentReturn);
	}
}

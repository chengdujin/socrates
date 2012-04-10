package cn.com.socrates.view;

import cn.com.socrates.bll.ViewerPreferences;
import cn.com.socrates.oauth.R;
import cn.com.socrates.utils.Constant;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ImageButton;

public class SocratesMainActivity  extends Activity {
	
	private ImageButton btn_sina;
    private ImageButton btn_twitter;
    
    private ViewerPreferences viewerPreferences;
    
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);
		
		viewerPreferences = new ViewerPreferences(this);
		btn_sina=(ImageButton)findViewById(R.id.btn_sina);
		btn_twitter=(ImageButton)findViewById(R.id.btn_twitter);
		
		btn_sina.setOnClickListener(new OnClickListener()
		{
			public void onClick(View v)
			{
				startChooseAuthorizeActivity(Constant.TARGETNET_SINA);
			}
		});
		
		btn_twitter.setOnClickListener(new OnClickListener()
		{
			public void onClick(View v)
			{
				startChooseAuthorizeActivity(Constant.TARGETNET_TWITTER);
			}
		});
	}

	public void startChooseAuthorizeActivity(String targetNet)
	{
		//viewerPreferences.isAuthorized();
		viewerPreferences.setTargetNet(targetNet);
		Intent intent = new Intent();
		intent.putExtra("targetNet", targetNet);
		intent.setClass(SocratesMainActivity.this, ChooseAuthorizeActivity.class);
		startActivity(intent);
	}
}

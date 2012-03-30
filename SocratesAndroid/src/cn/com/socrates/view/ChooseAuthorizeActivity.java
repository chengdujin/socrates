package cn.com.socrates.view;

import java.util.List;

import cn.com.socrates.data.Constant;
import cn.com.socrates.data.DataHelper;
import cn.com.socrates.data.ViewerPreferences;
import cn.com.socrates.domian.UserInfo;
import cn.com.socrates.oauth.R;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;

import android.view.MotionEvent;

public class ChooseAuthorizeActivity  extends Activity {
	
	private Spinner sp_noAuthorizeType;
	private ArrayAdapter<String> adapter;
	
	private EditText et_userInfo;
	private Button btn_submit;
	
	private Button btn_OAuth2;
	
	private String noAuthorizeType=Constant.NOAUTHORIZE_TYPE_USERID;
	
	private Intent intent;
	
	private String targetNet;
	private ViewerPreferences viewerPreferences;
	private DataHelper dbHelper;
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.chooseauthorize);
		initView();
		
		intent=this.getIntent();
		targetNet=intent.getStringExtra("targetNet");
		
		viewerPreferences=new ViewerPreferences(this);
		
		initData();
	}
	
	private void initView()
	{
		sp_noAuthorizeType=(Spinner)findViewById(R.id.sp_noAuthorizeType);
		adapter=new ArrayAdapter<String>(this,android.R.layout.simple_spinner_item);
		adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
		adapter.add(Constant.NOAUTHORIZE_TYPE_USERID);
		adapter.add(Constant.NOAUTHORIZE_TYPE_USERNAME);
		sp_noAuthorizeType.setAdapter(adapter);
		
		et_userInfo=(EditText)findViewById(R.id.et_userInfo);
		btn_submit=(Button)findViewById(R.id.btn_submit);
		btn_OAuth2=(Button)findViewById(R.id.btn_OAuth2);
		
		btn_submit.setOnClickListener(new OnClickListener()
		{
			public void onClick(View v)
			{
				if(et_userInfo.getText().toString().trim().length()==0)
				{
					showAlert();	
				}
				else{
					Log.e("ChooseAuthorizeActivity", "noAuthorizeType:"+noAuthorizeType);
					//ʣ�µĲ���Ϊ�����ȡ΢��
					//���Ѿ���֤����ת���������ҳ��
		        	Intent intent = new Intent();
		        	intent.putExtra(Constant.AUTHORIZE_TYPE, Constant.AUTHORIZE_TYPE_NOAUTHORIZE);
		        	intent.putExtra(Constant.NOAUTHORIZE_TYPE,noAuthorizeType);
		        	intent.putExtra(Constant.NOAUTHORIZE_VALUE,et_userInfo.getText().toString().trim());
		            intent.setClass(ChooseAuthorizeActivity.this, BrowserActivity.class);
		            startActivity(intent);
				}
			}
		});
		
		btn_OAuth2.setOnClickListener(new OnClickListener()
		{
			public void onClick(View v)
			{
				//��ȡ�˺��б�
				dbHelper=new DataHelper(ChooseAuthorizeActivity.this);
		        List<UserInfo> userList= dbHelper.GetUserList(true);
		        if(userList.isEmpty())
		        {
		        	//���Ϊ��˵����һ��ʹ������AuthorizeActivityҳ�����OAuth��֤
		            Intent intent = new Intent();
		            intent.setClass(ChooseAuthorizeActivity.this, AuthorizeActivity.class);
		            startActivity(intent);
		        }
		        else{
		        	//���Ѿ���֤����ת���������ҳ��
		        	Intent intent = new Intent();
		        	intent.putExtra(Constant.AUTHORIZE_TYPE, Constant.AUTHORIZE_TYPE_OAUTH2);
		            intent.setClass(ChooseAuthorizeActivity.this, BrowserActivity.class);
		            startActivity(intent);
		        }
				
			}
		});
		
		sp_noAuthorizeType.setSelection(0);
		sp_noAuthorizeType.setOnItemSelectedListener(new Spinner.OnItemSelectedListener(){
			public void onItemSelected(AdapterView< ?> arg0, View arg1, int arg2, long arg3) {
			// TODO Auto-generated method stub
			/* ����ѡmySpinner ��ֵ����myTextView ��*/
			noAuthorizeType=adapter.getItem(arg2);
			/* ��mySpinner ��ʾ*/
			arg0.setVisibility(View.VISIBLE);
			}

			public void onNothingSelected(AdapterView< ?> arg0) {
			// TODO Auto-generated method stub
				noAuthorizeType="UserID";
			arg0.setVisibility(View.VISIBLE);
			}
		});

		/*�����˵�����������ѡ����¼�����*/
		sp_noAuthorizeType.setOnTouchListener(new Spinner.OnTouchListener(){
			public boolean onTouch(View v, MotionEvent event) {
			// TODO Auto-generated method stub
			/* ��mySpinner ���أ�������Ҳ���ԣ����Լ�����*/
			v.setVisibility(View.INVISIBLE);
			return false;
			}
		});

		/*�����˵�����������ѡ���ı��¼�����*/
		sp_noAuthorizeType.setOnFocusChangeListener(new Spinner.OnFocusChangeListener(){
			public void onFocusChange(View v, boolean hasFocus) {
			// TODO Auto-generated method stub
			v.setVisibility(View.VISIBLE);
			}
		});
		
	}
	
	private void initData()
	{
		//����΢��ʹ��othus2��֤
		if(targetNet.equals(Constant.TARGETNET_SINA))
		{
			btn_submit.setEnabled(false);
			btn_OAuth2.setEnabled(true);
		}
		//���ز���Ҫ��֤
		else if(targetNet.equals(Constant.TARGETNET_TWITTER))
		{
			btn_submit.setEnabled(true);
			btn_OAuth2.setEnabled(false);
			
			String NoAuthorizeType=viewerPreferences.getNoAuthorizeType();
			et_userInfo.setText(NoAuthorizeType);
			
			if(NoAuthorizeType==Constant.NOAUTHORIZE_TYPE_USERID)
			{
				sp_noAuthorizeType.setSelection(0);
				noAuthorizeType=Constant.NOAUTHORIZE_TYPE_USERID;
			}
			else if(NoAuthorizeType==Constant.NOAUTHORIZE_TYPE_USERNAME)
			{
				sp_noAuthorizeType.setSelection(1);
				noAuthorizeType=Constant.NOAUTHORIZE_TYPE_USERNAME;
			}
		}
	}
	
	private void showAlert()
	{
		String str=noAuthorizeType;
		final AlertDialog alert = new AlertDialog.Builder(this).create();
		alert.setMessage(str);
		alert.setButton("OK", new DialogInterface.OnClickListener() {

			public void onClick(DialogInterface dialog, int whichButton) {
				alert.dismiss();
			}
		});
		alert.show();
	}
	
	@Override
    protected void onDestroy() {
        super.onDestroy();
        if(dbHelper!=null)
        {
        	dbHelper.Close();
        }
    }
}

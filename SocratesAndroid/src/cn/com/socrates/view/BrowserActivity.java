package cn.com.socrates.view;

import java.util.ArrayList;
import java.util.List;

import cn.com.socrates.bll.SinaBll;
import cn.com.socrates.bll.TwitterBll;
import cn.com.socrates.bll.UserInfoBll;
import cn.com.socrates.http.NewsTest;
import cn.com.socrates.model.NewInfo;
import cn.com.socrates.model.UserInfo;
import cn.com.socrates.model.WeiBoInfo;
import cn.com.socrates.oauth.R;
import cn.com.socrates.presentation.NewsAdapter;
import cn.com.socrates.presentation.WeiBoAdapater;
import cn.com.socrates.utils.Constant;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.FrameLayout;
import android.widget.ListView;
import android.widget.TabHost;	

public class  BrowserActivity extends Activity {

	private NewsAdapter adapter;
	private UserInfoBll dbHelper;
	private List<NewInfo> newsList;

    private final AdapterView.OnItemClickListener onItemClickListener = new AdapterView.OnItemClickListener()
    {
        @SuppressWarnings({"unchecked"})
        public void onItemClick(AdapterView<?> adapterView, View view, int i, long l)
        {
        	NewInfo n =newsList.get(i);
        	Intent intent = new Intent();
			intent.setClass(BrowserActivity.this, NewsView.class);
			intent.putExtra("Title", n.getTitle());
			intent.putExtra("Link", n.getLink());
			startActivity(intent);
        }
    };
    private WeiBoAdapater weiboAdapter;
    private Intent intent;
    private String AuthorizeType;

    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.browser);
        Log.e("BrowserActivity", "onCreate");
        initView();
        
        newsList=new ArrayList<NewInfo>();
        intent=this.getIntent();
        AuthorizeType=intent.getStringExtra(Constant.AUTHORIZE_TYPE);
        
        initData();
    }
    
    private void initData()
    {
    	
    	Log.e("BrowserActivity", "initData");
    	if(AuthorizeType.equals(Constant.AUTHORIZE_TYPE_NOAUTHORIZE))
    	{
    		Log.e("BrowserActivity", "noAuthorizeType:"+AuthorizeType);
    		String NoAuthorize_Type=intent.getStringExtra(Constant.NOAUTHORIZE_TYPE);
    		String NoAuthorize_Value=intent.getStringExtra(Constant.NOAUTHORIZE_VALUE);
    		List<WeiBoInfo> weiboList=new TwitterBll().getWeibo_NoAuthorize_UserIdOrName(NoAuthorize_Type,NoAuthorize_Value);
    		if(weiboList!=null)
            {
    			weiboAdapter.setWeiBoList(weiboList);
            }
    	}
    	else{
    		Log.e("BrowserActivity", "AuthorizeType:"+AuthorizeType);
    		dbHelper=new UserInfoBll(BrowserActivity.this);
            List<UserInfo> userList= dbHelper.GetUserList(true);
            if(userList.isEmpty())
            {
            	Intent intent = new Intent();
                intent.setClass(BrowserActivity.this, AuthorizeActivity.class);
                startActivity(intent);
            }
	        List<WeiBoInfo> weiboList=new SinaBll().getWeibo_Authorize_UserInfo(userList.get(0));
	        if(weiboList!=null)
            {
    			weiboAdapter.setWeiBoList(weiboList);
            }
    	}
    	//get news
    	try
    	{
    	    newsList= new NewsTest().PullParseXML();
    	}catch(Exception e)
    	{
    		e.printStackTrace();
    	}
    	if(newsList!=null)
        {
    		adapter.setNewsList(newsList);
        }
    	
    }
    
    private void initView()
    {
    	Log.e("BrowserActivity", "initView");
    	final ListView newsList = initNewsListView();
        final ListView weiboListView = initWeiboListView();
        TabHost tabHost = (TabHost) findViewById(R.id.browserTabHost);
        tabHost.setup();
        tabHost.addTab(tabHost.newTabSpec("news").setIndicator("news").setContent(new TabHost.TabContentFactory()
        {
            public View createTabContent(String s)
            {
                return newsList;
            }
        }));
        tabHost.addTab(tabHost.newTabSpec("weibo").setIndicator("weibo").setContent(new TabHost.TabContentFactory()
        {
            public View createTabContent(String s)
            {
                return weiboListView;
            }
        }));
    }

    private ListView initNewsListView()
    {
        final ListView listView = new ListView(this);
        adapter = new NewsAdapter(BrowserActivity.this);
        listView.setAdapter(adapter);
        listView.setOnItemClickListener(onItemClickListener);
        listView.setLayoutParams(new FrameLayout.LayoutParams(ViewGroup.LayoutParams.FILL_PARENT, ViewGroup.LayoutParams.FILL_PARENT));
        return listView;
    }

    private ListView initWeiboListView()
    {
        ListView listView = new ListView(this);
        weiboAdapter = new WeiBoAdapater();
        listView.setAdapter(weiboAdapter);
        listView.setLayoutParams(new FrameLayout.LayoutParams(ViewGroup.LayoutParams.FILL_PARENT, ViewGroup.LayoutParams.FILL_PARENT));
        return listView;
    }
    
    @Override
    protected void onResume()
    {
        super.onResume();
        //adapter.setNewsList(null);
        //weiboAdapter.setWeiboList(null);
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

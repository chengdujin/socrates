package cn.com.socrates.view;

import java.io.IOException;

import cn.com.socrates.http.NewsTest;
import cn.com.socrates.oauth.R;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class NewsView extends Activity {
	NewsTest getNewsBody = new NewsTest();
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		Bundle bundle = getIntent().getExtras();
		String title = bundle.getString("Title");
		String link = bundle.getString("Link");
		setContentView(R.layout.news_view_layout);
		TextView t = (TextView)findViewById(R.id.news_view_title);
		TextView b = (TextView)findViewById(R.id.news_view_body);
		t.setText(title.trim());
		try {
			b.setText(getNewsBody.loadHtml(link));
		} catch (IOException e) {
			e.printStackTrace();
		}
		super.onCreate(savedInstanceState);
	}
}

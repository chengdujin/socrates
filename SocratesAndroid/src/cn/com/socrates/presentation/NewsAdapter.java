package cn.com.socrates.presentation;

import android.content.Context;
import android.net.Uri;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.Collections;
import java.util.List;

import cn.com.socrates.model.NewInfo;
import cn.com.socrates.model.WeiBoInfo;
import cn.com.socrates.oauth.R;

public class NewsAdapter extends BaseAdapter
{
    private List<NewInfo> newsList=Collections.emptyList();;//存放频道下新闻的list
	private LayoutInflater mInflater;//布局器
	private Context context;//上下文
	
	public NewsAdapter(Context mcontext){
		this.context=mcontext;
		mInflater=LayoutInflater.from(context);
	}

    public int getCount()
    {
        return newsList.size();
    }

    public NewInfo getItem(int i)
    {
        return newsList.get(i);
    }

    public long getItemId(int i)
    {
        return i; 
    }

    public View getView(int position, View view, ViewGroup viewGroup)
    {
    	ViewHolder viewHolder=null;
    	NewInfo newinfo = newsList.get(position);
		if(view==null){//第一次显示的时候
			view=mInflater.inflate(R.layout.newsitem, null);
			viewHolder=new ViewHolder();
			viewHolder.newstitle=(TextView)view.findViewById(R.id.newsTitle);
			viewHolder.updatetime=(TextView)view.findViewById(R.id.updateTime);
			view.setTag(viewHolder);
		}else{//之前已经显示过，再次显示
			viewHolder=(ViewHolder)view.getTag();
		}
		if(newinfo!=null)
		{
			viewHolder.newstitle.setText(newinfo.getTitle());
			viewHolder.updatetime.setText(newinfo.getPubDate());
		}
		
		return view;
    }
	
	//保存每条新闻的类
	public final class ViewHolder{
		TextView newstitle;//新闻标题
		TextView updatetime;//新闻更新的时间
	}

    public void setNewsList(List<NewInfo> newsList)
    {
        this.newsList = newsList;
        notifyDataSetInvalidated();
    }
}

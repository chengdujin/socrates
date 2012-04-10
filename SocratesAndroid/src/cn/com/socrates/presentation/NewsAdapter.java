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
    private List<NewInfo> newsList=Collections.emptyList();;//���Ƶ�������ŵ�list
	private LayoutInflater mInflater;//������
	private Context context;//������
	
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
		if(view==null){//��һ����ʾ��ʱ��
			view=mInflater.inflate(R.layout.newsitem, null);
			viewHolder=new ViewHolder();
			viewHolder.newstitle=(TextView)view.findViewById(R.id.newsTitle);
			viewHolder.updatetime=(TextView)view.findViewById(R.id.updateTime);
			view.setTag(viewHolder);
		}else{//֮ǰ�Ѿ���ʾ�����ٴ���ʾ
			viewHolder=(ViewHolder)view.getTag();
		}
		if(newinfo!=null)
		{
			viewHolder.newstitle.setText(newinfo.getTitle());
			viewHolder.updatetime.setText(newinfo.getPubDate());
		}
		
		return view;
    }
	
	//����ÿ�����ŵ���
	public final class ViewHolder{
		TextView newstitle;//���ű���
		TextView updatetime;//���Ÿ��µ�ʱ��
	}

    public void setNewsList(List<NewInfo> newsList)
    {
        this.newsList = newsList;
        notifyDataSetInvalidated();
    }
}

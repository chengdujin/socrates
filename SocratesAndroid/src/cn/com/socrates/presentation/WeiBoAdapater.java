package cn.com.socrates.presentation;

import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.Collections;
import java.util.List;

import cn.com.socrates.domian.AsyncImageLoader;
import cn.com.socrates.domian.AsyncImageLoader.ImageCallback;
import cn.com.socrates.domian.NewInfo;
import cn.com.socrates.domian.WeiBoInfo;
import cn.com.socrates.oauth.R;

//Œ¢≤©¡–±ÌAdapater
public class WeiBoAdapater extends BaseAdapter{

	private List<WeiBoInfo> wbList = Collections.emptyList();
    private AsyncImageLoader asyncImageLoader;
    
    public int getCount() {
        return wbList.size();
    }

    public Object getItem(int position) {
        return wbList.get(position);
    }

    public long getItemId(int position) {
        return position;
    }
    
    public void setWeiBoList(List<WeiBoInfo> wbList)
    {
        this.wbList = wbList;
        notifyDataSetInvalidated();
    }
    
    public class WeiBoHolder {
		public ImageView wbimage;
		public ImageView wbicon;
		public TextView wbuser;
		public TextView wbtime;
		public TextView wbtext;
		}

    public View getView(int position, View convertView, ViewGroup parent) {
        asyncImageLoader = new AsyncImageLoader();
        convertView = LayoutInflater.from(parent.getContext()).inflate(R.layout.weibo, null);
        WeiBoHolder wh = new WeiBoHolder();
        wh.wbicon = (ImageView) convertView.findViewById(R.id.wbicon);
        wh.wbtext = (TextView) convertView.findViewById(R.id.wbtext);
        wh.wbtime = (TextView) convertView.findViewById(R.id.wbtime);
        wh.wbuser = (TextView) convertView.findViewById(R.id.wbuser);
        wh.wbimage=(ImageView) convertView.findViewById(R.id.wbimage);
        WeiBoInfo wb = wbList.get(position);
        if(wb!=null){
            convertView.setTag(wb.getId());
            wh.wbuser.setText(wb.getUserName());
            wh.wbtime.setText(wb.getTime());
            wh.wbtext.setText(wb.getText(), TextView.BufferType.SPANNABLE);
//            textHighlight(wh.wbtext,new char[]{'#'},new char[]{'#'});
//            textHighlight(wh.wbtext,new char[]{'@'},new char[]{':',' '});
//            textHighlight2(wh.wbtext,"http://"," ");
            
            if(wb.getHaveImage()){
//                wh.wbimage.setImageResource(R.drawable.images);
            }
            Drawable cachedImage = asyncImageLoader.loadDrawable(wb.getUserIcon(),wh.wbicon, new ImageCallback(){

                public void imageLoaded(Drawable imageDrawable,ImageView imageView, String imageUrl) {
                    imageView.setImageDrawable(imageDrawable);
                }
                
            });
             if (cachedImage == null) {
                 wh.wbicon.setImageResource(R.drawable.usericon);
                }else{
                    wh.wbicon.setImageDrawable(cachedImage);
                }
        }
        
        return convertView;
    }
}

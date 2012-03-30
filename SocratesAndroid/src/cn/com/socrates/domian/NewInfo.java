package cn.com.socrates.domian;

import android.os.Parcel;
import android.os.Parcelable;
import android.os.Parcelable.Creator;

public class NewInfo implements Parcelable{
	private int newsid;//新闻ID，标识这条新闻
	private String title;//新闻标题
	private String link;//新闻链接
	private String author;//新闻作者
	private String pubDate;//新闻发布时间
	private String description;//新闻内容
	private int channel_id;//频道ID,新闻属于哪个频道
	private int read_flag;//0表示未读 1 表示已读
	
	public int getNewsid() {
		return newsid;
	}
	public void setNewsid(int newsid) {
		this.newsid = newsid;
	}
	public int getChannel_id() {
		return channel_id;
	}
	public void setChannel_id(int channelId) {
		channel_id = channelId;
	}
	public int getRead_flag() {
		return read_flag;
	}
	public void setRead_flag(int readFlag) {
		read_flag = readFlag;
	}
	
	public String getTitle() {
		return checkDataToReturn(title);
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public String getLink() {
		return checkDataToReturn(link);
	}
	public void setLink(String link) {
		this.link = link;
	}
	public String getAuthor() {
		return checkDataToReturn(author);
	}
	public void setAuthor(String author) {
		this.author = author;
	}
	public String getPubDate() {
		return checkDataToReturn(pubDate);
	}
	public void setPubDate(String pubDate) {
		this.pubDate = pubDate;
	}
	public String getDescription() {
		return checkDataToReturn(description);
	}
	public void setDescription(String description) {
		this.description = description;
	}
	
	public String checkDataToReturn(String data){
		if(data==null){//xml文件中没有这个标签
			return "NO "+data;
		}else{
			return data.replace("\\n", "");
		}
	}
	
	public static final Parcelable.Creator<NewInfo> CREATOR=new Creator<NewInfo>(){

		@Override
		public NewInfo createFromParcel(Parcel source) {
			// TODO Auto-generated method stub
			NewInfo info=new NewInfo();
			info.newsid=source.readInt();
			info.channel_id=source.readInt();
			info.read_flag=source.readInt();
			info.author=source.readString();
			info.title=source.readString();
			info.link=source.readString();
			info.pubDate=source.readString();
			info.description=source.readString();
			return info;
		}

		@Override
		public NewInfo[] newArray(int size) {
			// TODO Auto-generated method stub
			return new NewInfo[size];
		}
		
	};
	
	@Override
	public int describeContents() {
		// TODO Auto-generated method stub
		return 0;
	}
	@Override
	public void writeToParcel(Parcel dest, int flags) {
		// TODO Auto-generated method stub
		dest.writeInt(newsid);
		dest.writeInt(channel_id);
		dest.writeInt(read_flag);
		dest.writeString(author);
		dest.writeString(title);
		dest.writeString(link);
		dest.writeString(pubDate);
		dest.writeString(description);
	}
}

package cn.com.socrates.data;

import android.content.Context;
import android.content.SharedPreferences;
import android.net.Uri;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.TreeMap;

public class ViewerPreferences
{
    private SharedPreferences sharedPreferences;
    
    private static final String FULL_SCREEN = "FullScreen";
    
    private static final String TARGETNET= "TargetNet";
    
    private static final String AUTHORIZED= "Authorized";
    
    private static final String AUTHORIZE_TYPE= "AuthorizeType";
    
    private static final String NOAUTHORIZE_TYPE= "NoAuthorizeType";
    
    private final static String NOAUTHORIZE_VALUE= "NoAuthorize_Value";
    
    public ViewerPreferences(Context context)
    {
        sharedPreferences = context.getSharedPreferences("ViewerPreferences", 0);
    }

    public void setFullScreen(boolean fullscreen)
    {
        final SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putBoolean(FULL_SCREEN, fullscreen);
        editor.commit();
    }

    public boolean isFullScreen()
    {
        return sharedPreferences.getBoolean(FULL_SCREEN, false);
    }
    
    public String getTargetNet()
    {
    	return sharedPreferences.getString(TARGETNET, "");
    }
    public void setTargetNet(String targetNet)
    {
    	final SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(TARGETNET, targetNet);
        editor.commit();
    }
    
    public void setAuthorized(boolean Authorized)
    {
        final SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putBoolean(AUTHORIZED, Authorized);
        editor.commit();
    }

    public boolean isAuthorized()
    {
        return sharedPreferences.getBoolean(AUTHORIZED, false);
    }
    
    public String getAuthorizeType()
    {
    	return sharedPreferences.getString(AUTHORIZE_TYPE, "");
    }
    public void setAuthorizeType(String AuthorizeTypeStr)
    {
    	final SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(AUTHORIZE_TYPE, AuthorizeTypeStr);
        editor.commit();
    }
    
    public String getNoAuthorizeType()
    {
    	return sharedPreferences.getString(NOAUTHORIZE_TYPE, "");
    }
    public void setNoAuthorizeType(String NoAuthorizeTypeStr)
    {
    	final SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(NOAUTHORIZE_TYPE, NoAuthorizeTypeStr);
        editor.commit();
    }
}

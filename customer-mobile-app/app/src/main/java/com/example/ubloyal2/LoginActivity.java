package com.example.ubloyal2;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.material.textfield.TextInputLayout;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.HttpUrl;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class LoginActivity extends AppCompatActivity {
   private boolean logged_in;
   private String response;
   private Activity ctx;
   public static String auth;
   public static String login_resposne;
   public static int user_id;

    TextInputLayout user_name_layout;
    TextInputLayout password_layout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_PAN);

        logged_in=false;
        response="";
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        ctx=this;

        final Activity cur=this;

        user_name_layout=findViewById(R.id.layout_user);
        password_layout=findViewById(R.id.layout_pass);


        EditText username = findViewById(R.id.username);
        username.setText("45678");

        username.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                user_name_layout.setErrorEnabled(false);
                return false;
            }
        });


        EditText password=  findViewById(R.id.pass);
        password.setText("UBLoyal");

        password.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                password_layout.setErrorEnabled(false);
                return false;
            }
        });


        findViewById(R.id.login).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String user= ((EditText) findViewById(R.id.username)).getText().toString();
                String pass = ((EditText) findViewById(R.id.pass)).getText().toString();

                LoginAPI api=new LoginAPI();
                api.execute(new String[]{
                        "https://webdev.cse.buffalo.edu/rewards/users/auth/login/",
                        user,
                        pass
                });

            }
        });

        findViewById(R.id.reg_click).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(LoginActivity.this, RegisterActivity.class);
                startActivity(intent);

            }
        });


    }

    private class LoginAPI extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {

            MediaType JSON = MediaType.parse("application/json; charset=utf-8");
            JSONObject jsonObject = new JSONObject();

            try {
                jsonObject.put("username", urls[1]);
                jsonObject.put("password", urls[2]);
            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("Login build obj",e.toString());
                Toast.makeText(ctx,"Login failed",Toast.LENGTH_LONG).show();
            }

            OkHttpClient client =new OkHttpClient();

            String url=urls[0];
            RequestBody body = RequestBody.create(JSON, jsonObject.toString());


            HttpUrl.Builder httpBuider = HttpUrl.parse(url).newBuilder();

            Request request = new Request.Builder()
                    .url(httpBuider.build())
                    .post(body)
                    .build();

            Response response = null;
            try {
                response = client.newCall(request).execute();
            } catch (IOException e) {
                e.printStackTrace();
                Log.e("Login response",e.toString());
                Toast.makeText(ctx,"Login failed",Toast.LENGTH_LONG).show();

                return "Download failed"; }

            if(!response.isSuccessful()){
                Log.e("Login API Failed",response.toString());
                try{
                    return response.body().string();
                }
                catch(Exception e){ }

            }


            if (response.isSuccessful()) {
                if (response.body() != null) {
                    try {
                        return response.body().string();
                    } catch (IOException e) {
                        e.printStackTrace();
                        Log.e("Login parse response",e.toString());
                        Toast.makeText(ctx,"Login failed",Toast.LENGTH_LONG).show();

                        return "Download failed";

                    }
                }
            }

            return "Download failed";

        }

    @Override
    protected void onPostExecute(String result) {
            Log.d("Response is",result);
        JSONObject jsonObject = new JSONObject();

        try {
            jsonObject= new JSONObject(result);
        } catch (JSONException e) {
            e.printStackTrace();
            Log.e("Login",e.toString());
            Toast.makeText(ctx,"Login failed: "+result,Toast.LENGTH_LONG).show();
            return;

        }

        try {
            auth=jsonObject.getString("token");
            user_id=jsonObject.getJSONObject("user").getInt("id");
        } catch (JSONException e) {
            e.printStackTrace();
            Log.e("Login",e.toString());
            //Toast.makeText(ctx,"Login failed",Toast.LENGTH_LONG).show();

            try{
                JSONArray obj=jsonObject.getJSONArray("username");
                String retVal="";

                for(int i=0;i<obj.length();i++){
                    retVal+=obj.getString(i)+" ";
                }
                user_name_layout.setError(retVal);
            }
            catch(Exception k){
            }

            try{
                JSONArray obj=jsonObject.getJSONArray("password");
                String retVal="";

                for(int i=0;i<obj.length();i++){
                    retVal+=obj.getString(i)+" ";
                }
                password_layout.setError(retVal);
            }
            catch(Exception k){
            }

            try{
                JSONArray obj=jsonObject.getJSONArray("non_field_errors");
                String retVal="";

                for(int i=0;i<obj.length();i++){
                    retVal+=obj.getString(i)+" ";
                }

                Toast.makeText(ctx,retVal,Toast.LENGTH_LONG).show();

            }
            catch (Exception k){

            }

            return;

        }

        login_resposne=result;
        Intent intent = new Intent(ctx, MainActivity.class);
        intent.putExtra("response",result);
        startActivity(intent);
//        ctx.finish();
    }
}

}

package com.example.ubloyal2;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
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

import okhttp3.HttpUrl;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class RegisterActivity extends AppCompatActivity {

    private EditText t_username;

    private EditText t_password1;

    private Activity atc;

    TextInputLayout user_name_layout;
    TextInputLayout password_layout;
    TextInputLayout phone_layout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_PAN);

        EditText first_name=findViewById(R.id.First_name);
        EditText last_name=findViewById(R.id.Last_name);
        EditText email=findViewById(R.id.email);
        EditText phone=findViewById(R.id.phone_num);
        EditText password2=findViewById(R.id.pass2);
        t_username=findViewById(R.id.username);
        t_password1=findViewById(R.id.pass1);


       user_name_layout=findViewById(R.id.user_layout);
       password_layout=findViewById(R.id.pass_layout);
       phone_layout=findViewById(R.id.phone_layout);


       phone.setOnTouchListener(new View.OnTouchListener() {
           @Override
           public boolean onTouch(View v, MotionEvent event) {
               phone_layout.setErrorEnabled(false);
               return false;
           }
       });


       t_username.setOnTouchListener(new View.OnTouchListener() {
           @Override
           public boolean onTouch(View v, MotionEvent event) {
               user_name_layout.setErrorEnabled(false);
               return false;
           }
       });


       t_password1.setOnTouchListener(new View.OnTouchListener() {
           @Override
           public boolean onTouch(View v, MotionEvent event) {
               password_layout.setErrorEnabled(false);
               return false;
           }
       });

        atc=this;


        Button reg=findViewById(R.id.reg);

        reg.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String  pass1 = ((EditText)(findViewById(R.id.pass1))).getText().toString().trim();
                String  pass2 = ((EditText)(findViewById(R.id.pass2))).getText().toString().trim();

                String first_name=((EditText) findViewById(R.id.First_name)).getText().toString().trim();
                String last_name=((EditText) findViewById(R.id.Last_name)).getText().toString().trim();

                String email=((EditText) findViewById(R.id.email)).getText().toString().trim();

                String phone=((EditText) findViewById(R.id.phone_num)).getText().toString().trim();

                String username=((EditText) findViewById(R.id.username)).getText().toString().trim();


                String[] info=new String[10];
                info[0]="https://webdev.cse.buffalo.edu/rewards/users/";
                info[1]=username;
                info[2]=pass1;
                info[3]=email;
                info[4]=phone;
                info[5]=first_name;
                info[6]=last_name;

                boolean flag=true;

                if(pass1.isEmpty()){
                    password_layout.setError("This field may not be blank.");
                    flag=false;

                }
                else if(!pass1.equals(pass2)){
                    password_layout.setError("Passwords do not match.");
                    flag=false;
                }

                if(username.isEmpty()){
                    user_name_layout.setError("This field may not be blank.");
                    flag=false;
                }

                if(!flag){
                    return;
                }

                RegAPI regAPI=new RegAPI();
                regAPI.execute(info);


            }
        });


    }
    private class RegAPI extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {

            MediaType JSON = MediaType.parse("application/json; charset=utf-8");
            JSONObject jsonObject = new JSONObject();

            try {
                jsonObject.put("username", urls[1]);
                jsonObject.put("password", urls[2]);
                jsonObject.put("email",urls[3]);
                jsonObject.put("phone",urls[4]);
                jsonObject.put("first_name",urls[5]);
                jsonObject.put("last_name",urls[6]);
            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("Login build obj",e.toString());
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
                Log.e("Reg response",e.toString());
                Toast.makeText(getApplicationContext(),"Reg failed with reason: "+e.toString(),Toast.LENGTH_LONG).show();
                return "Reg failed";
            }

            if(!response.isSuccessful()){
                Log.e("Reg API Failed",response.toString());
                try{
                    return response.body().string();
                }
                catch(Exception e){
                    return "API Failed to parse body";
                }

            }

            if (response.isSuccessful()) {
                if (response.body() != null) {
                    try {
                        return response.body().string();
                    } catch (IOException e) {
                        e.printStackTrace();
                        Log.e("Login parse response",e.toString());

                    }
                }
            }

            return response.toString();

        }

        @Override
        protected void onPostExecute(String result){
            Log.d("Response is",result);
            JSONObject jsonObject = new JSONObject();

            try {
                jsonObject= new JSONObject(result);
            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("Reg",e.toString());
                Toast.makeText(getApplicationContext(),"Reg failed: "+result,Toast.LENGTH_LONG).show();
                return;
            }

            try {
                LoginActivity.auth=jsonObject.getString("token");
            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("Reg",e.toString());

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
                    JSONArray obj=jsonObject.getJSONArray("phone");
                    String retVal="";

                    for(int i=0;i<obj.length();i++){
                        retVal+=obj.getString(i)+" ";
                    }
                    phone_layout.setError(retVal);
                }
                catch(Exception k){
                }

//                Toast.makeText(getApplicationContext(),"Reg failed: "+result,Toast.LENGTH_LONG).show();
                return;
            }


            LoginAPI loginAPI=new LoginAPI();
            loginAPI.execute(new String[] {
                    "https://webdev.cse.buffalo.edu/rewards/users/auth/login/",
                    t_username.getText().toString().trim(),t_password1.getText().toString().trim()
            });


        }
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
                Toast.makeText(getApplicationContext(),"Login failed",Toast.LENGTH_LONG).show();
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
                Toast.makeText(getApplicationContext(),"Login failed",Toast.LENGTH_LONG).show();

                return "Download failed";
            }


            if(!response.isSuccessful()){
                Log.e("Login API Failed",response.toString());
                return response.toString();
            }


            if (response.isSuccessful()) {
                if (response.body() != null) {
                    try {
                        return response.body().string();
                    } catch (IOException e) {
                        e.printStackTrace();
                        Log.e("Login parse response",e.toString());
                        Toast.makeText(getApplicationContext(),"Login failed",Toast.LENGTH_LONG).show();

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
                //Toast.makeText(getApplicationContext(),"Login failed",Toast.LENGTH_LONG).show();
                return;

            }

            try {
                LoginActivity.auth=jsonObject.getString("token");
                LoginActivity.user_id=jsonObject.getJSONObject("user").getInt("id");
                Toast.makeText(getApplicationContext(),"Registration and Login Successful!",Toast.LENGTH_LONG).show();


            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("Login",e.toString());
                //Toast.makeText(getApplicationContext(),"Login failed",Toast.LENGTH_LONG).show();
                return;

            }

            LoginActivity.login_resposne=result;
            Intent intent = new Intent(getApplicationContext(), MainActivity.class);
            intent.putExtra("response",result);
            startActivity(intent);
            atc.finish();
        }
    }

}

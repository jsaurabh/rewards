package com.example.ubloyal2.nav_bar.profile;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProviders;

import com.example.ubloyal2.LoginActivity;
import com.example.ubloyal2.R;
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

public class ProfileFragment extends Fragment {

    private ProfileViewModel profileViewModel;

    View deleteDialogView;
    AlertDialog deleteDialog;

    TextInputLayout layout_cur;
    TextInputLayout layout_newPass;
    TextInputLayout layout_newPassConfirm;

    TextInputLayout layout_phone;
    TextInputLayout layout_username;


    EditText user;
    EditText first_name;
    EditText last_name;
    EditText email;
    EditText phone_numer;


    Activity ctx;



    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        profileViewModel =
                ViewModelProviders.of(this).get(ProfileViewModel.class);
        View root = inflater.inflate(R.layout.fragment_profile, container, false);

        ctx=getActivity();

        getActivity().getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_PAN);

        String myDataFromActivity = LoginActivity.login_resposne;
        Log.d("login ",myDataFromActivity);
        JSONObject jsonObject = new JSONObject();


        try {
            jsonObject= new JSONObject(myDataFromActivity);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        root.findViewById(R.id.logout).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                LoginActivity.auth="";
                LoginActivity.login_resposne="";
                LoginActivity.user_id=0;
                startActivity(new Intent(v.getContext(),LoginActivity.class));
                ctx.finish();

            }
        });

        user=root.findViewById(R.id.username);
        first_name=root.findViewById(R.id.First_name);
        last_name=root.findViewById(R.id.Last_name);
        email=root.findViewById(R.id.email);
        phone_numer=root.findViewById(R.id.phone_num);

        layout_phone=root.findViewById(R.id.layout_phone);
        layout_username=root.findViewById(R.id.layout_user_id);

        try{

            String email_set= jsonObject.getJSONObject("user").getString("email");
            if(email_set!=null && !email_set.isEmpty()){
                email.setText(email_set);
            }

            String username_set= jsonObject.getJSONObject("user").getString("username");
            user.setText(username_set);

            first_name.setText(jsonObject.getJSONObject("user").getString("first_name"));
            last_name.setText(jsonObject.getJSONObject("user").getString("last_name"));

            String temp=jsonObject.getJSONObject("user").getString("phone");
            if(temp!= null && !temp.isEmpty() && !temp.equals("null")){
                phone_numer.setText(jsonObject.getJSONObject("user").getString("phone"));
            }


        }
        catch(Exception k){

        }

        user.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                layout_username.setErrorEnabled(false);
                return false;
            }
        });

        phone_numer.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                layout_phone.setErrorEnabled(false);
                return false;
            }
        });

        JSONObject update = new JSONObject();

        try{
            update.put("username",user.getText().toString().trim());
            update.put("first_name",first_name.getText().toString().trim());
            update.put("last_name",last_name.getText().toString().trim());
            update.put("email",email.getText().toString().trim());
            update.put("phone",phone_numer.getText().toString().trim());
        }
        catch (Exception e){

        }

        root.findViewById(R.id.update).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String u_fs=user.getText().toString().trim();

                String[] data= new String[] {
                        "https://webdev.cse.buffalo.edu/rewards/users/"+LoginActivity.user_id+"/",
                        user.getText().toString().trim(),
                        first_name.getText().toString().trim(),
                        last_name.getText().toString().trim(),
                        email.getText().toString().trim(),
                        phone_numer.getText().toString().trim()
                };

                UpdateAPI api=new UpdateAPI();
                api.execute(data);

            }
        });

        root.findViewById(R.id.update_pass).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                getActivity().getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_PAN);

                LayoutInflater factory = LayoutInflater.from(v.getContext());
                deleteDialogView = factory.inflate(R.layout.password_dialog, null);

                layout_cur=deleteDialogView.findViewById(R.id.pass_layout1);
                layout_newPass=deleteDialogView.findViewById(R.id.pass_layout2);
                layout_newPassConfirm=deleteDialogView.findViewById(R.id.pass_layout3);

                final EditText currPass= deleteDialogView.findViewById(R.id.pass1);
                final EditText newPass = deleteDialogView.findViewById(R.id.pass2);
                final EditText newPassConfirm = deleteDialogView.findViewById(R.id.pass3);

                currPass.setOnTouchListener(new View.OnTouchListener() {
                    @Override
                    public boolean onTouch(View v, MotionEvent event) {
                        layout_cur.setErrorEnabled(false);
                        return false;
                    }
                });

                newPass.setOnTouchListener(new View.OnTouchListener() {
                    @Override
                    public boolean onTouch(View v, MotionEvent event) {
                        layout_newPass.setErrorEnabled(false);
                        layout_newPassConfirm.setErrorEnabled(false);
                        return false;
                    }
                });


                deleteDialog = new AlertDialog.Builder(v.getContext()).create();
                deleteDialog.setView(deleteDialogView);

                deleteDialogView.findViewById(R.id.cancel_button).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        deleteDialog.dismiss();
                    }
                });

                deleteDialogView.findViewById(R.id.update_pass_button).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        //your business logic

                        String pass=currPass.getText().toString().trim();
                        String pass_new=newPass.getText().toString().trim();
                        String pass_new_confirm=newPassConfirm.getText().toString().trim();

                        boolean flag=true;

                        if(pass.isEmpty()){
                            layout_cur.setError("This field may not be blank.");
                            flag=false;
                        }

                        if(pass_new.isEmpty()){
                            layout_newPass.setError("This field may not be blank.");
                            flag=false;
                        }
                        else if(!pass_new.equals(pass_new_confirm)){
                            layout_newPass.setError("Passwords do not match.");
                            flag=false;
                        }

                        if(!flag){
                            return;
                        }

                        String url="https://webdev.cse.buffalo.edu/rewards/users/auth/change-password/";

                        PasswordAPI passwordAPI=new PasswordAPI();
                        passwordAPI.execute(new String[] {
                                url,currPass.getText().toString().trim(),newPass.getText().toString().trim()
                        });

                        //deleteDialog.dismiss();
                    }
                });

                deleteDialog.show();

            }
        });

        return root;
    }

    private class PasswordAPI extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {

            MediaType JSON = MediaType.parse("application/json; charset=utf-8");
            JSONObject jsonObject = new JSONObject();

            try {
                jsonObject.put("current_password", urls[1]);
                jsonObject.put("new_password", urls[2]);

            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("Update Password API Failed",e.toString());

            }

            OkHttpClient client =new OkHttpClient();

            String url=urls[0];
            RequestBody body = RequestBody.create(JSON, jsonObject.toString());

            HttpUrl.Builder httpBuider = HttpUrl.parse(url).newBuilder();

            Request request = new Request.Builder()
                    .url(httpBuider.build()).addHeader("authorization","token "+LoginActivity.auth)
                    .post(body)
                    .build();


            Response response = null;
            try {
                response = client.newCall(request).execute();
            } catch (IOException e) {
                e.printStackTrace();
                Log.e("Login response",e.toString());
                return "Download failed"; }

            if (response.isSuccessful()) {
                return "It worked";
            }

            try{
                return response.body().string();
            }
            catch (Exception e){
            }



            return "Download failed";

        }

        @Override
        protected void onPostExecute(String result) {
            Log.d("Response is",result);
            JSONObject jsonObject;

            if(result.equals("It worked")){
                Toast.makeText(ctx, "Password Updated Successfully!", Toast.LENGTH_LONG).show();
                deleteDialog.dismiss();
                return;
            }

            try {
                jsonObject= new JSONObject(result);
            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("Login",e.toString());
                return;
            }

                try{
                    JSONArray obj=jsonObject.getJSONArray("current_password");
                    String retVal="";

                    for(int i=0;i<obj.length();i++){
                        retVal+=obj.getString(i)+" ";
                    }
                    layout_cur.setError(retVal);
                }
                catch(Exception k){
                }

                try{
                    JSONArray obj=jsonObject.getJSONArray("new_password");
                    String retVal="";

                    for(int i=0;i<obj.length();i++){
                        retVal+=obj.getString(i)+" ";
                    }
                    layout_newPass.setError(retVal);
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
//        ctx.finish();
        }

    private class UpdateAPI extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {

            MediaType JSON = MediaType.parse("application/json; charset=utf-8");

            JSONObject update = new JSONObject();

            try {
                update.put("username",user.getText().toString().trim());
                update.put("first_name",first_name.getText().toString().trim());
                update.put("last_name",last_name.getText().toString().trim());
                update.put("email",email.getText().toString().trim());
                update.put("phone",phone_numer.getText().toString().trim());

            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("Update Password API Failed",e.toString());

            }

            OkHttpClient client =new OkHttpClient();

            String url=urls[0];
            RequestBody body = RequestBody.create(JSON, update.toString());

            HttpUrl.Builder httpBuider = HttpUrl.parse(url).newBuilder();

            Request request = new Request.Builder()
                    .url(httpBuider.build()).addHeader("authorization","token "+LoginActivity.auth)
                    .put(body)
                    .build();


            Response response = null;
            try {
                response = client.newCall(request).execute();
            } catch (IOException e) {
                e.printStackTrace();
                Log.e("Login response",e.toString());
                return "Download failed"; }

            String s="";

            try{
                s=response.body().string();
            }
            catch (Exception q){}


            if (response.isSuccessful()) {

                try{
                    String u=response.body().string();
                    return "!!"+u;
                }
                catch(Exception e){ }
            }

            try{
                return response.body().string();
            }
            catch (Exception e){

                e.toString();
            }

            return s;

        }

        @Override
        protected void onPostExecute(String result) {
            Log.d("Response is",result);
            JSONObject jsonObject;


            try {
                jsonObject= new JSONObject(result);
            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("Login",e.toString());
                return;
            }


            if(result.contains("!!")){
                Toast.makeText(ctx, "Profile Updated Successfully!", Toast.LENGTH_LONG).show();
                update_data(result.substring(2));
                return;
            }

            try{
                jsonObject.getInt("id");
                Toast.makeText(ctx, "Profile Updated Successfully!", Toast.LENGTH_LONG).show();
                return;
            }
            catch (Exception e){

            }



            try{
                JSONArray obj=jsonObject.getJSONArray("username");
                String retVal="";

                for(int i=0;i<obj.length();i++){
                    retVal+=obj.getString(i)+" ";
                }

                layout_username.setError(retVal);
            }
            catch(Exception k){ }

            try{
                JSONArray obj=jsonObject.getJSONArray("phone");
                String retVal="";

                for(int i=0;i<obj.length();i++){
                    retVal+=obj.getString(i)+" ";
                }
                layout_phone.setError(retVal);
            }
            catch(Exception k){ }

            try{
                JSONArray obj=jsonObject.getJSONArray("non_field_errors");
                String retVal="";

                for(int i=0;i<obj.length();i++){
                    retVal+=obj.getString(i)+" ";
                }

                Toast.makeText(ctx,retVal,Toast.LENGTH_LONG).show();

            }
            catch (Exception k){ }

            return;

        }
//        ctx.finish();
    }

    public void update_data(String s){

    }


}
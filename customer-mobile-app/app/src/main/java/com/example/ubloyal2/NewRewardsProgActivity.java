package com.example.ubloyal2;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;


import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class NewRewardsProgActivity extends AppCompatActivity {

    private ListView listView;

    ArrayList<String> title=new ArrayList<String>();
    ArrayList<String> address=new ArrayList<String>();
    ArrayList<String> phone_number=new ArrayList<String>();
    ArrayList<String> url=new ArrayList<String>();
    ArrayList<String> img=new ArrayList<String>();
    ArrayList<Integer> bus_id=new ArrayList<Integer>();
    Intent toSend;

    int pos_clicked;

    boolean flag=false;

    private MyAdapter adapter;

    Activity c_this;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_new_rewards_prog);

        toSend=new Intent(this,MainActivity.class);

        c_this=this;

        listView=findViewById(R.id.red);

        API api=new API();
        api.execute(new String[]{
                "https://webdev.cse.buffalo.edu/rewards/programs/businesses/?not-customer",

        });

        while(!title.isEmpty()){

        }

        MyAdapter adapter=new MyAdapter(this, title,address,phone_number,url,img);

        listView.setAdapter(adapter);


        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, final View view, final int position, long id) {


                new AlertDialog.Builder(c_this)
                        .setTitle("Add  Business")
                        .setMessage("Are you sure you want to add "+title.get(position) +" to your reward programs?")

                        // Specifying a listener allows you to take an action before dismissing the dialog.
                        // The dialog is automatically dismissed when a dialog button is clicked.
                        .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int which) {
                                // Continue with delete operation
                                pos_clicked=position;
                                JoinEndpoint joinEndpoint=new JoinEndpoint();
                                joinEndpoint.execute(new String[]{
                                        "https://webdev.cse.buffalo.edu/rewards/programs/join/"+bus_id.get(position)+"/"
                                });

                            }
                        })

                        // A null listener allows the button to dismiss the dialog and take no further action.
                        .setNegativeButton(android.R.string.no, null)
                        .setIcon(android.R.drawable.ic_dialog_alert)
                        .show();
            }
        });


    }

    class MyAdapter extends ArrayAdapter<String>{

        Context context;
        ArrayList<String> r_title;
        ArrayList<String> r_address;
        ArrayList<String> r_phone_number;
        ArrayList<String> r_url;
        ArrayList<String> r_img;


        MyAdapter(Context c, ArrayList<String> title, ArrayList<String> addy, ArrayList<String>  phone, ArrayList<String> url, ArrayList<String> img){
            super(c,R.layout.new_business,title);
            this.context=c;
            r_title=title;
            r_address=addy;
            r_phone_number=phone;
            r_url=url;
            r_img=img;

        }

        @NonNull
        @Override
        public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {

            LayoutInflater layoutInflater= (LayoutInflater) getApplicationContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);

            View row=layoutInflater.inflate(R.layout.new_business,parent,false);
            ImageView imageView= row.findViewById(R.id.logo);

            String img_temp=r_img.get(position);

            Picasso.get().load(r_img.get(position)).into(imageView);

            ((TextView) row.findViewById(R.id.name)).setText(r_title.get(position));

            ((TextView) row.findViewById(R.id.address)).setText(r_address.get(position));

            TextView tv = ((TextView) row.findViewById(R.id.url1));
            String url_one=r_url.get(position);

            tv.setText(Html.fromHtml("<a href="+url_one+"> Website"));
            tv.setMovementMethod(LinkMovementMethod.getInstance());
            tv.setTextColor(0xFF000000);
            tv.setFocusable(false);

            ((TextView) row.findViewById(R.id.phone_number)).setText(r_phone_number.get(position));

            return row;
        }
    }


    private class API extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {

            OkHttpClient client =new OkHttpClient();

            String url=urls[0];

            Request request = new Request.Builder()
                    .url(url).addHeader("authorization","token "+LoginActivity.auth)
                    .get()
                    .build();

            Response response = null;

            try {
                response = client.newCall(request).execute();
            } catch (IOException e) {
                e.printStackTrace();
            }


            if(!response.isSuccessful()){
                Log.e("Get all business API Failed",response.toString());
                try{
                    return response.body().string();
                }
                catch(Exception c){ }

            }


            if (response.isSuccessful()) {
                if (response.body() != null) {
                    try {
                        return response.body().string();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }

            return "API failed";

        }

        @Override
        protected void onPostExecute(String result) {

            Log.d("RewRewardsProg ",result);

            JSONArray jsonObject = new JSONArray();

            try {
                jsonObject= new JSONArray(result);
            } catch (JSONException e) {
                e.printStackTrace();
                Toast.makeText(c_this,"Login failed: "+result,Toast.LENGTH_LONG).show();
            }

            // [{"id":1,"name":"Craft Coffee House","is_published":null,"phone":"(716) 210-3546","url":"https://www.facebook.com/Craftcoffeehouse/","address":"6535 Campbell Blvd,\r\nLockport,\r\nNY 14094","logo":null},{"id":3,"name":"Starbucks Coffee Company","is_published":true,"phone":"800-782-7282","url":"https://www.starbucks.com/","address":"Somewhere, ON, Earth","logo":"http://webdev.cse.buffalo.edu:8000/rewards/media/programs/businesses/logos/Starbucks_Corporation_Logo_2011.png"},{"id":4,"name":"Tim Hortons","is_published":true,"phone":"1-888-601-1616","url":"https://www.timhortons.com/us/en/index.php","address":"","logo":"http://webdev.cse.buffalo.edu:8000/rewards/media/programs/businesses/logos/Tim_Hortons_logo.png"}]

            try {

                for (int i = 0; i < jsonObject.length(); ++i) {

                    JSONObject temp=jsonObject.getJSONObject(i);
                    title.add(temp.getString("name"));
                    address.add(temp.getString("address"));
                    phone_number.add(temp.getString("phone"));
                    url.add(temp.getString("url"));
                    img.add(temp.getString("logo"));
                    bus_id.add(temp.getInt("id"));
                }

                adapter=new MyAdapter(c_this, title,address,phone_number,url,img);
                listView.setAdapter(adapter);


            }
            catch (Exception e){

            }

//            String val= jsonObject.getJSONObject("user").getString("id");
//
//
//            Intent intent = new Intent(ctx, MainActivity.class);
//            intent.putExtra("response",result);
//            startActivity(intent);
        }
    }

    private class JoinEndpoint extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {

            OkHttpClient client =new OkHttpClient();

            String url=urls[0];

            Request request = new Request.Builder()
                    .url(url).addHeader("authorization","token "+LoginActivity.auth).addHeader("Content-Length","0")
                    .post(RequestBody.create(null,""))
                    .build();

            Response response = null;

            try {
                response = client.newCall(request).execute();
            } catch (IOException e) {
                e.printStackTrace();
                return "API failed";
            }

            if(response.code()>200 && response.code() < 200){
                Log.e("Get all business API Failed",response.toString());
                return response.toString();
            }


            if (response.isSuccessful()) {
                if (response.body() != null) {
                    try {
//                        Log.d("new bus",response.body().string());
//                        String s=response.body().string();
                        return "it worked";
                    } catch (Exception e) {
                        e.printStackTrace();
                        return "API failed";
                    }
                }
            }

            return "API failed";

        }

        @Override
        protected void onPostExecute(String result) {

            Log.d("RewRewardsProg ",result);

            if(!result.equals("API failed")){
                Toast.makeText(c_this,title.get(pos_clicked)+" has been added!",Toast.LENGTH_SHORT).show();
                title.remove(pos_clicked);
                address.remove(pos_clicked);
                phone_number.remove(pos_clicked);
                url.remove(pos_clicked);
                bus_id.remove(pos_clicked);
                img.remove(pos_clicked);

                adapter.notifyDataSetChanged();

                startActivity(toSend);
                c_this.finish();

            }
            else{
                Toast.makeText(c_this,"Error in adding business",Toast.LENGTH_LONG).show();

            }

        }
    }


}

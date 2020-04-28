package com.example.ubloyal2;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.app.AlertDialog;
import android.app.Fragment;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.content.Context;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.util.JsonReader;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class ExpandBusiness extends AppCompatActivity {

    String business_name;
    String rp;
    //ListView rew_list;

    View deleteDialogView;
    AlertDialog deleteDialog;

    int business_id;


    ArrayList<String> reward_titles=new ArrayList<>();
    ArrayList<Integer> reward_value=new ArrayList<>();
    ArrayList<String> reward_logos=new ArrayList<>();

    ArrayList<Currency> currencies=new ArrayList<>();

    int value;

    String rewards_string;

    ArrayList<String> history_data=new ArrayList<>();

    int curency_id;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_expand_business);

//        i.putExtra("business_name",name);
//        i.putExtra("bus_id",bus_id.get(parent_pos));
//        i.putExtra("addy",r_address.get(parent_pos));
//        i.putExtra("phone",r_phone_number.get(parent_pos));
//        i.putExtra("link",r_url.get(parent_pos));
//        i.putExtra("logo",r_img.get(parent_pos));
//
//        i.putExtra("currency_id",cur.get(position).id);
//        i.putExtra("currency_val",cur.get(position).val);
//        i.putExtra("currency_rewards",cur.get(position).rewards);
//        i.putExtra("currency_name",cur.get(position).name);


        business_id = getIntent().getIntExtra("bus_id",-1);
        business_name = getIntent().getStringExtra("business_name");

//        curency_id=getIntent().getIntExtra("currency_id",-1);
//        value=getIntent().getIntExtra("currency_val",-1);
//        rewards_string=getIntent().getStringExtra("currency_rewards");

        String temp_string=getIntent().getStringExtra("currency_string");

        try {
            setCurrencies(temp_string);
        } catch (Exception e) {
            e.printStackTrace();
        }


        ArrayList<String> currency_strings=new ArrayList<>();

        for(Currency c:currencies){
            currency_strings.add(c.toString());
        }

        String list_data=getIntent().getStringExtra("list");

//        try {
//            parseRewards();
//        } catch (JSONException e) {
//            e.printStackTrace();
//        }

        rp = getIntent().getStringExtra("rp");

        String addy = getIntent().getStringExtra("addy");
        String phone = getIntent().getStringExtra("phone");
        String link = getIntent().getStringExtra("link");
        String logo=getIntent().getStringExtra("logo");



        ImageView imageView= findViewById(R.id.logo);

        Picasso.get().load(logo).into(imageView);

        TextView tv = ((TextView) findViewById(R.id.url));

        tv.setText(Html.fromHtml("<a href="+link+"> Website"));
        tv.setMovementMethod(LinkMovementMethod.getInstance());

        ((TextView) findViewById(R.id.address)).setText(addy);
        ((TextView) findViewById(R.id.phone_number)).setText(phone);

        ((TextView) findViewById(R.id.name)).setText(business_name);
        //((TextView) findViewById(R.id.camp_rp)).setText("Balance: "+value+ " "+currency_name);

//        Button history = (Button) findViewById(R.id.history);
//
//        history.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//
//                LayoutInflater factory = LayoutInflater.from(v.getContext());
//                deleteDialogView = factory.inflate(R.layout.new_dialog, null);
//
//                deleteDialog = new AlertDialog.Builder(v.getContext()).create();
//                deleteDialog.setView(deleteDialogView);
//
//                deleteDialogView.findViewById(R.id.button2).setOnClickListener(new View.OnClickListener() {
//                    @Override
//                    public void onClick(View v) {
//                        //your business logic
//                        deleteDialog.dismiss();
//                    }
//                });
//
//                ListView his_list = (ListView) deleteDialogView.findViewById(R.id.his);
//
//                ArrayAdapter<String> his_adp = new ArrayAdapter<String>(
//                        v.getContext(),
//                        android.R.layout.simple_list_item_1
//                        , history_data
//                );
//
//                ((TextView) deleteDialogView.findViewById(R.id.camp_name)).setText("Balance: "+value+ " "+currency_name);
//                ((TextView) deleteDialogView.findViewById(R.id.buss_name)).setText(business_name);
//
//                his_list.setAdapter(his_adp);
//                deleteDialog.show();
//            }
//        });

        //rew_list = findViewById(R.id.rewards_list);

       // MyAdapter adp=new MyAdapter(this,reward_titles,reward_value,reward_logos);
        //rew_list.setAdapter(adp);


        Spinner dynamicSpinner = (Spinner) findViewById(R.id.spinner);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_spinner_item, currency_strings);

        dynamicSpinner.setAdapter(adapter);


        dynamicSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {

                Bundle args = new Bundle();
                Currency obj=currencies.get(position);
                args.putInt("currency_id",obj.id);
                args.putString("rewards",obj.rewards);
                args.putInt("value",obj.val);
                args.putString("name",obj.name);
                args.putString("business_name",business_name);

                CurrencyFragment curFrag=new CurrencyFragment();
                curFrag.setArguments(args);

                FragmentManager manager = getFragmentManager();
                FragmentTransaction transaction = manager.beginTransaction();



                Fragment fragmentA = manager.findFragmentByTag("Cur");
                if (fragmentA == null) {
                    transaction.add(R.id.frag_layout,curFrag,"Cur");
//                    transaction.addToBackStack(null);

                } else {
                    transaction.replace(R.id.frag_layout,curFrag,"Cur");
//                    transaction.addToBackStack(null);
                }

                transaction.commit();



            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {

            }
        });


        String url="https://webdev.cse.buffalo.edu/rewards/rewards/history/?customer="+LoginActivity.user_id+"&currency="+curency_id;

       API api=new API();
       api.execute(new String[]{url});

    }

    public void parseRewards() throws JSONException {

        JSONArray arry=new JSONArray(rewards_string);

//            [
//            {
//                "id": 1,
//                    "reward": "Free coffee",
//                    "image": "/media/rewards/starbucks-coffee.jpg",
//                    "value": 5,
//                    "campaign": 2
//            }
//        ]

        for(int i=0;i<arry.length();i++){
            JSONObject cur=arry.getJSONObject(i);
            String rev_name=cur.getString("reward");
            String logo=cur.getString("image");
            int points_cur=cur.getInt("value");

            reward_titles.add(rev_name);
            reward_logos.add(logo);
            reward_value.add(points_cur);

        }

    }

//    class MyAdapter extends ArrayAdapter<String> {
//
//        Context context;
//        ArrayList<String> reward_titles;
//        ArrayList<Integer> reward_value;
//        ArrayList<String> reward_logos;
//
//        MyAdapter(Context c, ArrayList<String> title, ArrayList<Integer> values,ArrayList<String> images) {
//            super(c, R.layout.progress, title);
//            this.context = c;
//            reward_titles=title;
//            reward_value=values;
//            reward_logos=images;
//
//        }
//
//        @NonNull
//        @Override
//        public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
//
//            LayoutInflater layoutInflater = (LayoutInflater) getApplicationContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
//
//            View row = layoutInflater.inflate(R.layout.progress, parent, false);
//
//            ProgressBar text = row.findViewById(R.id.progressBar);
//
//
//            Double reward_val=new Double(reward_value.get(position));
//            Double total_points=new Double(value);
//
//            int num= (int) Math.round((total_points/reward_val)*100);
//
//            text.setProgress(num);
//
//            if(num>=100){
//                text.setProgressTintList(ColorStateList.valueOf(0xFF4CAF50));
//            }
//            else{
//                //text.setProgressBackgroundTintList(ColorStateList.valueOf(R.color.colorPrimary));
//                //text.setProgressBackgroundTintList(getResources().getColorStateList(R.color.colorPrimary));
//                text.setProgressTintList(ColorStateList.valueOf(0xFF1281D5));
//            }
//
//          //  ((TextView) row.findViewById(R.id.reward_name)).setText(reward_titles.get(position)+": "+reward_value.get(position)+ " "+currency_name);
//
//            ImageView imageView= row.findViewById(R.id.logo);
//
//            String img_url="https://webdev.cse.buffalo.edu"+reward_logos.get(position);
//
//            Picasso.get().load(img_url).into(imageView);
//
//            return row;
//        }
//
//
//    }

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
                return "API failed";
            }
            if (response.isSuccessful()) {
                if (response.body() != null) {
                    try {
                        return response.body().string();
                    } catch (IOException e) {
                        e.printStackTrace();
                        return "API failed";
                    }
                }
            }

            return "API failed";

        }

        @Override
        protected void onPostExecute(String result) {

            Log.d("Result Rewards ",result);

            if(result.equals("API failed")){
                return;
            }
            try {
                //setup(result);
            } catch (Exception e) {
                e.printStackTrace();
            }
            return;

        }
    }

//    private void setup(String s) throws JSONException{
//
////        "[\n" +
////                "    {\n" +
////                "        \"created_at\": \"2019-11-14T07:45:43Z\",\n" +
////                "        \"reward\": \"free drink\",\n" +
////                "        \"value\": -20\n" +
////                "    },"
//
//        JSONArray jr=new JSONArray(s);
//
//        for(int i=0;i<jr.length();i++){
//            JSONObject cur=jr.getJSONObject(i);
//            String created=cur.getString("created_at");
//            String reward="";
//            String exp="";
//            int val_t=0;
//
//            try{
//                reward=cur.getString("reward");
//            }
//            catch (Exception e){
//                exp=cur.getString("expires_at");
//            }
//
//            val_t=cur.getInt("value");
//
//            String full="";
//
//            if(reward.isEmpty()){
//
//               full = "Date: "+created+"\n"+
//                       "Expiry Date: "+exp+"\n"+
//                        val_t+" "+currency_name;
//
//            }
//            else{
//
//                full = "Date: "+created+"\n"+
//                        "Reward Redeemed: "+reward+"\n"+
//                        val_t+" "+currency_name;
//            }
//
//            history_data.add(full);
//
//        }
//
//        history_data.size();
//
//    }


    public void setCurrencies(String s) throws Exception{

        JSONArray jso = new JSONArray(s);

        for(int i=0;i<jso.length();i++){
            JSONObject cur=jso.getJSONObject(i);

            int points_total=cur.getInt("accumulated");
            JSONObject curObj=cur.getJSONObject("currency");

            Currency temp=new Currency(points_total,curObj.getString("plural_label"),curObj.getInt("id"),cur.getJSONArray("rewards").toString());
            currencies.add(temp);
        }


    }


    private class Currency {

        private int val;
        private String name;
        private int id;
        private String rewards;

        public int getVal() {
            return val;
        }

        public void setVal(int val) {
            this.val = val;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public int getId() {
            return id;
        }

        public void setId(int id) {
            this.id = id;
        }

        public String getRewards() {
            return rewards;
        }

        public void setRewards(String rewards) {
            this.rewards = rewards;
        }

        @NonNull
        @Override
        public String toString() {
            return val+" "+name;
        }

        public Currency(int t_val, String _name, int _id, String t_rewards){
            val=t_val;
            name=_name;
            id=_id;
            rewards=t_rewards;
        }

    }


}
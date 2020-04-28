package com.example.ubloyal2.nav_bar.rewards;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProviders;

import com.example.ubloyal2.ExpandBusiness;
import com.example.ubloyal2.LoginActivity;
import com.example.ubloyal2.NewRewardsProgActivity;
import com.example.ubloyal2.R;
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class RewardsFragment extends Fragment {

    private static RewardsViewModel rewardsViewModel;

    ArrayList<String> title=new ArrayList<String>();
    ArrayList<String> address=new ArrayList<String>();
    ArrayList<String> phone_number=new ArrayList<String>();
    ArrayList<String> url=new ArrayList<String>();
    ArrayList<String> img=new ArrayList<String>();
    ArrayList<Integer> bus_id=new ArrayList<Integer>();
    HashMap<Integer,ArrayList<Currency>> currencies=new HashMap<>();
    HashMap<Integer,String> currency_data=new HashMap<>();

    MyAdapter adapter;
    ListView listView;

    int user_id=0;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        rewardsViewModel =
                ViewModelProviders.of(this).get(RewardsViewModel.class);
        View root = inflater.inflate(R.layout.fragment_rewards, container, false);

        title.clear();address.clear();address.clear();phone_number.clear();url.clear();img.clear();bus_id.clear();

        listView=root.findViewById(R.id.listView);
        adapter=new MyAdapter(getActivity(), title,address,phone_number,url,img,currencies);

//        API api=new API();
//        api.execute(new String[]{
//                "https://webdev.cse.buffalo.edu/rewards/users/"+LoginActivity.user_id+"/"
//        });

        Button addButton= root.findViewById(R.id.add_button);

        addButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getContext(), NewRewardsProgActivity.class);
                startActivity(intent);
            }
        });


        //listView.setClickable(false);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Intent i=new Intent(getActivity(), ExpandBusiness.class);

                int parent_pos=position;

                i.putExtra("business_name",title.get(position));
                i.putExtra("bus_id",bus_id.get(parent_pos));
                i.putExtra("addy",address.get(parent_pos));
                i.putExtra("phone",phone_number.get(parent_pos));
                i.putExtra("link",url.get(parent_pos));
                i.putExtra("logo",img.get(parent_pos));

                int bus_id_cur=bus_id.get(position);
//                i.putExtra("currency_id",cur.get(position).id);
//                i.putExtra("currency_val",cur.get(position).val);
//                i.putExtra("currency_rewards",cur.get(position).rewards);
//                i.putExtra("currency_name",cur.get(position).name);

             //   i.putExtra("list",cur.toString());

                i.putExtra("currency_string",currency_data.get(bus_id_cur));

                startActivity(i);


            }
        });


        return root;
    }

    public void setup(String result) throws Exception{

        JSONObject jsonObject = new JSONObject(result);
        JSONArray comp = jsonObject.getJSONArray("customer_of");

        for (int i = 0; i < comp.length(); ++i) {

            JSONObject temp = comp.getJSONObject(i);
            title.add(temp.getString("name"));
            address.add(temp.getString("address"));
            phone_number.add(temp.getString("phone"));
            url.add(temp.getString("url"));
            img.add(temp.getString("logo"));
            bus_id.add(temp.getInt("id"));
            currencies.put(bus_id.get(i),new ArrayList<Currency>());
        }

        listView.setAdapter(adapter);
        adapter.notifyDataSetChanged();


        for (int id:bus_id){

            String url="https://webdev.cse.buffalo.edu/rewards/rewards/redeem/?business="+id+"&customer="+LoginActivity.user_id;

            CurrAPI currAPI=new CurrAPI();
            currAPI.execute(new String[]{url});


        }
    }


    class MyAdapter extends ArrayAdapter<String>{

        Context context;
        ArrayList<String> r_title;
        ArrayList<String> r_address;
        ArrayList<String> r_phone_number;
        ArrayList<String> r_url;
        ArrayList<String> r_img;
        HashMap<Integer,ArrayList<Currency>> r_currencies;


        MyAdapter(Context c, ArrayList<String> title, ArrayList<String> addy, ArrayList<String>  phone, ArrayList<String> url, ArrayList<String> img,HashMap<Integer,ArrayList<Currency>> currencies){
            super(c,R.layout.current_business,title);
            this.context=c;
            r_title=title;
            r_address=addy;
            r_phone_number=phone;
            r_url=url;
            r_img=img;
            r_currencies=currencies;

        }

        @NonNull
        @Override
        public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {

            LayoutInflater layoutInflater= (LayoutInflater) getActivity().getApplicationContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);

            View row=layoutInflater.inflate(R.layout.current_business,parent,false);
            ImageView imageView= row.findViewById(R.id.logo);

            String temp_img=r_img.get(position);

            Picasso.get().load(temp_img).into(imageView);

            ListView listView=(ListView) row.findViewById(R.id.list_rp);

            final String name=r_title.get(position);

            final int bus_id_cur=bus_id.get(position);

            final ArrayList<Currency> cur=r_currencies.get(bus_id_cur);

            ArrayList<String> currency_strings=new ArrayList<>();

            for(Currency c:cur){
                currency_strings.add(c.toString());
            }

            final int parent_pos=position;

            ((TextView) row.findViewById(R.id.name)).setText(r_title.get(position));

            ArrayAdapter<String> adapter = new ArrayAdapter<String> (getContext(), android.R.layout.simple_list_item_1, currency_strings);

            listView.setClickable(false);
            listView.setEnabled(false);
            listView.setFocusable(false);

            listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {

                    Intent i=new Intent(getActivity(), ExpandBusiness.class);

                    i.putExtra("business_name",name);
                    i.putExtra("bus_id",bus_id.get(parent_pos));
                    i.putExtra("addy",r_address.get(parent_pos));
                    i.putExtra("phone",r_phone_number.get(parent_pos));
                    i.putExtra("link",r_url.get(parent_pos));
                    i.putExtra("logo",r_img.get(parent_pos));

                    i.putExtra("currency_id",cur.get(position).id);
                    i.putExtra("currency_val",cur.get(position).val);
                    i.putExtra("currency_rewards",cur.get(position).rewards);
                    i.putExtra("currency_name",cur.get(position).name);

                    i.putExtra("list",cur.toString());

                    i.putExtra("currency_string",currency_data.get(bus_id_cur));

                    startActivity(i);

                }
            });

            listView.setAdapter(adapter);

            return row;
        }
    }



    @Override
    public void onResume(){
        super.onResume();
        Log.d("home-frag","On resume worked");

        title.clear();address.clear();address.clear();phone_number.clear();url.clear();img.clear();bus_id.clear();currencies.clear();

        API api=new API();
        api.execute(new String[]{
                "https://webdev.cse.buffalo.edu/rewards/users/"+LoginActivity.user_id+"/"
        });


        try {

        } catch (Exception e) {
            e.printStackTrace();
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
                return "API failed";
            }

            if(!response.isSuccessful()){

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

            Log.d("Home Frag ",result);

            if(result.equals("API failed")){
                return;
            }

            try {
                setup(result);
            } catch (Exception e) {
                e.printStackTrace();
            }

            return;

        }
    }

    private class CurrAPI extends AsyncTask<String, Void, String> {
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

            if(!response.isSuccessful()){

                Log.e("Currency API Failed",response.toString());

                try{
                    Log.e("Error Currency API",response.body().string());
                    return response.body().string();
                }
                catch (Exception k){
                }
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

            Log.d("Home Frag ",result);

            if(result.equals("API failed")){
                return;
            }

            try {
                setCurrencies(result);
            } catch (Exception e) {
                e.printStackTrace();
                return;
            }
            return;

        }
    }

    public void setCurrencies(String s) throws Exception{

        JSONArray jso;

        try{
            jso = new JSONArray(s);
        }
        catch(Exception k){
            return;
        }


        for(int i=0;i<jso.length();i++){
            JSONObject cur=jso.getJSONObject(i);

            int points_total=cur.getInt("accumulated");
            JSONObject curObj=cur.getJSONObject("currency");

            int bus_id_cur=curObj.getInt("business");

            currency_data.put(bus_id_cur,s);

            Currency temp=new Currency(points_total,curObj.getString("plural_label"),curObj.getInt("id"),cur.getJSONArray("rewards").toString());
            currencies.get((bus_id_cur)).add(temp);
        }



        adapter.notifyDataSetChanged();


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
package com.example.ubloyal2;

import android.app.AlertDialog;
import android.content.Context;
import android.content.res.ColorStateList;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import android.app.Fragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;


/**
 * A simple {@link Fragment} subclass.
 * Activities that contain this fragment must implement the
 * {@link CurrencyFragment.OnFragmentInteractionListener} interface
 * to handle interaction events.
 * Use the {@link CurrencyFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class CurrencyFragment extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters

    ListView listView;
    Button his_but;

    View deleteDialogView;
    AlertDialog deleteDialog;

   ArrayList<String> history_data=new ArrayList<>();
   String business_name;

    ArrayList<String> reward_titles=new ArrayList<>();
    ArrayList<Integer> reward_value=new ArrayList<>();
    ArrayList<String> reward_logos=new ArrayList<>();

   Currency currencyObj;

    private OnFragmentInteractionListener mListener;

    public CurrencyFragment() {
        // Required empty public constructor
    }

    // TODO: Rename and change types and number of parameters
    public static CurrencyFragment newInstance(String param1, String param2) {
        CurrencyFragment fragment = new CurrencyFragment();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {

//           currencyObj args.putInt("currency_id",obj.id);
//            args.putString("rewards",obj.rewards);
//            args.putInt("value",obj.val);
//            args.putString("name",obj.name);


            String name=getArguments().getString("name");
            String rewards=getArguments().getString("rewards");
            int valueee=getArguments().getInt("value",-1);
            int id=getArguments().getInt("currency_id",-1);

            business_name=getArguments().getString("business_name");
            currencyObj=new Currency(valueee,name,id,rewards);

        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View root= inflater.inflate(R.layout.fragment_currency, container, false);

        listView=root.findViewById(R.id.rewards_list);
        his_but=root.findViewById(R.id.history);

        his_but.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                LayoutInflater factory = LayoutInflater.from(v.getContext());
                deleteDialogView = factory.inflate(R.layout.new_dialog, null);

                deleteDialog = new AlertDialog.Builder(v.getContext()).create();
                deleteDialog.setView(deleteDialogView);

                deleteDialogView.findViewById(R.id.button2).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        //your business logic
                        deleteDialog.dismiss();
                    }
                });

                ListView his_list = (ListView) deleteDialogView.findViewById(R.id.his);

                ArrayAdapter<String> his_adp = new ArrayAdapter<String>(
                        v.getContext(),
                        android.R.layout.simple_list_item_1
                        , history_data
                );

                ((TextView) deleteDialogView.findViewById(R.id.camp_name)).setText("Balance: "+currencyObj.val+ " "+currencyObj.name);
                ((TextView) deleteDialogView.findViewById(R.id.buss_name)).setText(business_name);

                his_list.setAdapter(his_adp);
                deleteDialog.show();

            }
        });

        try {
            parseRewards(currencyObj.rewards);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        String url="https://webdev.cse.buffalo.edu/rewards/rewards/history/?customer="+LoginActivity.user_id+"&currency="+currencyObj.id;


        MyAdapter adp=new MyAdapter(getActivity(),reward_titles,reward_value,reward_logos);
        listView.setAdapter(adp);

        API api=new API();
        api.execute(new String[]{url});

        return root;
    }

    // TODO: Rename method, update argument and hook method into UI event
    public void onButtonPressed(Uri uri) {
        if (mListener != null) {
            mListener.onFragmentInteraction(uri);
        }
    }

//    @Override
//    public void onAttach(Context context) {
//        super.onAttach(context);
//        if (context instanceof OnFragmentInteractionListener) {
//            mListener = (OnFragmentInteractionListener) context;
//        } else {
//            throw new RuntimeException(context.toString()
//                    + " must implement OnFragmentInteractionListener");
//        }
//    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }

    /**
     * This interface must be implemented by activities that contain this
     * fragment to allow an interaction in this fragment to be communicated
     * to the activity and potentially other fragments contained in that
     * activity.
     * <p>
     * See the Android Training lesson <a href=
     * "http://developer.android.com/training/basics/fragments/communicating.html"
     * >Communicating with Other Fragments</a> for more information.
     */
    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name
        void onFragmentInteraction(Uri uri);
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
                setup(result);
            } catch (Exception e) {
                e.printStackTrace();
            }
            return;

        }
    }

    private void setup(String s) throws JSONException{

//        "[\n" +
//                "    {\n" +
//                "        \"created_at\": \"2019-11-14T07:45:43Z\",\n" +
//                "        \"reward\": \"free drink\",\n" +
//                "        \"value\": -20\n" +
//                "    },"

        JSONArray jr=new JSONArray(s);

        for(int i=0;i<jr.length();i++){
            JSONObject cur=jr.getJSONObject(i);
            String created=cur.getString("created_at");
            String reward="";
            String exp="";
            int val_t=0;

            try{
                reward=cur.getString("reward");
            }
            catch (Exception e){
                exp=cur.getString("expires_at");
            }

            val_t=cur.getInt("value");

            String full="";

            if(reward.isEmpty()){

                full = "Date: "+created+"\n"+
                        "Expiry Date: "+exp+"\n"+
                        val_t+" "+currencyObj.name;

            }
            else{

                full = "Date: "+created+"\n"+
                        "Reward Redeemed: "+reward+"\n"+
                        val_t+" "+currencyObj.name;
            }

            history_data.add(full);

        }

        history_data.size();

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

    class MyAdapter extends ArrayAdapter<String> {

        Context context;
        ArrayList<String> reward_titles;
        ArrayList<Integer> reward_value;
        ArrayList<String> reward_logos;

        MyAdapter(Context c, ArrayList<String> title, ArrayList<Integer> values,ArrayList<String> images) {
            super(c, R.layout.progress, title);
            this.context = c;
            reward_titles=title;
            reward_value=values;
            reward_logos=images;

        }

        @NonNull
        @Override
        public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {

            LayoutInflater layoutInflater = (LayoutInflater) getContext().getApplicationContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);

            View row = layoutInflater.inflate(R.layout.progress, parent, false);

            ProgressBar text = row.findViewById(R.id.progressBar);


            Double reward_val=new Double(reward_value.get(position));
            Double total_points=new Double(currencyObj.val);

            int num= (int) Math.round((total_points/reward_val)*100);

            text.setProgress(num);

            if(num>=100){
                text.setProgressTintList(ColorStateList.valueOf(0xFF4CAF50));
            }
            else{
                //text.setProgressBackgroundTintList(ColorStateList.valueOf(R.color.colorPrimary));
                //text.setProgressBackgroundTintList(getResources().getColorStateList(R.color.colorPrimary));
                text.setProgressTintList(ColorStateList.valueOf(0xFF1281D5));
            }

            ((TextView) row.findViewById(R.id.reward_name)).setText(reward_titles.get(position)+": "+reward_value.get(position)+ " "+currencyObj.name);

            ImageView imageView= row.findViewById(R.id.logo);

            String img_url="https://webdev.cse.buffalo.edu"+reward_logos.get(position);

            Picasso.get().load(img_url).into(imageView);

            return row;
        }


    }

    public void parseRewards(String s) throws JSONException {

        JSONArray arry=new JSONArray(s);

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

}

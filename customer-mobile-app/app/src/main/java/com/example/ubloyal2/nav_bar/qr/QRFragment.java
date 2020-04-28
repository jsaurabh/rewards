package com.example.ubloyal2.nav_bar.qr;

import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProviders;

import com.example.ubloyal2.LoginActivity;
import com.example.ubloyal2.MainActivity;
import com.example.ubloyal2.R;
import com.google.zxing.BarcodeFormat;
import com.google.zxing.MultiFormatWriter;
import com.google.zxing.WriterException;
import com.google.zxing.common.BitMatrix;
import com.journeyapps.barcodescanner.BarcodeEncoder;

import org.json.JSONException;
import org.json.JSONObject;

public class QRFragment extends Fragment {

    private QRViewModel QRViewModel;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        QRViewModel =
                ViewModelProviders.of(this).get(QRViewModel.class);
        View root = inflater.inflate(R.layout.fragment_qr, container, false);

        //TextView userId=root.findViewById(R.id.account_id);

        ImageView img=root.findViewById(R.id.qr_code);


        MainActivity activity = (MainActivity) getActivity();
        String myDataFromActivity = LoginActivity.login_resposne;
        Log.d("login ",myDataFromActivity);
        JSONObject jsonObject = new JSONObject();

        try {
            jsonObject= new JSONObject(myDataFromActivity);
        } catch (JSONException e) {
            e.printStackTrace();
        }


        try {
            String email_set= jsonObject.getJSONObject("user").getString("id");
            //userId.setText("Account # "+email_set);
            MultiFormatWriter multiFormatWriter = new MultiFormatWriter();

                try {

                    BitMatrix bitMatrix= multiFormatWriter.encode(email_set,BarcodeFormat.QR_CODE,500,500);

                    BarcodeEncoder barcodeEncoder=new BarcodeEncoder();

                    Bitmap bm = barcodeEncoder.createBitmap(bitMatrix);

                    if(bm != null) {
                        img.setImageBitmap(bm);
                    }
                } catch (WriterException e){
                    Log.e("QR","QR Failed to gen");

                }

        } catch (JSONException e) {
            e.printStackTrace();
        }


        return root;
    }
}
package com.example.ubloyal2;

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatDialogFragment;

public class RewardsDialog extends Dialog {

//    @NonNull
//    @Override
//    public Dialog onCreateDialog(@Nullable Bundle savedInstanceState) {
//        AlertDialog.Builder builder=new AlertDialog.Builder(getActivity());
//
//        LayoutInflater inflater=getActivity().getLayoutInflater();
//        View view=inflater.inflate(R.layout.dialog_des,null);
//
//        if(view.getParent()!=null){
//            ((ViewGroup)view.getParent()).removeView(view);
//        }
//
//        builder.setView(view)
//                .setTitle("Rewards Status")
//                .setMessage("reward.name")
//                .setPositiveButton(android.R.string.ok, null)
//                .show();
//
//
//        return builder.create();
//
//    }

    public RewardsDialog(@NonNull Context context) {
        super(context);
    }
}

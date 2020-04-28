package com.example.ubloyal2.nav_bar.rewards;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class RewardsViewModel extends ViewModel {

    private MutableLiveData<String> mText;

    public RewardsViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("Rewards Programs");
    }

    public LiveData<String> getText() {
        return mText;
    }
}
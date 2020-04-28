import 'dart:convert';

import 'package:digital_rewards/data/CurrencyDataModel.dart';
import 'package:digital_rewards/data/RewardsDataModel.dart';

/*GET Request -
*  {
*     "currency": {
*                   "id": 2,
*                   "singular_label": "Star",
*                   "plural_label": "Stars",
*                   "business": 1
*                },
*     "accumulated": 530,
*     "rewards": [
*           {
*               "id": 1,
*               "reward": "Free coffee",
*               "image": "/media/rewards/starbucks-coffee.jpg",
*               "value": 5,
*               "campaign": 2
*           }
*       ]
*  },
*/
class CustomerRewardsDataModel {
  //JSON Response
  final CurrencyDataModel currencyDataModel;
  final int accumulatedRewards;
  final List<RewardsDataModel> rewardsDataModel;

  int currentRewards;
  bool rewardsRedeemable;

  CustomerRewardsDataModel(
      {this.currencyDataModel,
      this.rewardsDataModel,
      this.accumulatedRewards,
      this.currentRewards,
      this.rewardsRedeemable});

  //JSON Response
  factory CustomerRewardsDataModel.fromJson(Map<String, dynamic> jsonData) {
    var filterRewards = [];
    bool redeemableStatus = false;
    var rewardsList = jsonData['rewards'] as List;
    List<RewardsDataModel> rewardsDataModelList =
        rewardsList.map((i) => RewardsDataModel.fromJson(i)).toList();

    rewardsDataModelList.forEach((rewards) {
      if (jsonData['accumulated'] < rewards.rewardValue) {
        filterRewards.add(rewards);
      }else
        redeemableStatus = true;
    });

    rewardsDataModelList
        .removeWhere((rewards) => filterRewards.contains(rewards));


    return CustomerRewardsDataModel(
      currencyDataModel: CurrencyDataModel.fromJson(jsonData['currency']),
      accumulatedRewards: jsonData['accumulated'],
      currentRewards: jsonData['accumulated'],
      rewardsDataModel: rewardsDataModelList,
      rewardsRedeemable: redeemableStatus
    );
  }
}

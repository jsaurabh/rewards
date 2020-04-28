import 'package:digital_rewards/data/CustomerRewardsDataModel.dart';

/*GET Request: /rewards/rewards/redeem/?business={businessId}&customer={customerId}
*curl -H "Authorization: Token f432ebdbcfa936048d1d6b80002f42eeb07f669e" -H "Content-Type: application/json" https://webdev.cse.buffalo.edu/rewards/rewards/redeem/?business=4&customer=4
*Response:
* [
*    {
*        "currency": {
*            "id": 2,
*            "label": "Stars",
*            "business": 1
*        },
*        "accumulated": 530,
*        "rewards": [
*            {
*                "id": 1,
*                "reward": "Free coffee",
*                "image": "/media/rewards/starbucks-coffee.jpg",
*                "value": 5,
*                "campaign": 2
*            }
*        ]
*    },
*    {
*        "currency": {
*            "id": 3,
*            "label" : "Bucks",
*            "business": 1
*        },
*        "accumulated": 374,
*        "rewards": []
*    }
* ]
*/
class RewardsProgramDataModel {
  //JSON Response
  final List<CustomerRewardsDataModel> redemptionDataModel;

  bool rewardsRedeemable;

  RewardsProgramDataModel({this.redemptionDataModel, this.rewardsRedeemable});

  factory RewardsProgramDataModel.fromJson(List<dynamic> jsonData) {
    bool redeemableStatus = false;
    var filterRewards = [];
    List<CustomerRewardsDataModel> redemptionDataModelList =
        new List<CustomerRewardsDataModel>();
    redemptionDataModelList =
        jsonData.map((i) => CustomerRewardsDataModel.fromJson(i)).toList();

    redemptionDataModelList.forEach((rewardsDataModel) {
      if (rewardsDataModel.rewardsRedeemable) {
        redeemableStatus = true;
      }else
        filterRewards.add(rewardsDataModel);
    });

    redemptionDataModelList
        .removeWhere((rewards) => filterRewards.contains(rewards));

    return new RewardsProgramDataModel(
      redemptionDataModel: redemptionDataModelList,
      rewardsRedeemable: redeemableStatus,
    );
  }
}

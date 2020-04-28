/*Rewards Redemption POST Sample Curl Command
* curl -H "Authorization: Token f432ebdbcfa936048d1d6b80002f42eeb07f669e" -H "Content-Type: application/json" -d '{"business": 4, "customer": 4, "redemption_rules": [{"menu_item": 6, "quantity": 2}, {"menu_item": 7, "quantity": 2}]}' https://webdev.cse.buffalo.edu/rewards/rewards/redeem/
* For 400 Error -
* {
*    "actual": {
*        "2": 9,
*        "3": 369
*    },
*    "expected": {
*        "2": 25
*    }
* }
*/
class RedemptionDataModel {
  //JSON Request
  final int businessID;
  final int customerID;

  RedemptionDataModel({this.customerID, this.businessID});

  Map mapRequestBody(List rewardItemsList) {
    var map = new Map<String, dynamic>();
    var rewardsRedemptionList = [];

    if (rewardItemsList.isNotEmpty) {
      rewardItemsList.forEach((item) {
        var rewardsMap = {
          'rule': item.redemptionRuleID,
          'quantity': item.itemQuantity,
        };
        rewardsRedemptionList.add(rewardsMap);
      });
    }
    map['business'] = businessID;
    map['customer'] = customerID;
    map['rewards'] = rewardsRedemptionList;

    print("Rewards Redemption RequestBody: "+ map.toString());

    return map;
  }
}

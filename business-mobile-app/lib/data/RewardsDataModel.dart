/*GET Request -
* "rewards": [
*            {
*               "id": 1,
*               "reward": "Free coffee",
*               "image": "/media/rewards/starbucks-coffee.jpg",
*               "value": 5,
*               "campaign": 2
*            }
*        ]
*/

class RewardsDataModel {
  //JSON Response
  final int redemptionRuleID;
  final String rewardsName;
  final String rewardsImage;
  final int rewardValue;
  final int campaignID;

  int itemQuantity;
  bool buttonDisable;

  RewardsDataModel(
      {this.redemptionRuleID,
      this.rewardsName,
      this.rewardsImage,
      this.rewardValue,
      this.campaignID,
      this.itemQuantity = 0,
      this.buttonDisable = false});

  //Mapping JSON Response
  factory RewardsDataModel.fromJson(Map<String, dynamic> jsonData) {
    return RewardsDataModel(
        redemptionRuleID: jsonData['id'],
        rewardsName: jsonData['reward'],
        rewardsImage: jsonData['image'],
        rewardValue: jsonData['value'],
        campaignID: jsonData['campaign']);
  }
}

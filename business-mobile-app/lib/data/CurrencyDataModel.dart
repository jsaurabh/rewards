/* GET Request -
* "currency": {
*             "id": 2,
*             "label": "Stars",
*             "business": 1
*          },
*/
class CurrencyDataModel {
  //JSON Response
  final int currencyID;
  final String label;
  final int businessID;

  CurrencyDataModel({this.currencyID, this.label, this.businessID});

  //Mapping JSON Response
  factory CurrencyDataModel.fromJson(Map<String, dynamic> jsonData) {
    return CurrencyDataModel(
        currencyID: jsonData['id'],
        label: jsonData['label'],
        businessID: jsonData['business']);
  }
}

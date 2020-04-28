
/*
* GET Request
* {
*   "id": 1,
*   "name": "Drip coffee",
*   "description" : "This is Drip Coffee",
*   "category" : 1,
* }
*
*/

class ItemDataModel {

  //JSON Response
  final int itemID;
  final String itemName;
  final String itemImagePath;

  //Track Item Quantity
  int itemQuantity;

  ItemDataModel({this.itemID, this.itemName, this.itemImagePath, this.itemQuantity = 0});

  //Mapping JSON Response
  factory ItemDataModel.fromJson(Map<String, dynamic> jsonData){
    return ItemDataModel(
      itemID: jsonData['id'],
      itemName: jsonData['name'],
      itemImagePath: jsonData['image'],
    );
  }
}

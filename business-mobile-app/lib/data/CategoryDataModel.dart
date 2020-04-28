import 'package:digital_rewards/data/ItemDataModel.dart';

/*
* GET Request:
* "items": [
*     {
*       "id": 1,
*       "name": "Drip Coffee",
*       "description": "This is Drip Coffee",
*       "category": 1
*     },
*     {
*       "id": 2,
*       "name": "Espresso",
*       "description": "This is Espresso",
*       "category": 1
*     },
*     {
*       "id": 3,
*       "name": "Americano",
*       "description": "This is Americano",
*       "category": 1
*     },
*  ]
* */
class CategoryDataModel{

  //JSON Response
  final int categoryID;
  final String categoryName;
  final List<ItemDataModel> itemDataModel;

  CategoryDataModel({this.categoryID, this.categoryName, this.itemDataModel});

  //Mapping JSON Response
  factory CategoryDataModel.fromJson(Map<String, dynamic> jsonData){
    var itemsList = jsonData['items'] as List;
    List<ItemDataModel> itemDataModelList = itemsList.map((i) => ItemDataModel.fromJson(i)).toList();

    return CategoryDataModel(
      categoryID: jsonData['id'],
      categoryName: jsonData['name'],
      itemDataModel: itemDataModelList,
    );
  }

}
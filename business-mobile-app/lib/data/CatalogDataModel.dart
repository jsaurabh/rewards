import 'package:digital_rewards/data/CategoryDataModel.dart';

/* GET Request: /rewards/catalog/business/'${businessId}'
 * curl -H "Authorization: Token f432ebdbcfa936048d1d6b80002f42eeb07f669e" -H "Content-Type: application/json" https://webdev.cse.buffalo.edu/rewar
ds/catalog/business/4
 * Response:
 * [
 *    {
 *    "id": 1
 *    "items": [
 *      {
 *        "id": 1,
 *        "name": "Drip Coffee",
 *        "description": "This is Drip Coffee",
 *        "category": 1
 *      },
 *      {
 *        "id": 2,
 *        "name": "Espresso",
 *        "description": "This is Espresso",
 *        "category": 1
 *      },
 *    ]
 *    "name": "Coffee",
 *    business": 1
 *    }
 *    {
 *    "id": 2,
 *    "items": [
 *      {
 *        "id": 3,
 *        "name": "Veggie Delight",
 *        "description": "This is Veggie Delight",
 *        "category": 2
 *      }
 *    ],
 *    "name": "Sandwich",
 *    "business": 1
 *    }
 *  ]
 */

class CatalogDataModel {
  //JSON Request
  final String token;
  final int businessID;
  //final String businessName;

  //JSON Response
  final List<CategoryDataModel> categoryDataModel;

  CatalogDataModel({this.token, this.businessID, this.categoryDataModel});

  //JSON Request
  List mapRequestBody() {
    var orderItemList = [];

    categoryDataModel.forEach((category) {
      category.itemDataModel.forEach((items) {
        if (items.itemQuantity > 0) {
          var itemsMap = {
            'menu_item': items.itemID,
            'quantity': items.itemQuantity,
          };
          orderItemList.add(itemsMap);
        }
      });
    });

    print(orderItemList);
    return orderItemList;
  }

  //JSON Response
  factory CatalogDataModel.fromJson(List<dynamic> jsonData) {
    List<CategoryDataModel> categoryDataModel =
        jsonData.map((i) => CategoryDataModel.fromJson(i)).toList();

    return CatalogDataModel(
      categoryDataModel: categoryDataModel,
    );
  }
}

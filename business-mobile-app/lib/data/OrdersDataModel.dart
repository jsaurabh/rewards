/*Orders POST Curl Sample Command
* curl -H "Authorization: Token f432ebdbcfa936048d1d6b80002f42eeb07f669e" -H "Content-Type: application/json" -d '{"business": 4, "customer": 4, "line_items": [{"menu_item": 6, "quantity": 2}, {"menu_item": 7, "quantity": 2}]}' https://webdev.cse.buffalo.edu/rewards/orders/
*/
class OrdersDataModel {
  //JSON Request
  final int businessID;
  final int customerID;

  OrdersDataModel({this.businessID, this.customerID});

  //JSON Request
  Map mapRequestBody(List itemList) {
    var map = new Map<String, dynamic>();
    var orderItemList = [];

    if (itemList.isNotEmpty) {
      itemList.forEach((item) {
        var itemsMap = new Map<String, int>();
        itemsMap['menu_item'] = item.itemID;
        itemsMap['quantity'] = item.itemQuantity;
        orderItemList.add(itemsMap);
      });

      map['business'] = businessID;
      map['customer'] = customerID;
      map['line_items'] = orderItemList;

      print(map);
    }
    return map;
  }
}

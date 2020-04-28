import 'package:digital_rewards/data/CatalogDataModel.dart';
import 'package:digital_rewards/data/EmployeeDataModel.dart';
import 'package:digital_rewards/data/OrdersDataModel.dart';
import 'package:digital_rewards/data/RedemptionDataModel.dart';
import 'package:digital_rewards/data/RewardsProgramDataModel.dart';
import 'package:digital_rewards/utils/Helper.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:digital_rewards/utils/Const.dart';
import 'package:digital_rewards/web/CustomerCheckInPage.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:convert';
import 'dart:io';

class CartCheckOutPage extends StatefulWidget {
  final String title;
  final String token;
  final int customerID;
  final int rewardsStatus;
  final RewardsProgramDataModel rewardsData;
  final CatalogDataModel businessCatalog;
  final EmployeeDataModel employeeProfile;

  CartCheckOutPage(
      {Key key,
      @required this.title,
      @required this.customerID,
      @required this.rewardsStatus,
      this.rewardsData,
      @required this.businessCatalog,
      @required this.employeeProfile,
      @required this.token})
      : super(key: key);

  @override
  _CartCheckOutPageState createState() => new _CartCheckOutPageState();
}

class _CartCheckOutPageState extends State<CartCheckOutPage> {
  final GlobalKey<ScaffoldState> _scaffoldKey = new GlobalKey<ScaffoldState>();
  List ordersItemList = [];
  List rewardItemsList = [];
  bool redemptionStatus = false;
  bool orderStatus = false;
  bool rewardsAvailable = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBar(
        title: Text('${Const.title_checkout}',
            style: TextStyle(color: Colors.white)),
        backgroundColor: Colors.blueAccent,
      ),
      body: Material(
        child: Container(
          child: Padding(
            padding: const EdgeInsets.all(25.0),
            child: renderCartUI(context),
          ),
        ),
      ),
    );
  }

  Widget renderCartUI(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: <Widget>[
          Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              Text(
                Const.label_order_details,
                style: TextStyle(fontSize: 30.0, fontWeight: FontWeight.bold),
              ),
              SizedBox(
                height: 8.0,
              ),
            ],
          ),
          displayCart(context),
          SizedBox(
            height: 10.0,
          ),
          RaisedButton(
            padding: EdgeInsets.all(12.0),
            shape: StadiumBorder(),
            child: Text(
              "${Const.button_submit_order}",
              style: TextStyle(color: Colors.white, fontSize: 20.0),
            ),
            color: Colors.blueAccent,
            onPressed: () async {
              OrdersDataModel ordersDataModel = new OrdersDataModel(
                  businessID: widget.employeeProfile.business[0].businessID,
                  customerID: widget.customerID);

              String orders = await createOrdersPostRequest(
                  Const.API_HOST, Const.API_ORDERS_PATH,
                  requestBody: ordersDataModel.mapRequestBody(ordersItemList));

              if (widget.rewardsStatus == 200 && rewardsAvailable) {
                RedemptionDataModel redemptionDataModel =
                    new RedemptionDataModel(
                        businessID:
                            widget.employeeProfile.business[0].businessID,
                        customerID: widget.customerID);

                String redemptionStatus = await createRewardsPostRequest(
                    Const.API_HOST, Const.API_REWARDS_REDEEM_PATH,
                    requestBody:
                        redemptionDataModel.mapRequestBody(rewardItemsList));
              }

              if (orderStatus || redemptionStatus) {
                Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (BuildContext context) => CustomerCheckInPage(
                          title: widget.title,
                          token: widget.token,
                          employeeProfile: widget.employeeProfile),
                    ));

                if (orderStatus && redemptionStatus)
                  Helper.showInTransactionAlert(Const.success_order_rewards,
                      Icons.check_box, Colors.green, context);
                else if (!orderStatus && redemptionStatus)
                  Helper.showInTransactionAlert(Const.success_rewards,
                      Icons.check_box, Colors.green, context);
                else
                  Helper.showInTransactionAlert(Const.success_order,
                      Icons.check_box, Colors.green, context);
              } else {
                if (rewardItemsList.isEmpty && ordersItemList.isEmpty)
                  Helper.showInTransactionAlert(Const.error_cart_empty,
                      Icons.remove_shopping_cart, Colors.red[400], context);
                else
                  Helper.showInTransactionAlert(Const.error_order, Icons.cancel,
                      Colors.red[400], context);
              }
            },
          ),
        ],
      ),
    );
  }

  Widget displayCart(BuildContext context) {
    List<Widget> list = new List<Widget>();

    list.add(Padding(
        padding: EdgeInsets.all(10.0),
        child: Text(
          '\t\t' +
              'Qty' +
              "\t\t\t" +
              'Item Name' +
              '\n-----------------------------',
          style: TextStyle(fontSize: 20.0, fontWeight: FontWeight.bold),
          textAlign: TextAlign.justify,
        )));

    widget.businessCatalog.categoryDataModel.forEach((category) {
      category.itemDataModel.forEach((item) {
        if (item.itemQuantity > 0) {
          ordersItemList.add(item);
          list.add(Padding(
              padding: EdgeInsets.all(10.0),
              child: Text(
                '\t\t' +
                    item.itemQuantity.toString() +
                    "\t\t\t" +
                    item.itemName,
                style: TextStyle(fontSize: 20.0),
                textAlign: TextAlign.justify,
              )));
        }
      });
    });

    if (widget.rewardsStatus == 200) {
      widget.rewardsData.redemptionDataModel.forEach((rewards) {
        rewards.rewardsDataModel.forEach((item) {
          if (item.itemQuantity > 0) {
            rewardItemsList.add(item);
            list.add(Padding(
                padding: EdgeInsets.all(10.0),
                child: Text(
                  '(-) ${item.itemQuantity.toString()}' +
                      "\t\t\t" +
                      item.rewardsName.toString(),
                  style: TextStyle(fontSize: 20.0),
                  textAlign: TextAlign.justify,
                )));
            rewardsAvailable = true;
          }
        });
      });
    }
    return new Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10.0),
      ),
      elevation: 8.0,
      margin: EdgeInsets.all(5.0),
      semanticContainer: true,
      child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch, children: list),
    );
  }

  /*Submit Order API GET Request
    * Populate all the rewards that the customer is eligible for
    */
  Future<String> createOrdersPostRequest(String host, String path,
      {Map requestBody}) {
    var url = Uri.https(host, path);

    //print("Orders API URL: " + url.toString());

    return http
        .post(url,
            headers: {
              HttpHeaders.authorizationHeader: 'Token ${widget.token}',
              HttpHeaders.contentTypeHeader: 'application/json',
            },
            body: json.encode(requestBody))
        .then((http.Response response) {
      final int statusCode = response.statusCode;

      /*print("Orders API Status: " +
          statusCode.toString() +
          " Response: " +
          '${response.body}');*/

      if (statusCode == 200) {
        orderStatus = true;
        return statusCode.toString();
      } else if (statusCode == 400) {
        return "";
      } else
        throw new Exception('Error while fetching data');
    });
  }
  /*Redeem Rewards API POST Request-
  * Redeeming rewards that users have selected to redeeem in the current transaction
  */
  Future<String> createRewardsPostRequest(String host, String path,
      {Map requestBody}) {
    var url = Uri.https(host, path);

    //print("Rewards Redemption API URL: " + url.toString());

    return http
        .post(url,
            headers: {
              HttpHeaders.authorizationHeader: 'Token ${widget.token}',
              HttpHeaders.contentTypeHeader: 'application/json',
            },
            body: json.encode(requestBody))
        .then((http.Response response) {
      final int statusCode = response.statusCode;

      /*print("Rewards Redemption API Status: " +
          statusCode.toString() +
          " Response: " +
          '${response.body}');*/

      if (statusCode == 204) {
        redemptionStatus = true;
        return statusCode.toString();
      } else
        throw new Exception('Error while fetching data');
    });
  }
}

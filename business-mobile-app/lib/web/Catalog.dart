import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:digital_rewards/data/EmployeeDataModel.dart';
import 'package:digital_rewards/data/RewardsProgramDataModel.dart';
import 'package:digital_rewards/utils/Helper.dart';
import 'package:digital_rewards/web/RewardsPage.dart';

import 'package:http/http.dart' as http;
import 'package:digital_rewards/data/CatalogDataModel.dart';
import 'package:digital_rewards/web/CartCheckOutPage.dart';
import 'package:flutter/material.dart';
import 'package:flushbar/flushbar.dart';
import 'package:digital_rewards/web/BusinessProfilePage.dart';
import 'package:digital_rewards/utils/Const.dart';

class Catalog extends StatefulWidget {
  final String title;
  final String token;
  final EmployeeDataModel employeeProfile;
  final CatalogDataModel businessCatalog;
  final String customerID;

  Catalog(
      {Key key,
      this.token,
      @required this.title,
      @required this.employeeProfile,
      @required this.businessCatalog,
      @required this.customerID})
      : super(key: key);

  @override
  _CatalogState createState() => new _CatalogState();
}

class _CatalogState extends State<Catalog> with SingleTickerProviderStateMixin {
  int rewardsStatus = 0;
  bool rewardsRedeemable = false;
  Flushbar flushBar;
  TabController _tabController;
  RewardsProgramDataModel rewards;
  
  //Increment item Qty
  void _addProduct(int categoryIndex, int itemIndex) {
    setState(() => widget.businessCatalog.categoryDataModel[categoryIndex]
        .itemDataModel[itemIndex].itemQuantity++);
  }
  
  //Decrement item Qty
  void _removeProduct(int categoryIndex, int itemIndex) {
    setState(() {
      if (widget.businessCatalog.categoryDataModel[categoryIndex]
              .itemDataModel[itemIndex].itemQuantity !=
          0)
        widget.businessCatalog.categoryDataModel[categoryIndex]
            .itemDataModel[itemIndex].itemQuantity--;
    });
  }

  @override
  void initState() {
    super.initState();
    _tabController = TabController(
        length: widget.businessCatalog.categoryDataModel.length, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    final Orientation orientation = MediaQuery.of(context).orientation;
    List<Color> _color = [Colors.orange[600],Colors.orange[200], Colors.grey[400]];

    return Scaffold(
      //key: _scaffoldKey,
      appBar: AppBar(
        title: Text(widget.title),
        bottom: TabBar(
          isScrollable: true,
          indicatorColor: Colors.white,
          indicatorSize: TabBarIndicatorSize.label,
          tabs: List<Widget>.generate(
              widget.businessCatalog.categoryDataModel.length, (int index) {
            return new Tab(
              text:
                  widget.businessCatalog.categoryDataModel[index].categoryName,
            );
          }),
          controller: _tabController,
        ),
      ),
      body: TabBarView(
        children: List<Widget>.generate(
            widget.businessCatalog.categoryDataModel.length, (int index) {
          return _populateItemGridView(orientation, index);
        }),
        controller: _tabController,
      ),
      floatingActionButton: (Container(
        alignment: Alignment.bottomRight,
        height: 150,
        width: 150,
        child: Column(children: <Widget>[
          FloatingActionButton(
            heroTag: null,
            child: Icon(
              Icons.card_giftcard,
              size: 30,
            ),
            backgroundColor: rewardsStatus != 200 ? _color[0] : rewardsRedeemable ? _color[1] : _color[2],
            onPressed: () async {
              if (rewardsStatus != 200) {
                rewards = await createGETRewardsRedeem(
                    Const.API_HOST, Const.API_REWARDS_REDEEM_PATH);
              }

              if (rewards != null && rewards.rewardsRedeemable) {

                setState(() {
                  rewardsRedeemable = true;
                });

                Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (BuildContext context) =>
                            RewardsPage(rewardsData: rewards)));
              }else{
                Helper.showInFlushBar(Const.info_rewards_redeemable, context);
              }
            },
            hoverElevation: 70.0,
          ),
          SizedBox(
            height: 20.0,
          ),
          FloatingActionButton(
            heroTag: null,
            child: Icon(
              Icons.shopping_cart,
              size: 30,
            ),
            backgroundColor: Colors.blue,
            onPressed: () {
              //Conditional Route Navigation
              if(rewardsStatus == 200)
                Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (BuildContext context) => CartCheckOutPage(
                          title: widget.title,
                          token: widget.token,
                          rewardsData: rewards,
                          rewardsStatus: rewardsStatus,
                          customerID: int.parse(widget.customerID),
                          businessCatalog: widget.businessCatalog,
                          employeeProfile: widget.employeeProfile),
                    ));
              else
                Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (BuildContext context) => CartCheckOutPage(
                          title: widget.title,
                          token: widget.token,
                          rewardsStatus: rewardsStatus,
                          customerID: int.parse(widget.customerID),
                          businessCatalog: widget.businessCatalog,
                          employeeProfile: widget.employeeProfile),
                    ));

            },
            hoverElevation: 70.0,
          ),
        ]),
      )),
      drawer: BusinessProfilePage(employeeProfile: widget.employeeProfile),
    );
  }

  GridView _populateItemGridView(orientation, int categoryIndex) {
    var size = MediaQuery.of(context).size;
    var itemHeightLandscape = (size.height / 3.5);
    var itemHeightPortrait = (size.height / 5);

    final double itemHeight = orientation == Orientation.portrait
        ? itemHeightPortrait
        : itemHeightLandscape;

    return GridView.count(
      crossAxisCount: orientation == Orientation.portrait ? 2 : 3,
      crossAxisSpacing: 10.0,
      childAspectRatio: orientation == Orientation.portrait ? 1.1 : 1.3,
      children: List.generate(
          widget.businessCatalog.categoryDataModel[categoryIndex].itemDataModel
              .length, (itemIndex) {
        return Container(
          //height: 200.0,
          //constraints: BoxConstraints(minHeight: itemHeight/2, maxWidth: itemWidth),
          child: new Card(
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10.0),
            ),
            elevation: 10.0,
            margin: EdgeInsets.all(10.0),
            semanticContainer: true,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                Material(
                  child: InkWell(
                    splashColor: Colors.blue[300],
                    onTap: () {
                      _addProduct(categoryIndex, itemIndex);
                    },
                    child: Container(
                      width: size.width,
                      child: new Image.network(
                        widget.businessCatalog.categoryDataModel[categoryIndex]
                            .itemDataModel[itemIndex].itemImagePath,
                        //fit: BoxFit.fill,
                        alignment: Alignment.topCenter,
                        height: itemHeight,
                      ),
                    ),
                  ),
                ),
                new Expanded(
                  flex: 2,
                  child: new Center(
                    child: new Column(
                      children: <Widget>[
                        //SizedBox(height: 1.0),
                        new Text(
                          widget
                              .businessCatalog
                              .categoryDataModel[categoryIndex]
                              .itemDataModel[itemIndex]
                              .itemName,
                          style: new TextStyle(
                            fontSize: 15.0,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
//                        SizedBox(
//                          height: 2.0,
//                        ),
                        Container(
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.center,
                            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                            children: <Widget>[
                              new IconButton(
                                icon: new Icon(Icons.remove_circle_outline),
                                color: Colors.black,
                                onPressed: () {
                                  _removeProduct(categoryIndex, itemIndex);
                                },
                              ),
                              Text(
                                  '${widget.businessCatalog.categoryDataModel[categoryIndex].itemDataModel[itemIndex].itemQuantity}',
                                  style: new TextStyle(fontSize: 20.0)),
                              new IconButton(
                                icon: new Icon(Icons.add_circle_outline),
                                color: Colors.black,
                                onPressed: () {
                                  _addProduct(categoryIndex, itemIndex);
                                },
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      }),
    );
  }

  /*Rewards Redemption API GET Request
  * Populate all the rewards that the customer is eligible for
  */
  Future<RewardsProgramDataModel> createGETRewardsRedeem(
      String host, String path) {
    var queryParameters = {
      'business': widget.employeeProfile.business[0].businessID.toString(),
      'customer': widget.customerID
    };

    var url = Uri.https(host, path, queryParameters);

    print("Rewards API URL: " + url.toString());

    return http.get(url, headers: {
      HttpHeaders.authorizationHeader: 'Token ${widget.token}',
      HttpHeaders.contentTypeHeader: 'application/json',
    }).then((http.Response response) {
      final int statusCode = response.statusCode;
      print("Rewards API Status: " +
          statusCode.toString() +
          " Token Id: " +
          widget.token +
          "Response: " +
          '${response.body}');

      if (statusCode == 200) {
        rewardsStatus = statusCode;
        return RewardsProgramDataModel.fromJson(json.decode(response.body));
      } else
        throw new Exception('Error while fetching data for ' + widget.token);
    });
  }
}

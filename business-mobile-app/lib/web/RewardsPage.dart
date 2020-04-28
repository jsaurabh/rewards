import 'package:digital_rewards/data/RewardsProgramDataModel.dart';
import 'package:flutter/material.dart';
import 'package:digital_rewards/utils/Const.dart';

class RewardsPage extends StatefulWidget {
  final RewardsProgramDataModel rewardsData;

  RewardsPage({Key key, @required this.rewardsData}) : super(key: key);

  @override
  _RewardsPageState createState() => new _RewardsPageState();
}

class _RewardsPageState extends State<RewardsPage>
    with SingleTickerProviderStateMixin {
  TabController _tabController;
  List itemList = [];
  int _tabCurrentIndex = 0;
  int _accumulatedRewards = 0;

  int get getTotalRewards => _accumulatedRewards;

  void _handleTabSelection() {
    setState(() {
      _tabCurrentIndex = _tabController.index;
      _accumulatedRewards = widget
          .rewardsData.redemptionDataModel[_tabCurrentIndex].currentRewards;
    });
  }

  void _calculateRewards(int rewardsIndex, int rewardsPoints) {
    int rewardsValue = getTotalRewards + rewardsPoints;

    setState(() {
      if (rewardsValue >= 0) {
        _accumulatedRewards += rewardsPoints;
        widget.rewardsData.redemptionDataModel[_tabCurrentIndex]
            .currentRewards = _accumulatedRewards;

        widget.rewardsData.redemptionDataModel[_tabCurrentIndex]
            .rewardsDataModel[rewardsIndex].buttonDisable = false;
      } else
        widget.rewardsData.redemptionDataModel[_tabCurrentIndex]
            .rewardsDataModel[rewardsIndex].buttonDisable = true;
    });
  }
  
  //Increment the Qty of the item
  void _addProduct(int currencyIndex, int rewardsIndex) {
    int rewardsPoints = widget.rewardsData.redemptionDataModel[currencyIndex]
        .rewardsDataModel[rewardsIndex].rewardValue;

    setState(() {
      if (getTotalRewards - rewardsPoints >= 0)
        widget.rewardsData.redemptionDataModel[currencyIndex]
            .rewardsDataModel[rewardsIndex].itemQuantity++;
    });

    _calculateRewards(rewardsIndex, -rewardsPoints);
  }
  
  //Decrement the Qty of the item
  void _removeProduct(int currencyIndex, int rewardsIndex) {
    int rewardsPoints = widget.rewardsData.redemptionDataModel[currencyIndex]
        .rewardsDataModel[rewardsIndex].rewardValue;

    setState(() {
      if (widget.rewardsData.redemptionDataModel[currencyIndex]
              .rewardsDataModel[rewardsIndex].itemQuantity !=
          0) {
        widget.rewardsData.redemptionDataModel[currencyIndex]
            .rewardsDataModel[rewardsIndex].itemQuantity--;

        _calculateRewards(rewardsIndex, rewardsPoints);
      }
    });
  }

  @override
  void initState() {
    super.initState();
    _tabController = TabController(
        length: widget.rewardsData.redemptionDataModel.length, vsync: this);
    _tabController.addListener(_handleTabSelection);
    _accumulatedRewards =
        widget.rewardsData.redemptionDataModel[_tabCurrentIndex].currentRewards;
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final Orientation orientation = MediaQuery.of(context).orientation;

    return Scaffold(
      appBar: AppBar(
        title: Text(Const.label_rewards_title),
        bottom: TabBar(
          isScrollable: true,
          tabs: List<Widget>.generate(
              widget.rewardsData.redemptionDataModel.length, (int index) {
            return new Tab(
              text:
                  '${widget.rewardsData.redemptionDataModel[index].currencyDataModel.label} : ${widget.rewardsData.redemptionDataModel[index].currentRewards}',
            );
          }),
          controller: _tabController,
        ),
      ),
      body: TabBarView(
        children: List<Widget>.generate(
            widget.rewardsData.redemptionDataModel.length, (int index) {
          return _populateItemGridView(orientation, index);
        }),
        controller: _tabController,
      ),
    );
  }

  GridView _populateItemGridView(orientation, currencyIndex) {
    var size = MediaQuery.of(context).size;
    var itemHeightLandscape = (size.height / 3.5);
    var itemHeightPortrait = (size.height / 5);

    final double itemHeight = orientation == Orientation.portrait
        ? itemHeightPortrait
        : itemHeightLandscape;

    return GridView.count(
      crossAxisCount: orientation == Orientation.portrait ? 2 : 3,
      crossAxisSpacing: 10.0,
      childAspectRatio: orientation == Orientation.portrait ? 1.0 : 1.2,
      children: List.generate(
          widget.rewardsData.redemptionDataModel[currencyIndex].rewardsDataModel
              .length, (rewardsIndex) {
        bool buttonDisable = widget
            .rewardsData
            .redemptionDataModel[currencyIndex]
            .rewardsDataModel[rewardsIndex]
            .buttonDisable;
        return Container(
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
                      if (buttonDisable == false)
                        _addProduct(currencyIndex, rewardsIndex);
                    },
                    child: Container(
                      width: size.width,
                      //child: FadeInImage(image: NetworkImage(url), placeholder: AssetImage(assetName)
                      child: FadeInImage.assetNetwork(
                        placeholder: 'assets/images/Rewards_default.jpg',
                        image: 'https://' +
                            Const.API_HOST +
                            widget
                                .rewardsData
                                .redemptionDataModel[currencyIndex]
                                .rewardsDataModel[rewardsIndex]
                                .rewardsImage,
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
                        //SizedBox(height: 5.0),
                        new Text(
                          widget.rewardsData.redemptionDataModel[currencyIndex]
                              .rewardsDataModel[rewardsIndex].rewardsName,
                          style: new TextStyle(
                            fontSize: 15.0,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        new Text(
                            widget
                                    .rewardsData
                                    .redemptionDataModel[currencyIndex]
                                    .rewardsDataModel[rewardsIndex]
                                    .rewardValue
                                    .toString() +
                                " " +
                                widget
                                    .rewardsData
                                    .redemptionDataModel[currencyIndex]
                                    .currencyDataModel
                                    .label,
                            style: new TextStyle(
                              fontSize: 15.0,
                            )),
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
                                  _removeProduct(currencyIndex, rewardsIndex);
                                },
                              ),
                              Text(
                                  '${widget.rewardsData.redemptionDataModel[currencyIndex].rewardsDataModel[rewardsIndex].itemQuantity}',
                                  style: new TextStyle(fontSize: 20.0)),
                              new IconButton(
                                icon: new Icon(Icons.add_circle_outline),
                                color: buttonDisable == true
                                    ? Colors.grey
                                    : Colors.black,
                                onPressed: () {
                                  if (buttonDisable == false)
                                    _addProduct(currencyIndex, rewardsIndex);
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
}

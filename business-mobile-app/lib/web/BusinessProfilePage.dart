import 'package:digital_rewards/data/EmployeeDataModel.dart';
import 'package:digital_rewards/utils/Const.dart';
import 'package:digital_rewards/web/LoginPage.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class BusinessProfilePage extends StatefulWidget {
  final EmployeeDataModel employeeProfile;

  BusinessProfilePage({this.employeeProfile});

  @override
  _BusinessProfilePageState createState() => _BusinessProfilePageState();
}

class _BusinessProfilePageState extends State<BusinessProfilePage> {
  bool _isVisible = true;

  @override
  Widget build(BuildContext context) {
    return profileDrawer();
  }
  
  //Side drawer with Profile Info
  Widget profileDrawer() {
    return Drawer(
      child: Container(
        padding: EdgeInsets.all(10.0),
        child: new Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            Container(
              height: 120,
              width: 120,
              decoration: new BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(
                      color: Colors.black,
                      width: 2.0,
                      style: BorderStyle.solid),
                  image: new DecorationImage(
                      fit: BoxFit.fitWidth,
                      image: new NetworkImage(Const.url_businessLogo +
                          widget.employeeProfile.business[0].businessLogo))
              ),
            ),

            SizedBox(
              height: 5.0,
            ),
            Container(
              padding: EdgeInsets.all(10.0),
            ),
            Text(
              widget.employeeProfile.userName,
              textAlign: TextAlign.start,
              style: TextStyle(fontSize: 20.0),
            ),
            Text(
              widget.employeeProfile.emailID,
              textAlign: TextAlign.left,
              style: TextStyle(fontSize: 20.0),
            ),
            SizedBox(
              height: 5.0,
            ),
            InkWell(
                child: new Text(
                  "${Const.label_logout}",
                  style: TextStyle(
                      fontSize: 23.0,
                      color: Colors.blue[900],
                      fontWeight: FontWeight.bold,
                      decoration: TextDecoration.underline),
                ),
                onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (BuildContext context) => LoginPage()))),
          ],
        ),
      ),
    );
  }
}

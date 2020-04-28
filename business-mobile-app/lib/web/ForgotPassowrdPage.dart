import 'package:flutter/material.dart';
import 'package:digital_rewards/utils/Const.dart';

class ForgotPasswordPage extends StatelessWidget {
  const ForgotPasswordPage();

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: forgotPasswordBody(),
      ),
    );
  }

  forgotPasswordBody() =>
      SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: <Widget>[passwordFields()],
        ),
      );

  passwordFields() =>
      Container(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            FlutterLogo(
              colors: Colors.blue,
              size: 80.0,
            ),
            SizedBox(
              height: 30.0,
            ),
            Text('It\u0027s okay, We are here to help you rest your password!'),
            Container(
              padding: EdgeInsets.symmetric(vertical: 16.0, horizontal: 30.0),
              child: TextField(
                maxLines: 1,
                decoration: InputDecoration(
                  hintText: "Enter your email",
                  labelText: "${Const.label_email}",
                ),
              ),
            ),
            SizedBox(
              height: 30.0,
            ),
            Container(
              padding: EdgeInsets.symmetric(vertical: 0.0, horizontal: 30.0),
              width: double.infinity,
              child: RaisedButton(
                padding: EdgeInsets.all(12.0),
                shape: StadiumBorder(),
                child: Text(
                  "${Const.button_reset_password}",
                  style: TextStyle(color: Colors.white),
                ),
                color: Colors.blueAccent,
                onPressed: () {
                  //Redirect to a new Page
                },
              ),
            ),
          ],
        ),
      );
}
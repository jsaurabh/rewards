import 'dart:async';
import 'dart:convert';
import 'package:digital_rewards/web/CustomerCheckInPage.dart';
import 'package:http/http.dart' as http;
import 'package:flushbar/flushbar_route.dart';
import 'package:flushbar/flushbar.dart';
import 'package:flutter/material.dart';
import 'package:digital_rewards/data/LoginDataModel.dart';
import 'package:digital_rewards/utils/Const.dart';

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => new _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final GlobalKey<ScaffoldState> _scaffoldKey = new GlobalKey<ScaffoldState>();
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  bool _autoValidate = false;
  bool _obscureText = true;
  String _userName;
  String _userPassword;

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      key: _scaffoldKey,
      backgroundColor: Colors.white,
      body: Center(
        child: loginBody(context),
      ),
    );
  }

  loginHeader() => Column(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: <Widget>[
          Image.asset(
            'assets/images/Loyal_Blues.jpg',
            height: 150.0,
          ),
          SizedBox(
            height: 20.0,
          ),
          Text(
            "Welcome to ${Const.appName}",
            style: TextStyle(
                fontWeight: FontWeight.w700, color: Colors.blueAccent),
          ),
          SizedBox(
            height: 5.0,
          ),
          Text(
            "Sign in with your UBLoyal Account",
            style: TextStyle(color: Colors.grey),
          ),
          SizedBox(
            height: 5.0,
          ),
        ],
      );

  loginBody(BuildContext context) => SingleChildScrollView(
    child: Column(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: <Widget>[
        loginHeader(),
        new Form(
            key: _formKey,
            autovalidate: _autoValidate,
            child: loginFields(context))
      ],
    ),
  );

  loginFields(BuildContext context) => Container(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            Container(
              padding: EdgeInsets.symmetric(vertical: 16.0, horizontal: 30.0),
              child: TextFormField(
                maxLines: 1,
                keyboardType: TextInputType.emailAddress,
                decoration: InputDecoration(
                  hintText: "Enter your username",
                  labelText: "${Const.label_user_name}",
                ),
                validator: (userName) => validateUserName(userName),
                onSaved: (String userName) =>
                    setState(() => _userName = userName),
              ),
            ),
            Container(
              padding: EdgeInsets.symmetric(vertical: 0.0, horizontal: 30.0),
              child: TextFormField(
                maxLines: 1,
                obscureText: _obscureText,
                decoration: InputDecoration(
                  hintText: "Enter your password",
                  labelText: "${Const.label_password}",
                  suffixIcon: GestureDetector(
                    onTap: () {
                      setState(() {
                        _obscureText = !_obscureText;
                      });
                    },
                    child: Icon(
                      _obscureText ? Icons.visibility : Icons.visibility_off,
                      semanticLabel:
                          _obscureText ? 'show password' : 'hide password',
                    ),
                  ),
                ),
                validator: (password) => validatePassword(password),
                onSaved: (String password) =>
                    setState(() => _userPassword = password),
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
                  "${Const.button_login}",
                  style: TextStyle(color: Colors.white),
                ),
                color: Colors.blueAccent,
                onPressed: () async {
                  if (validateInputs()) {
                    LoginDataModel loginDataModel = new LoginDataModel(
                        userName: _userName, userPassword: _userPassword);

                    LoginDataModel login = await createPostRequest(
                        Const.API_HOST, Const.API_LOGIN_PATH,
                        requestBody: loginDataModel.mapRequestBody());

                    //User is an employee of a business
                    if (login != null)
                      Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (BuildContext context) =>
                                CustomerCheckInPage(
                                    title:
                                        login.employee.business[0].businessName,
                                    token: login.token,
                                    employeeProfile: login.employee),
                          ));
                    else{
                      showInFlushBar();
                    }
                  }
                },
              ),
            ),
//            SizedBox(
//              height: 10.0,
//            ),
//            Container(
//              child: new InkWell(
//                  child: new Text(
//                    "${Const.link_forgot_password}",
//                    style: TextStyle(
//                        color: Colors.grey,
//                        decoration: TextDecoration.underline),
//                  ),
//                  onTap: () => Navigator.push(
//                      context,
//                      MaterialPageRoute(
//                          builder: (BuildContext context) =>
//                              ForgotPasswordPage()))),
//            )
          ],
        ),
      );

  /*Login POST Request
  * Employee Login returns Auth Token
  * with Employee Data
  */
  Future<LoginDataModel> createPostRequest(String host, String path,
      {Map requestBody}) {
    var url = Uri.https(host, path);

    return http.post(url, body: requestBody).then((http.Response response) {
      final int statusCode = response.statusCode;

      /*print("Login Status: " +
          statusCode.toString() +
          " Response: " +
          '${response.body}');*/

      if (statusCode == 200) {
        return LoginDataModel.fromJson(json.decode(response.body));
      }else if(statusCode == 400){
        return null;
      }else
        throw new Exception('Error while fetching data');
    });
  }

  //FlushBar for Invalid Login Credentials
  void showInFlushBar() {
    Flushbar flushBar = Flushbar(
      messageText: new Text(Const.error_auth_login,
          style: TextStyle(fontSize: 15.0, color: Colors.white)),
      duration: new Duration(seconds: 4),
      flushbarStyle: FlushbarStyle.FLOATING,
      flushbarPosition: FlushbarPosition.TOP,
      borderRadius: 10,
      margin: EdgeInsets.all(8),
    )..show(context);
    showFlushbar(context: context, flushbar: flushBar);
  }

  //Form Input Validation
  String validateUserName(String userName) {
    RegExp regex = new RegExp(r'^[a-zA-Z0-9]+$', caseSensitive: false);

    if (userName.isEmpty) return Const.validation_userName_Empty;
    if (userName.length < 3 || userName.length > 150)
      return Const.validation_userName_Length;
    if (!regex.hasMatch(userName)) return Const.validation_userName_invalid;

    return null;
  }
  
  //Form Input Validation
  String validatePassword(String userPassword) {
    if (userPassword.isEmpty) return Const.validation_userPassword_Empty;
    if (userPassword.length < 8)
      return Const.validation_userPassword_Length;

    return null;
  }
  
  //Form Input Validation
  bool validateInputs() {
    if (_formKey.currentState.validate()) {
      _formKey.currentState.save();
      return true;
    } else {
      setState(() {
        _autoValidate = true;
      });
      return false;
    }
  }
}

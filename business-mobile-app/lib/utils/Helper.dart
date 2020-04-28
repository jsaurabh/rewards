import 'package:flutter/material.dart';
import 'package:flushbar/flushbar_route.dart';
import 'package:flushbar/flushbar.dart';

class Helper {

  //FlushBar for general notification
  static void showInFlushBar(String message, BuildContext context) {
    Flushbar flushBar = Flushbar(
      messageText: new Text(message,
          style: TextStyle(fontSize: 15.0, color: Colors.white)),
      duration: new Duration(seconds: 4),
      flushbarStyle: FlushbarStyle.FLOATING,
      flushbarPosition: FlushbarPosition.TOP,
      borderRadius: 10,
      margin: EdgeInsets.all(8),
    )..show(context);
    showFlushbar(context: context, flushbar: flushBar);
  }

  //FlushBar for Transaction Alerts
  static void showInTransactionAlert(String message, IconData iconData,
      Color colorValue, BuildContext context) {
    Flushbar flushBar = Flushbar(
      icon: Icon(
        iconData,
        color: colorValue,
      ),
      messageText: new Text(message,
          style: TextStyle(fontSize: 15.0, color: Colors.white)),
      duration: new Duration(seconds: 4),
      flushbarStyle: FlushbarStyle.FLOATING,
      flushbarPosition: FlushbarPosition.TOP,
      borderRadius: 10,
      margin: EdgeInsets.all(8),
    )..show(context);
    showFlushbar(context: context, flushbar: flushBar);
  }
}
import 'package:digital_rewards/utils/Const.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:digital_rewards/web/LoginPage.dart';

void main(){
  runApp(LandingPage());
}

class LandingPage extends StatelessWidget{
  @override
  Widget build(BuildContext context){
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: '${Const.appName}',
      home: LoginPage(),
      //home: Catalog(),
    );
  }
}

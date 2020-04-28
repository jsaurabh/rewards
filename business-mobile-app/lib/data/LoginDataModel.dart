import 'package:digital_rewards/data/EmployeeDataModel.dart';

  /*
  *POST-
  * curl http://webdev.cse.buffalo.edu:8000/rewards/users/auth/login/ -d 'username=23456&password=UBLoyal'
  *
  * Response:
  * {
  * "token":"71a33849043d53659748a0ac2f773c6b4cea4674",
  * "user":{
  *     "id":2,
  *     "first_name":"Two",
  *     "last_name":"Six",
  *     "username":"23456",
  *     "email":"rewards-23456@example.org"
  *   }
  * }
  *
  */

class LoginDataModel{
  //JSON Request
  final String userName;
  final String userPassword;

  //JSON Response
  final String token;
  final EmployeeDataModel employee;

  LoginDataModel({this.userName, this.userPassword, this.token, this.employee});

  //JSON Request
  Map mapRequestBody(){
    var map = new Map<String, dynamic>();
    map['username'] = userName;
    map['password'] = userPassword;

    return map;
  }

  //Mapping JSON Response
  factory LoginDataModel.fromJson(Map<String, dynamic> jsonData){
    return LoginDataModel(
      token: jsonData['token'],
      employee : EmployeeDataModel.fromJson(jsonData['user']),
    );
  }

}
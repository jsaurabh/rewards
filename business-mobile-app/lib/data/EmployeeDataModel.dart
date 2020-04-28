import 'package:digital_rewards/data/BusinessDataModel.dart';

class EmployeeDataModel{

  final int employeeID;
  final String userName;
  final String firstName;
  final String lastName;
  final String emailID;
  final String phoneNumber;

  final List<BusinessDataModel> business;

  EmployeeDataModel({this.employeeID, this.userName, this.firstName, this.lastName, this.emailID, this.phoneNumber, this.business});

  factory EmployeeDataModel.fromJson(Map<String, dynamic> jsonData){
    var employeeOfBusiness = jsonData['employee_of'] as List;
    List<BusinessDataModel> employeeOfBusinessList = employeeOfBusiness.map((i) => BusinessDataModel.fromJson(i)).toList();

    return EmployeeDataModel(
      employeeID : jsonData['id'],
      userName : jsonData['username'],
      firstName : jsonData['first_name'],
      lastName : jsonData['last_name'],
      emailID : jsonData['email'],
      phoneNumber: jsonData['phone'],
      business: employeeOfBusinessList,
    );
  }
}
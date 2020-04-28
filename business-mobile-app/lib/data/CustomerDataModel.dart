/* GET Request:
* URL - /rewards/programs/customers/{businessId}/?phone={customerPhoneNumber}
*                         OR
*       /rewards/programs/customers/{businessId}/?id={customerId}
*
* curl -H "Authorization: Token f432ebdbcfa936048d1d6b80002f42eeb07f669e" -H "Content-Type: application/json" https://webdev.cse.buffalo.edu/rewards/programs/customers/4/?phone=7167890123
* Response: [{"id":4,"first_name":"Four","last_name":"Eight"}]
* */

class CustomerDataModel{
  final int customerID;
  final String firstName;
  final String lastName;

  CustomerDataModel({this.customerID, this.firstName, this.lastName});

  factory CustomerDataModel.fromJson (Map<String, dynamic> jsonData){
    return CustomerDataModel(
      customerID: jsonData['id'],
      firstName: jsonData['first_name'],
      lastName: jsonData['last_name'],
    );
  }
}
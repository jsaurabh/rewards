class BusinessDataModel{

  final int businessID;
  final String businessName;
  final String businessLogo;

  BusinessDataModel({this.businessID, this.businessName, this.businessLogo});

  factory BusinessDataModel.fromJson(Map<String, dynamic> jsonData){
    return BusinessDataModel(
      businessID: jsonData['id'],
      businessName: jsonData['name'],
      businessLogo: jsonData['logo'],
    );
  }
}
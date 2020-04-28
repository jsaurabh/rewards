import 'package:digital_rewards/data/CatalogDataModel.dart';
import 'package:digital_rewards/data/CustomerDataModel.dart';
import 'package:digital_rewards/data/EmployeeDataModel.dart';
import 'package:digital_rewards/utils/Const.dart';
import 'package:digital_rewards/utils/Helper.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:barcode_scan/barcode_scan.dart';
import 'package:flutter/services.dart';
import 'package:digital_rewards/web/BusinessProfilePage.dart';
import 'package:digital_rewards/web/Catalog.dart';
import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

class CustomerCheckInPage extends StatefulWidget {
  final String title;
  final String token;
  final EmployeeDataModel employeeProfile;

  CustomerCheckInPage(
      {@required this.title,
      @required this.token,
      @required this.employeeProfile});

  @override
  _CustomerCheckInPageState createState() => new _CustomerCheckInPageState();
}

class _CustomerCheckInPageState extends State<CustomerCheckInPage> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  bool _autoValidate = false;
  bool snapShotStatus = false;
  String _customerPhoneNumber;
  String _qrCodeSnapshotData;

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final Orientation orientation = MediaQuery.of(context).orientation;

    return new Scaffold(
        drawer: BusinessProfilePage(employeeProfile: widget.employeeProfile),
        appBar: AppBar(
          title: Text(widget.title),
        ),
        body: new Form(
          key: _formKey,
          autovalidate: _autoValidate,
          child: customerCheckInInBody(orientation),
        ));
  }

  Widget customerCheckInInBody(Orientation orientation) => Column(
        children: <Widget>[
          Expanded(
            flex: 2,
            child: Flex(
              direction: orientation == Orientation.landscape
                  ? Axis.horizontal
                  : Axis.vertical,
              children: <Widget>[
                Container(
                  child: Center(
                    heightFactor: 4.5,
                    child: Container(
                      padding: EdgeInsets.symmetric(
                          vertical: 0.0, horizontal: 150.0),
                      height: 70.0,
                      child: FloatingActionButton.extended(
                        onPressed: () async {
                          startQRScan();

                          if (snapShotStatus) {
                            var queryParam = {'id': _qrCodeSnapshotData};

                            CustomerDataModel customer =
                                await createCustomerGetRequest(Const.API_HOST,
                                    Const.API_CUSTOMER_PATH, queryParam);

                            CatalogDataModel catalog =
                                await createCatalogGetRequest(
                                    Const.API_HOST, Const.API_CATALOG_PATH);
            

                            if (customer.customerID != null &&
                                catalog.categoryDataModel.isNotEmpty) {
                              Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (BuildContext context) => Catalog(
                                        title: widget.title,
                                        token: widget.token,
                                        employeeProfile: widget.employeeProfile,
                                        businessCatalog: catalog,
                                        customerID:
                                            customer.customerID.toString()),
                                  ));
                            }
                          } else {
                            //QR Code not scanned
                            Helper.showInFlushBar(_qrCodeSnapshotData, context);
                          }
                        },
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.all(Radius.circular(10.0)),
                        ),
                        backgroundColor: Colors.blue,
                        elevation: 10.0,
                        tooltip: 'Tap to scan',
                        icon: Icon(Icons.filter_center_focus, size: 70.0),
                        label: Text(
                          Const.label_start_scan,
                          style: TextStyle(fontSize: 17.0),
                        ),
                      ),
                    ),
                  ),
                ),
                Container(
                  width: MediaQuery.of(context).size.width / 2.7,
                  child: TextFormField(
                    maxLines: 1,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                        labelText: Const.label_search_user_phoneNumber,
                        labelStyle: TextStyle(fontSize: 17.0),
                        hintText: "Enter the Phone Number",
                        suffixIcon: new IconButton(
                            icon: Icon(Icons.search),
                            color: Colors.black,
                            onPressed: () async {
                              if (validateInputs()) {
                                var queryPram = {'phone': _customerPhoneNumber};

                                CustomerDataModel customer =
                                    await createCustomerGetRequest(
                                        Const.API_HOST,
                                        Const.API_CUSTOMER_PATH,
                                        queryPram);

                                if (customer == null) {
                                  //FlushBar for Phone Number not available
                                  Helper.showInFlushBar(Const.error_phone_number, context);
                                } else {
                                  CatalogDataModel catalog =
                                      await createCatalogGetRequest(
                                          Const.API_HOST,
                                          Const.API_CATALOG_PATH);

                                  if (catalog.categoryDataModel.isNotEmpty) {
                                    Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder: (BuildContext context) =>
                                              Catalog(
                                                  title: widget.title,
                                                  token: widget.token,
                                                  employeeProfile:
                                                      widget.employeeProfile,
                                                  businessCatalog: catalog,
                                                  customerID: customer
                                                      .customerID
                                                      .toString()),
                                        ));
                                  }
                                }
                              }
                            })),
                    validator: (phoneNumber) =>
                        validatePhoneNumber(phoneNumber),
                    onSaved: (String phoneNumber) =>
                        setState(() => _customerPhoneNumber = phoneNumber),
                  ),
                ),
              ],
            ),
          )
        ],
      );

  //Form Input Validation
  String validatePhoneNumber(String phoneNumber) {
    RegExp regExp = new RegExp(r'^(?:[1-9])?[0-9]{10}$');

    if (phoneNumber.isEmpty) return Const.validation_phoneNumber_Empty;
    if (!regExp.hasMatch(phoneNumber))
      return Const.validation_phoneNumber_invalid;

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

  /*QR Code Scanner
  * Scans the QR Code and return the customerID*/
  Future startQRScan() async {
    try {
      String snapShotData = await BarcodeScanner.scan();
      _qrCodeSnapshotData = snapShotData;
      snapShotStatus = true;
      //snapShotStatus = true;
      print("QRSnapShot Data " + _qrCodeSnapshotData);
    } on PlatformException catch (exception) {
      _qrCodeSnapshotData = Const.error_qr_code_platform;
    } on FormatException catch (exception) {
      _qrCodeSnapshotData = Const.error_qr_code_format;
    } catch (exception) {
      _qrCodeSnapshotData = Const.error_generic;
      print('Unkown Error: ' + exception.toString());
    }
  }


  /*Catalog API GET Request
  * Populate all the Category and Items of the business
  */
  Future<CatalogDataModel> createCatalogGetRequest(String host, String path) {
    var url = Uri.https(
        host, path + '${widget.employeeProfile.business[0].businessID}');

    //print("Catalog API URL: " + url.toString());

    return http.get(url, headers: {
      HttpHeaders.authorizationHeader: 'Token ${widget.token}',
      HttpHeaders.contentTypeHeader: 'application/json',
    }).then((http.Response response) {
      final int statusCode = response.statusCode;
      /*print("Catalog API Status: " +
          statusCode.toString() +
          " Token Id: " +
          widget.token +
          " Response: " +
          '${response.body}');*/

      if (statusCode == 200) {
        return CatalogDataModel.fromJson(json.decode(response.body));
      } else
        throw new Exception('Error while fetching data for ' + widget.token);
    });
  }

  /*Customer API GET Request
  with either UserId QR Code Data or User Phone Number
   */
  Future<CustomerDataModel> createCustomerGetRequest(
      String host, String path, Map queryParameter) {
    var url = Uri.https(
        host,
        path + '${widget.employeeProfile.business[0].businessID}/',
        queryParameter);

    //print('Customer API URL: ' + url.toString());

    return http.get(url, headers: {
      HttpHeaders.authorizationHeader: 'Token ${widget.token}',
      HttpHeaders.contentTypeHeader: 'application/json',
    }).then((http.Response response) {
      final int statusCode = response.statusCode;
      /*print("Customer API Status: " +
          statusCode.toString() +
          " Token Id: " +
          widget.token +
          " Response: " +
          '${response.body}');*/

      if (statusCode == 200) {
        var customers = json.decode(response.body);
        if (customers.isNotEmpty)
          return CustomerDataModel.fromJson(customers[0]);
        else
          return null;
      } else
        throw new Exception('Error while fetching data for ' + widget.token);
    });
  }
}

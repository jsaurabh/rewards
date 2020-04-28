class Const{
  static const String appName = "UBLoyal";
  static const String url_businessLogo = 'https://webdev.cse.buffalo.edu';
  //API URL
  static const String API_HOST = 'webdev.cse.buffalo.edu';
  static const String API_LOGIN_PATH = '/rewards/users/auth/login/';
  static const String API_CATALOG_PATH = '/rewards/catalog/business/';
  static const String API_CUSTOMER_PATH = '/rewards/programs/customers/';
  static const String API_REWARDS_REDEEM_PATH ='/rewards/rewards/redeem/';
  static const String API_ORDERS_PATH = '/rewards/orders/';

  //Login Page
  static const String label_user_name = "Username";
  static const String label_password = "Password";
  static const String button_login = "SIGN IN";

  static const String error_auth_login = 'Unable to login with provided credentials!';

  //Forgot Password Page - Future Improvements
  static const String link_forgot_password = "FORGOT PASSWORD?";
  static const String label_email = "Email";
  static const String button_reset_password = "RESET PASSWORD";

  //Rewards
  static const String label_rewards_title = 'Rewards';

  //QR Scanner
  static const String label_start_scan = 'Start Camera Scan';
  static const String label_search_user_phoneNumber = 'Search with Phone Number';
  static const String button_proceed_CatalogPage = 'Proceed to Catalog';

  static const String error_phone_number = 'Customer Phone Number not registered!';
  static const String error_qr_code_format = 'You pressed the back button before scanning anything.';
  static const String error_qr_code_platform = 'Camera Permissions not granted.';

  //Catalog
  static const String info_rewards_redeemable = 'Customer has no rewards redeemable!';

  //Profile
  static const String label_logout = 'Logout';

  //Cart CheckOut
  static const String title_checkout = 'Cart Check Out';
  static const String label_order_details = 'Order Summary';
  static const String button_submit_order = 'Submit Order';

  static const String success_order_rewards = 'Orders and Rewards Successful!';
  static const String success_order = 'Order processed Successfully!';
  static const String success_rewards = 'Rewards redeemed Successfully!';
  static const String error_cart_empty = 'Cart is Empty!';
  static const String error_order = 'Transaction Failed!';

  //Default Error
  static const String error_generic = 'Unknown Error, Try Again!';

  //Validation Errors
  static const String validation_userName_Length = 'Username length invalid';
  static const String validation_userName_Empty = 'Enter a Username';
  static const String validation_userName_invalid = 'Username conatins invalid characters';

  static const String validation_userPassword_Length = 'Password length invalid';
  static const String validation_userPassword_Empty = 'Enter the password';

  static const String validation_phoneNumber_Empty = 'Enter the Phone Number';
  static const String validation_phoneNumber_invalid = 'Phone Number invalid';
}
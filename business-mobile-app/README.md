# Business App

The business employee app lets employees at the checkout associate purchase information with rewards. It displays the Catalog of the business along with the rewards points earned by the customer enrolled in the business rewards program.

1. Once the employee logins-in, they are prompted with a screen to either Scan the OR code of the customer or enter the phone number.
2. The API calls verify that the customer is an enrolled user of the business rewards program.
3. On success, the employee is displayed in the business catalog.
4. They can select the items that are being ordered by the customer today as well as view any rewards that the customer has accumulated.
5. Business Owners who have signed up with their businesses can have multiple rewards campaigns running for their customers as per their liking. This allows them to incentivize customers to earn rewards on different currencies for their special campaigns.
6. The Employee at check out can now view the ordered and rewards items in the cart.
7. On check out, an API call is made to added new accumulated rewards for their orders as well as redeem the accumulated points with reward offers.


## Future Improvements

Currently, the app supports one business per employee.
The app deals with a lot of image content so it would be advised to cache the images in the network.


## Getting Started

This project is a starting point for a Flutter application.
A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://flutter.dev/docs/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://flutter.dev/docs/cookbook)
- [Material Design: Design guidelines](https://material.io/)

For help getting started with Flutter, view the
[online documentation](https://flutter.dev/docs), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

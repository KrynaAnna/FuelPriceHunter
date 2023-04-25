### <a href="http://annak.pythonanywhere.com/">Use Web App</a>
<p align="center">
  <img src="https://user-images.githubusercontent.com/98818064/234134926-3b7bf138-a142-488b-9fc0-803706edb685.png" width="52px">
  <br>
  <strong>Fuel Price Hunter</strong>
</p>

## Overview:
This documentation outlines the features and functionality of the Fuel Price Hunter web app, including how to install and use it. The web app is written in Python language using Flask framework and utilizes the Courier API to send notifications by email. 
It accesses the user data from a MySQL database table, uses the ApifyClient library to retrieve gas prices for the user's specified location and fuel type, and sends the information by email using the trycourier library. The program runs in a loop, iterating over the rows in the user table, and updating the next_date field in the database based on the frequency of the checks (every day, once a week, twice a month, or once a month). 

## Features
<li>User authentication: The web app allows users to create an account, login, and logout.
<li>Fuel subscription: Once logged in, users can create a fuel subscription by selecting the type of fuel, province, city, and the frequency of notifications.
<li>Notification settings: Users can customize their notification preferences by selecting the time of day to receive notifications and the email address to receive notifications.
<li>Courier API integration: The web app utilizes the Courier API to send notifications to users via email.

## Usage
1. Navigate to http://annak.pythonanywhere.com to access the login page.
2. Create an account or login with existing credentials.
3. Once logged in, you will be redirected to the fuel subscription page.
4. Select the type of fuel, province, city, and frequency of notifications, then click "Subscribe".
5. Customize your notification preferences by selecting the time of day to receive notifications and the email address to receive notifications.
6. To stop the subscription, click "Unsubscribe" from the fuel subscription page.


## Installation
1. Clone the repository: git clone https://github.com/KrynaAnna/fuelpricehunter.git
2. Install dependencies: pip install -r requirements.txt
3. Set environment variables: export COURIER_AUTH_TOKEN=<your_token>
4. Start the app: python main.py

## Main dependencies:
<li>Flask 2.2.3
<li>Flask-SQLAlchemy 3.0.3
<li>Trycourier 4.4.0
<li>Apify-client 1.0.0

## Routes:
<li>'/': The home page route.
<li>'/register': The registration page route.
<li>'/login': The login page route.

## Files:
<li>app.py: Contains the main Flask application code.
<li>additional.py: Contains the list of provinces used in the application.
<li>data.db: Contains the database used by the application.
<li>checker.py: Contains the program that checks gas prices for users and sends them a notification via email if their scheduled check date matches the current date. 

## Courier API integration
The web app utilizes the Courier API to send notifications to users via email. To use the Courier API, you will need to sign up for a Courier account and obtain an API key. Once you have obtained an API key, set the COURIER_AUTH_TOKEN environment variable to your API key.
<br></br>
Notifications are sent via the send endpoint of the Courier API. To send a notification, make a POST request to the send endpoint with the following parameters:
<li>recipient: The recipient of the notification.
<li>content: The data about prices.

## Design
The design for the Fuel Subscription web app was created using Figma, and the front-end was built using HTML, CSS, JS, and Bootstrap.
![figma](https://user-images.githubusercontent.com/98818064/234134810-9c5965f2-107e-438c-8699-f1096aa504e5.png)

## Deployment
The Fuel Price Hunter web app is deployed on PythonAnywhere, a cloud-based Python web hosting service.

## Conclusion
Overall, this project provides a convenient way for users to stay informed about gas prices in their city. With the use of APIs and email notifications, users can receive up-to-date information without having to manually check gas prices themselves.


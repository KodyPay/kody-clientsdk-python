# Payments Via Kody

KodyPay supports following ways to execute payment.

1. Kody Terminal
2. Online Payment


## Kody Terminal
Pre-requisite to start payment through Kody Terminal are:

1. Request Kody to order the Kody Terminal.
2. Request Kody to create a Store and configure it as per the requirement.
3. Request Kody to assign Terminal to the Store.
4. Request Kody to generate API Key assigned to the Store. API key is needed for the authorization of the payment request.

Once the above pre-requisite has met, you can start developing the code to make a payment request using the API key.

Following steps are needed:

1. **Kody SDK Client**: The Kody SDK Client allows direct communication with the Kody Payments Gateway. It simplifies the integration of Kody payments into your application.
The SDK is generated from Protobuf gRPC protocols to facilitate communication with the Kody Payments Gateway.
Kody SDK Client are available in following languages:
- Java : https://github.com/KodyPay/kody-clientsdk-java/
- Python: https://github.com/KodyPay/kody-clientsdk-python/
- PHP: https://github.com/KodyPay/kody-clientsdk-php/
- .Net: https://github.com/KodyPay/kody-clientsdk-dotnet/

2. **Get list of Terminals** : Terminals request is made to verify the list of available terminals and to check whether it is online or not.

Key attributes to make a terminal call:
- TerminalsRequest : Request message for fetching terminal status 
```protobuf
message TerminalsRequest {
  string store_id = 1; // UUID of store
}
```
- KodyPayTerminalService : Service used to make the Terminal request.
- KodyPayTerminalService.Terminals: RPC function used to make the Terminal Request
```protobuf
service KodyPayTerminalService {
  rpc Terminals(TerminalsRequest) returns (TerminalsResponse);
}
```
- TerminalsResponse: Response message 

````protobuf
message TerminalsResponse {
  repeated Terminal terminals = 1;
}
message Terminal {
  string terminal_id = 1; // terminal serial number
  bool online = 2;
}
````
3. **Create payment request**: Request to start the payment on the selected terminal.

Key attributes to make a payment call:

- PayRequest : Request message to start payment.
```protobuf
message PayRequest {
  string store_id = 1; // UUID of store
  string amount = 2; // amount in BigDecimal/2.dp (0.00)
  string terminal_id = 3; // send the payment to this terminal serial number
  optional bool show_tips = 4; // Show tips on the terminal
}
```
- KodyPayTerminalService : Service used to make the Payment request.
- KodyPayTerminalService.Pay: RPC function used to make the Payment Request
```protobuf
service KodyPayTerminalService {
  rpc Pay(PayRequest) returns (stream PayResponse);
}
```
- PayResponse : Payment Response

````protobuf
message PayResponse {
  PaymentStatus status = 1;
  optional string failure_reason = 2; // only populated on failure
  optional string receipt_json = 3; // json blob containing the receipt data
  string order_id = 4;
  google.protobuf.Timestamp date_created = 5;
  optional string ext_payment_ref = 6;
  google.protobuf.Timestamp date_paid = 7;
  optional string total_amount = 8;
  optional string sale_amount = 9;
  optional string tips_amount = 10;
}
````

4. **Sample code:** Samples of the code to showcase how to make payment are available in the respective language client sdk.
- Java : https://github.com/KodyPay/kody-clientsdk-java/tree/main/samples/src/main/java/terminal
- Python: https://github.com/KodyPay/kody-clientsdk-python/tree/main/versions/3_12/samples/terminal
- PHP: https://github.com/KodyPay/kody-clientsdk-php/tree/main/samples/php8/pos
- .Net: https://github.com/KodyPay/kody-clientsdk-dotnet/tree/main/samples/ListTerminals,https://github.com/KodyPay/kody-clientsdk-dotnet/tree/main/samples/TerminalPayment 

5. **Create a client:** Use the code given is samples to create a client to make the payment request.

## Online Payment
Online payment is used for ecommerce transaction.

Pre-requisite to start online payment are:

1. Request Kody to create a Store and configure it as per the requirement.
2. Request Kody to generate API Key assigned to the Store. API key is needed for the authorization of the payment request.

Once the above pre-requisite has met, you can start developing the code to make a payment request using the API key.

Following steps are needed:
1. **Kody SDK Client:** Similar to Kody Terminal Payments, Kody SDK Clients can also be used to make Ecommerce payments. Refer to the above section for Kody terminal Payments to find the link to the respective language client.
2. **Create Online Payment:** Request to start payment online.

Key attributes to make a payment call:

- PaymentInitiationRequest : Request message to start online payment.
```protobuf
// Payment Initiation Request
message PaymentInitiationRequest {
  string store_id = 1;  // Your Kody store id
  string payment_reference = 2;   // Your unique reference of this payment request.
  uint64 amount = 3; // Amount in minor units. For example, 2000 means GBP 20.00.
  string currency = 4; // ISO 4217 three letter currency code
  string order_id = 5; // Your identifier of the order. It doesn't have to be unique, for example when the same order has multiple payments.
  optional string order_metadata = 6; // A data set that can be used to store information about the order and used in the payment details. For example a JSON with checkout items. It will be useful as evidence to challenge chargebacks or any risk data.
  string return_url = 7; // The URL that your client application will be redirected to after the payment is authorised. You can include additional query parameters, for example, the user id or order reference.
  optional string payer_statement = 8; // The text to be shown on the payer's bank statement. Maximum 22 characters, otherwise banks might truncate the string. If not set it will use the store's terminals receipt printing name. Allowed characters: a-z, A-Z, 0-9, spaces, and special characters . , ' _ - ? + * /
  optional string payer_email_address = 9; // We recommend that you provide this data, as it is used in velocity fraud checks. Required for 3D Secure 2 transactions.
  optional string payer_ip_address = 10; // The payer IP address used for risk checks, also required for 3D Secure 2 transactions.
  optional string payer_locale = 11; // The language code and country code to specify the language to display the payment pages. It will default to en_GB if not set.
  optional bool tokenise_card = 12; // defaults false 
  optional ExpirySettings expiry = 13; // Nested message for expiry settings

  message ExpirySettings {
    bool show_timer = 1; // Display a countdown timer to the user in the payment page, default is false
    uint64 expiring_seconds = 2; // Timeout duration in seconds, defaults to 1800 seconds (30 minutes)
  } 
}
```
- KodyEcomPaymentsService : Service used to make the Online payment request.
- KodyEcomPaymentsService.InitiatePayment: RPC function used to make online payment.
```protobuf
service KodyEcomPaymentsService {
  // Initiates a payment and returns a URL for the user to complete payment
  rpc InitiatePayment(PaymentInitiationRequest) returns (PaymentInitiationResponse);
}
```
- PaymentInitiationResponse : Payment Response
```protobuf
/ Payment Initiation Response
message PaymentInitiationResponse {
  oneof result {
    Response response = 1;
    Error error = 2;
  }

  message Response {
    string payment_id = 1; // The unique identifier created by Kody
    string payment_url = 2; // The URL to send the user to from your application
  }

  message Error {
    Type type = 1;
    string message = 2;

    enum Type {
      UNKNOWN = 0;
      DUPLICATE_ATTEMPT = 1;
      INVALID_REQUEST = 2;
    }
  }
}
```
The response of the service call will generate a payment url which then can be used to complete the payment.


4. Sample Code: Samples of the code to showcase how to make payment are available in the respective language client sdk.
- Java : https://github.com/KodyPay/kody-clientsdk-java/tree/main/samples/src/main/java/ecom
- Python: https://github.com/KodyPay/kody-clientsdk-python/tree/main/versions/3_12/samples/ecom
- PHP: https://github.com/KodyPay/kody-clientsdk-php/tree/main/samples/php8/ecom-server
- .Net: https://github.com/KodyPay/kody-clientsdk-dotnet/tree/main/samples/ListTerminals,https://github.com/KodyPay/kody-clientsdk-dotnet/tree/main/samples/TerminalPayment 

5. **Create a client:** Use the code given is samples to create a client to make the payment request.

## Get Terminal Payment Details

Pre-requisite to get payment are:

1. Request Kody to create a Store and configure it as per the requirement.
2. Request Kody to generate API Key assigned to the Store. API key is needed for the authorization of the payment request.
3. Existing payment

Steps needed to get payment details are:

1. **Kody SDK Client:** Kody SDK Clients can also be used to get the details of the payment. Refer to the above section for Kody terminal payments to find the link to the respective language client.
2. **Get Payment Details** - Key attributes to make a get payment call:

- PaymentDetailsRequest : Request message to get payment details
```protobuf
message PaymentDetailsRequest {
  string store_id = 1; // UUID of store
  string order_id = 2; // to identify the payment (order)
}
```
- KodyPayTerminalService : Service which define the function to make the respective call.
- KodyPayTerminalService.PaymentDetails: RPC function to make respective call.
```protobuf
service KodyPayTerminalService {
  rpc PaymentDetails(PaymentDetailsRequest) returns (PayResponse);
}
```
- PayResponse - Response of get payment details.
```protobuf
message PayResponse {
  PaymentStatus status = 1;
  optional string failure_reason = 2; // only populated on failure
  optional string receipt_json = 3; // json blob containing the receipt data
  string order_id = 4;
  google.protobuf.Timestamp date_created = 5;
  optional string ext_payment_ref = 6;
  google.protobuf.Timestamp date_paid = 7;
  optional string total_amount = 8;
  optional string sale_amount = 9;
  optional string tips_amount = 10;
}
enum PaymentStatus {
  PENDING = 0;
  SUCCESS = 1;
  FAILED = 2;
  CANCELLED = 3;
}
```
3. **Create a client:** Use the code given is samples to create a client to make the get payment details request.

## Cancel Terminal Payment Details

Pre-requisite to cancel payment are:

1. Request Kody to create a Store and configure it as per the requirement.
2. Request Kody to generate API Key assigned to the Store. API key is needed for the authorization of the payment request.
3. Existing payment

Steps needed to cancel payment:

1. **Kody SDK Client:** Kody SDK Clients can also be used to get the details of the payment. Refer to the above section for Kody terminal payments to find the link to the respective language client.
2. **Cancel Payment** - Following key attributes are required to make a cancel payment call

- CancelRequest : Request message to cancel payment.
```protobuf
message CancelRequest {
  string store_id = 1; // UUID of store
  string amount = 2; // amount in BigDecimal/2.dp (0.00) - to identify the payment to cancel
  string terminal_id = 3; // to identify the terminal where the payment was sent
  optional string order_id = 4; // to identify the payment (order) to cancel
}
```
- KodyPayTerminalService : Service which define the function to make the respective call.
- KodyPayTerminalService.Cancel: RPC function to make respective call.
```protobuf
service KodyPayTerminalService {
  rpc Cancel(CancelRequest) returns (CancelResponse);;
}
```
- CancelResponse - Response of cancel payment.
```protobuf
message CancelResponse {
  PaymentStatus status = 1;
}
enum PaymentStatus {
  PENDING = 0;
  SUCCESS = 1;
  FAILED = 2;
  CANCELLED = 3;
}
```
3. **Create a client:** Use the code given is samples to create a client to make the cancel request.







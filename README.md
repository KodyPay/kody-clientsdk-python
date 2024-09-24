# Kody Payments API

This guide provides an overview of using the Kody Payments API and its reference documentation.

## Client Libraries

Kody provides client libraries for many popular languages to access the APIs. If your desired programming language is supported by the client libraries, we recommend that you use this option.

Available languages:
- Python: https://github.com/KodyPay/kody-clientsdk-python/
- Java : https://github.com/KodyPay/kody-clientsdk-java/
- PHP: https://github.com/KodyPay/kody-clientsdk-php/
- .Net: https://github.com/KodyPay/kody-clientsdk-dotnet/

The advantages of using the Kody Client library instead of a REST API are:
- Maintained by Kody.
- Built-in authentication.
- Built-in retries.
- Idiomatic for each language.
- Efficient protocol buffer HTTP request body.

If your coding language is not listed, please let the Kody team know and we will be able to create it for you.

## Authenticate to Payments API

The client library uses a combination of a `Store ID` and an `API key`. These will be shared with you during the technical integration onbiarding or by your Kody contact.
During develoment you will have access to a test Store and test API key, and when the integration is ready for live access, those production credentials will be shared securely.
Test and live API calls are always compatible, only changing credentials and the service hostname is required.

### Host names

- Development and test: `https://grpc-staging.kodypay.com`
- Live: `https://grpc.kodypay.com`

## Payments API Documentation

Kody supports the following channels to accept payments via API.

1. Terminal - In-person payments
2. Online - E-commerce payments

Each of these channels have their own collection of services that are available as method calls on the client library:
- `KodyPayTerminalService`
- `KodyEcomPaymentsService`

### Terminal

The Kody Payments API Terminal service has the following methods:

- `KodyPayTerminalService.Terminals` - returns all the terminals of the store and their online status
- `KodyPayTerminalService.Pay` - initiate a terminal payment
- `KodyPayTerminalService.Cancel` - cancel an active terminal payment
- `KodyPayTerminalService.PaymentDetails` - get the payment details

### Online

The Kody Payments API Online service has the following methods:

- `KodyPayTerminalService.Terminals` - returns all the terminals of the store and their online status
- `KodyPayTerminalService.Pay` - initiate a terminal payment
- `KodyPayTerminalService.Cancel` - cancel an active terminal payment
- `KodyPayTerminalService.PaymentDetails` - get the payment details


## Demo code

### **Get list of Terminals**

This simple call is a fast, read only method, that returns a list of all terminals assigned to the store, and their online status.

````python
 with grpc.secure_channel(target=config.address,
                             credentials=grpc.ssl_channel_credentials()) as channel:
        stub = pay_grpc_client.KodyPayTerminalServiceStub(channel)
        response = stub.Terminals(
            pay_model.TerminalsRequest(store_id=config.store_id),
            metadata=[("x-api-key", config.api_key)]
        )
````
- TerminalResponse : Terminal Response

```python
message TerminalsResponse {
  repeated Terminal terminals = 1;
}

message Terminal {
  string terminal_id = 1; // terminal serial number
  bool online = 2;
}
```

### **Create terminal payment**

Send to a terminal a payment initiation request. This request can make the terminal to immediately display a card acquiring screen, or display a tip screen to the user which after will go to the card scanning screen.

````python
# without tips screen
with grpc.secure_channel(target=config.address, credentials=grpc.ssl_channel_credentials()) as channel:
        stub = pay_grpc_client.KodyPayTerminalServiceStub(channel)
        response_iterator = stub.Pay(
            pay_model.PayRequest(store_id=config.store_id, terminal_id=config.terminal_id, amount=amount),
            metadata=[("x-api-key", config.api_key)]
        )

# with tips screen
with grpc.secure_channel(target=config.address, credentials=grpc.ssl_channel_credentials()) as channel:
        stub = pay_grpc_client.KodyPayTerminalServiceStub(channel)
        response_iterator = stub.Pay(
            pay_model.PayRequest(store_id=config.store_id, terminal_id=config.terminal_id, amount=amount,  show_tips=bool(True)),
            metadata=[("x-api-key", config.api_key)]
        )
````

- PayResponse : Payment Response

````python
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

### **Get Terminal Payment Details**

````python
with grpc.secure_channel(target=config.address, credentials=grpc.ssl_channel_credentials()) as channel:
        stub = pay_grpc_client.KodyPayTerminalServiceStub(channel)
        response = stub.PaymentDetails(
            pay_model.PaymentDetailsRequest(store_id=config.store_id, order_id=config.order_id),
            metadata=[("x-api-key", config.api_key)]
        )
````
- PayResponse : Get Payment Detail Response

### **Cancel Terminal Payment**

````python
with grpc.secure_channel(target=config.address, credentials=grpc.ssl_channel_credentials()) as channel:
        stub = pay_grpc_client.KodyPayTerminalServiceStub(channel)
        response = stub.Cancel(
            pay_model.CancelRequest(store_id=config.store_id, terminal_id=config.terminal_id, amount=amount,  order_id=config.order_id),
            metadata=[("x-api-key", config.api_key)]
        )
````
- CancelResponse : Cancel Payment Response

````python
message CancelResponse {
  PaymentStatus status = 1;
}
````

### **Create online payment**

````python
 with grpc.secure_channel(target=config.address,
                             credentials=grpc.ssl_channel_credentials()) as channel:
        stub = ecom_grpc_client.KodyEcomPaymentsServiceStub(channel)
        response = stub.InitiatePayment(ecom_model.PaymentInitiationRequest(store_id=config.store_id,
                                                                            payment_reference=payment_reference,
                                                                            amount=amount,
                                                                            currency=currency,
                                                                            order_id=order_id,
                                                                            return_url=return_url,
                                                                            expiry=expiry),
                                        metadata=[("x-api-key", config.api_key)])
````
- PaymentInitiationResponse - Online Payment Response
````python
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
````
## More sample code

- Java : https://github.com/KodyPay/kody-clientsdk-java/tree/main/samples/src/main/java/terminal
- Python: https://github.com/KodyPay/kody-clientsdk-python/tree/main/versions/3_12/samples/terminal
- PHP: https://github.com/KodyPay/kody-clientsdk-php/tree/main/samples/php8/pos
- .Net: https://github.com/KodyPay/kody-clientsdk-dotnet/tree/main/samples/ListTerminals,https://github.com/KodyPay/kody-clientsdk-dotnet/tree/main/samples/TerminalPayment 

# Kody Payments API

This guide provides an overview of using the Kody Payments API and its reference documentation.

- [Client Libraries](#client-libraries)
- [Python Installation](#python-installation)
- [Authenticate to Payments API](#authenticate-to-payments-api)
- [Payments API Reference](#payments-api-reference)
- [API data reference and Demo code](#api-data-reference-and-demo-code)
- [More sample code](#more-sample-code)

## Client Libraries

Kody provides client libraries for many popular languages to access the APIs. If your desired programming language is supported by the client libraries, we recommend that you use this option.

Available languages:
- Python: https://github.com/KodyPay/kody-clientsdk-python/
- Java : https://github.com/KodyPay/kody-clientsdk-java/
- PHP: https://github.com/KodyPay/kody-clientsdk-php/
- .Net: https://github.com/KodyPay/kody-clientsdk-dotnet/

The advantages of using the Kody Client library instead of a REST API are:
- Maintained by Kody.
- Built-in authentication and increased security.
- Built-in retries.
- Idiomatic for each language.
- Efficient protocol buffer HTTP request body.
- Quicker development.
- Backwards compatibility with new versions.

If your coding language is not listed, please let the Kody team know and we will be able to create it for you.

## Python Installation
### Requirements
Add to your `requirements.txt` the following:
````
grpcio-tools
````
And in your `setup.py` the following:
````python
    install_requires=[
        'grpcio==1.66.1',
        'protobuf==5.27.2'
    ],
````
### PIP

Install the Kody Python Client SDK using the following command:

```bash 
pip install kody-clientsdk-python
```
### Import in code
You can import the Kody Client Library in your Python code with the following:
````python
import kody_clientsdk_python.pay.v1.pay_pb2 as kody_model
import kody_clientsdk_python.pay.v1.pay_pb2_grpc as kody_client
````

## Authenticate to Payments API

The client library uses a combination of a `Store ID` and an `API key`. 
These will be shared with you during the technical integration onboarding or by your Kody contact.

During development, you will have access to a **test Store** and **test API key**, and when the integration is ready for live access, the production credentials will be shared securely with you and associated with a live store that was onboarded on Kody.

The test and live API calls are always compatible, only changing credentials and the service hostname is required to enable the integration in production.

### Host names

- Development and test: `https://grpc-staging.kodypay.com`
- Live: `https://grpc.kodypay.com`

### API Authentication

Every client library request authenticates with the server using a `store id` and metadata field `x-api-key`.

Example: 
````python
# Create request and set metadata
get_terminals_request = kody_model.TerminalsRequest(store_id="STORE ID")
metadata = [("x-api-key", "API KEY")]

# Setup gRPC channel and client stub
channel = grpc.secure_channel("HOSTNAME", grpc.ssl_channel_credentials())
kody_service = kody_client.KodyPayTerminalServiceStub(channel)

# Make the client call with request and metadata
get_terminals_response = kody_service.Terminals(get_terminals_request, metadata=metadata)
````
Replace the `STORE ID`, `API KEY` and `HOSTNAME` with the details provided by the Kody team.
Note: it is recommended that you store the `API KEY` in a secured storage, and insert it into your code via an environment variable. Read more [How to Handle Secrets in Python](https://blog.gitguardian.com/how-to-handle-secrets-in-python/). 

## Payments API Reference

Kody supports the following channels to accept payments via API.

1. [**Terminal**](#terminal---in-person-payments) - In-person payments
2. [**Online**](#online---e-commerce-payments) - E-commerce payments

Each of these channels have their own collection of services that are available as method calls on the client library:
- `KodyPayTerminalService`
- `KodyEcomPaymentsService`

### Terminal - In-person payments

The Kody Payments API Terminal service has the following methods:

- [Get List of Terminals](#Get-list-of-Terminals): `KodyPayTerminalService.Terminals` - returns all the terminals of the store and their online status
- [Create Terminal Payment](#create-terminal-payment):`KodyPayTerminalService.Pay` - initiate a terminal payment
- Cancel terminal payment: `KodyPayTerminalService.Cancel` - cancel an active terminal payment
- [Get Payment Details](#get-terminal-payment-details) `KodyPayTerminalService.PaymentDetails` - get the payment details

Follow the links of these methods to see the sample code and the data specification.

### Online - E-commerce payments

The Kody Payments API Online service has the following methods:

- `KodyEcomPaymentsService.InitiatePayment` - returns a URL to display an online payment page to the shopper
- `KodyEcomPaymentsService.PaymentDetails` - get the payment details
- `KodyEcomPaymentsService.GetCardToken` - get card token
- `KodyEcomPaymentsService.GetPayments` - get list of all store payments, with a filter and paginated


## API data reference and Demo code

Every request to the client library requires authentication and the identifier of the store. See more [authentication](#authenticate-to-payments-api).

### Get list of Terminals

This is a simple and read only method, that returns a list of all terminals assigned to the store, and their online status.
You can use this request frequently and it is a good way to check if your API code is configured properly for authentication.

- TerminalRequest : Terminal Request
```python
@dataclass
class TerminalRequest:
    store_id: str  # The store id
```

- TerminalResponse : Terminal Response
```python
@dataclass
class Terminal:
    terminal_id: str  # Terminal serial number
    online: bool  # Online status

@dataclass
class TerminalsResponse:
    terminals: List[Terminal]  # List of Terminal objects
```

#### Python Demo
````python
import kody_clientsdk_python.pay.v1.pay_pb2 as kody_model
import kody_clientsdk_python.pay.v1.pay_pb2_grpc as kody_client

channel = grpc.secure_channel("HOSTNAME", grpc.ssl_channel_credentials())
kody_service = kody_client.KodyPayTerminalServiceStub(channel)
metadata = [("x-api-key", "API KEY")]

# Make the client call with request and metadata
get_terminals_request = kody_model.TerminalsRequest(store_id="STORE ID")
get_terminals_response = kody_service.Terminals(get_terminals_request, metadata=metadata)
````

### Create terminal payment

Send a payment initiation request to a terminal. 
This request will either make the terminal immediately display the card acquiring screen, or display a tip screen to the user after which it will go to the card acquiring screen.

A test terminal might have multiple apps on the OS screen. Launch the terminal app called `[S] Payments`.

The terminal must be in the mode: `Wait for Orders` which can be launched from the terminal app menu.
A store that has the feature `Wait for Orders` enabled will always launch the `Wait for Orders` screen automatically. 
This screen can be closed (by tapping the `X` icon) to access other terminal features, but payments from API will not work until the `Wait for Orders` screen is started. 

#### PayRequest - Payment Request 
```python
@dataclass
class PayRequest:
    store_id: str
    terminal_id: str
    amount: float
    show_tips: bool
```

Request parameters:
- `store_id` - the ID of your assigned store
- `terminal_id` - the serial number of the terminal that will process the payment request. This number is returned by the [list of terminals request](#get-list-of-terminals), or can be found on the back label of the hardware.
- `amount` - amount as a 2.dp decimal number, such as `"1.00"`
- `show_tips` - (optional) whether to show (true) or hide (false) the tip options. Default is (false)


#### PayResponse : Payment Response

````python
class PaymentStatus(Enum):
    PENDING = 1
    SUCCESS = 2
    FAILED = 3
    CANCELLED = 4

@dataclass
class PayResponse:
    status: PaymentStatus
    order_id: str  # Unique order ID generated by Kody
    failure_reason: Optional[str] = None  # Optional, only populated on failure
    receipt_json: Optional[str] = None  # Optional, json blob for receipt data
    date_created: datetime  # Timestamp when the response was created
    ext_payment_ref: Optional[str] = None  # Optional external payment reference
    date_paid: Optional[datetime] = None  # Optional timestamp for date paid
    total_amount: Optional[str] = None  # Optional total amount
    sale_amount: Optional[str] = None  # Optional sale amount
    tips_amount: Optional[str] = None  # Optional tips amount
````

#### Python Demo 
````python
import kody_clientsdk_python.pay.v1.pay_pb2 as kody_model
import kody_clientsdk_python.pay.v1.pay_pb2_grpc as kody_client

channel = grpc.secure_channel("HOSTNAME", grpc.ssl_channel_credentials())
kody_service = kody_client.KodyPayTerminalServiceStub(channel)
metadata = [("x-api-key", "API KEY")]

# Make the client call with request and metadata
payment_request = kody_model.PayRequest(store_id="STORE ID", 
                                        terminal_id="TERMINAL ID", 
                                        amount="65.50",
                                        show_tips=bool(False))
payment_response = kody_service.Pay(payment_request, metadata=metadata])
````

### Get Terminal Payment Details

The payment details request requires the following parameters:
- `store_id` - the ID of your assigned store
- `order_id` - the Order ID returned in the initial payment response, a unique UUID value for each payment.

````python
payment_details_response = kody_client.PaymentDetails(
    kody_model.PaymentDetailsRequest(store_id="STORE ID", 
                                     order_id="ORDER ID"),
    metadata=metadata
)
````
- PayResponse : [Get Payment Detail Response](#payresponse--payment-response)

### Cancel Terminal Payment

#### CancelRequest
The cancel payment request requires the following parameters:

- `store_id` - the ID of your assigned store
- `terminal_id` - the serial number of the terminal that is processing the payment request
- `amount` - the amount sent in the original payment request, used to find the payment request
- `order_id` - the Order ID returned in the initial payment response, a unique UUID value for each payment


````python
response = kody_client.Cancel(
    kody_model.CancelRequest(store_id="STORE ID",
                            terminal_id="TERMINAL ID",
                            amount="65.50", 
                            order_id="ORDER ID"),
    metadata=metadata
)
````

#### CancelResponse : Cancel Payment Response

````python
class PaymentStatus(Enum):
   PENDING = 1
   SUCCESS = 2
   FAILED = 3
   CANCELLED = 4

@dataclass
class CancelResponse:
    status: PaymentStatus
````

### Online Payments
#### PaymentInitiationRequest - Online payment request
The online payment request requires the following parameters:
- `store_id` - the ID of your assigned store
- `payment_reference` - a unique reference for the payment, sent from the client and returned by the server
- `amount` - the amount to request for the online payment, formatted as a 2.dp decimal number, such as `1.00`
- `currency` - the currency for this payment in 3 character ISO format, such as `GBP`
- `order_id` - a unique order ID for this payment, sent from the client and returned by the server
- `return_url` - where the payment form will redirect to after the payment has completed, the return url will have additional query parameters appended to indicate the status of the payment request.
- `expiry` - how long the payment form will wait until the payment expires and the page will redirect to the return url

````python
response = kody_client.InitiatePayment(
    kody_model.PaymentInitiationRequest(store_id="STORE ID",
                                        payment_reference=payment_reference,
                                        amount=amount,
                                        currency=currency,
                                        order_id=order_id,
                                        return_url=return_url,
                                        expiry=expiry),
    metadata=metadata)
````

#### PaymentInitiationResponse - Online payment response
````python
@dataclass
class PaymentInitiationResponse:
    response: Optional[Response] = None
    error: Optional[Error] = None

@dataclass
class Response:
    payment_id: str  # The unique identifier created by Kody
    payment_url: str  # The URL to send to the user from your application

class ErrorType(Enum):
    UNKNOWN = 0
    DUPLICATE_ATTEMPT = 1
    INVALID_REQUEST = 2

@dataclass
class Error:
    type: ErrorType  # Enum for the error type
    message: str  # Error message
````

## More sample code

- Java : https://github.com/KodyPay/kody-clientsdk-java/tree/main/samples/src/main/java/terminal
- Python: https://github.com/KodyPay/kody-clientsdk-python/tree/main/versions/3_12/samples/terminal
- PHP: https://github.com/KodyPay/kody-clientsdk-php/tree/main/samples/php8/pos
- .Net: https://github.com/KodyPay/kody-clientsdk-dotnet/tree/main/samples/ListTerminals,https://github.com/KodyPay/kody-clientsdk-dotnet/tree/main/samples/TerminalPayment 

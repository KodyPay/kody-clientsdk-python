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

The client library uses a combination of a `Store ID` and an `API key`. These will be shared with you during the technical integration onboarding or by your Kody contact.
During development, you will have access to a test Store and test API key, and when the integration is ready for live access, those production credentials will be shared securely.
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

- `KodyPayTerminalService.InitiatePayment` - initiate an online payment
- `KodyPayTerminalService.PaymentDetails` - get the payment details
- `KodyPayTerminalService.GetPayments` - get list of payments
- `KodyPayTerminalService.GetCardToken` - get card token


## Demo code

### **Get list of Terminals**

This simple call is a fast, read only method, that returns a list of all terminals assigned to the store, and their online status.

The terminals request requires the following parameters:
- `store_id` - the ID of your assigned store

The request authenticates with the server using the `x-api-key` metadata field, you must use your assigned API key.
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
from dataclasses import dataclass
from typing import List

@dataclass
class Terminal:
    terminal_id: str  # Terminal serial number
    online: bool  # Online status

@dataclass
class TerminalsResponse:
    terminals: List[Terminal]  # List of Terminal objects
```

### **Create terminal payment**

Send a payment initiation request to a terminal. This request will either make the terminal immediately display the card acquiring screen, or display a tip screen to the user after which it will go to the card acquiring screen.

The pay request requires the following parameters:
- `store_id` - the ID of your assigned store
- `terminal_id` - the serial number of the terminal that will process the payment request
- `amount` - amount as a 2.dp decimal number, such as 1.00
  The following parameters are optional:
- `show_tips` - whether to show (true) or hide (false) the tip options, default is to hide the tip options (false)

The request authenticates with the server using the `x-api-key` metadata field, you must use your assigned API key.
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
from dataclasses import dataclass
from typing import Optional
from enum import Enum
from datetime import datetime

class PaymentStatus(Enum):
    PENDING = 1
    SUCCESS = 2
    FAILED = 3
    CANCELLED = 4

@dataclass
class PayResponse:
    status: PaymentStatus  # Payment status (enum)
    failure_reason: Optional[str] = None  # Optional, only populated on failure
    receipt_json: Optional[str] = None  # Optional, json blob for receipt data
    order_id: str  # Mandatory field for order ID
    date_created: datetime  # Timestamp when the response was created
    ext_payment_ref: Optional[str] = None  # Optional external payment reference
    date_paid: Optional[datetime] = None  # Optional timestamp for date paid
    total_amount: Optional[str] = None  # Optional total amount
    sale_amount: Optional[str] = None  # Optional sale amount
    tips_amount: Optional[str] = None  # Optional tips amount
````

### **Get Terminal Payment Details**

The payment details request requires the following parameters:
- `store_id` - the ID of your assigned store
- `order_id` - the Order ID returned in the initial payment response, a unique UUID value for each payment.

The request authenticates with the server using the `x-api-key` metadata field, you must use your assigned API key.
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

The cancel payment request requires the following parameters:

- `store_id` - the ID of your assigned store
- `terminal_id` - the serial number of the terminal that is processing the payment request
- `amount` - the amount sent in the original payment request, used to find the payment request
- `order_id` - the Order ID returned in the initial payment response, a unique UUID value for each payment

The request authenticates with the server using the `x-api-key` metadata field, you must use your assigned API key.

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
from dataclasses import dataclass
from enum import Enum

class PaymentStatus(Enum):
   PENDING = 1
   SUCCESS = 2
   FAILED = 3
   CANCELLED = 4

@dataclass
class CancelResponse:
    status: PaymentStatus  # PaymentStatus enum for the cancel operation status
````

### **Create online payment**

The online payment request requires the following parameters:

- `store_id` - the ID of your assigned store
- `payment_reference` - a unique reference for the payment, sent from the client and returned by the server
- `amount` - the amount to request for the online payment, formatted as a 2.dp decimal number, such as `1.00`
- `currency` - the currency for this payment in 3 character ISO format, such as `GBP`
- `order_id` - a unique order ID for this payment, sent from the client and returned by the server
- `return_url` - where the payment form will redirect to after the payment has completed, the return url will have additional query parameters appended to indicate the status of the payment request.
- `expiry` - how long the payment form will wait until the payment expires and the page will redirect to the return url

The request authenticates with the server using the `x-api-key` metadata field, you must use your assigned API key.

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
from dataclasses import dataclass
from typing import Optional

@dataclass
class PaymentInitiationResponse:
    response: Optional[str] = None
    error: Optional[str] = None
````
```python
from dataclasses import dataclass

@dataclass
class Response:
    payment_id: str  # The unique identifier created by Kody
    payment_url: str  # The URL to send the user to from your application

```
```python
from dataclasses import dataclass
from enum import Enum

class ErrorType(Enum):
    UNKNOWN = 0
    DUPLICATE_ATTEMPT = 1
    INVALID_REQUEST = 2

@dataclass
class Error:
    type: ErrorType  # Enum for the error type
    message: str  # Error message
```
## More sample code

- Java : https://github.com/KodyPay/kody-clientsdk-java/tree/main/samples/src/main/java/terminal
- Python: https://github.com/KodyPay/kody-clientsdk-python/tree/main/versions/3_12/samples/terminal
- PHP: https://github.com/KodyPay/kody-clientsdk-php/tree/main/samples/php8/pos
- .Net: https://github.com/KodyPay/kody-clientsdk-dotnet/tree/main/samples/ListTerminals,https://github.com/KodyPay/kody-clientsdk-dotnet/tree/main/samples/TerminalPayment 

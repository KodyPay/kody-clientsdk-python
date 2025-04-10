
# Kody API – Python SDK

This guide provides an overview of using the Kody Python gRPC Client SDK and its reference documentation.

- [Client Libraries](#client-libraries)
- [Python Installation](#python-installation)
- [Authentication](#authentication)
- [Documentation](#documentation)
- [Sample Code](#sample-code)

## Client Libraries

Kody provides client libraries for many popular languages to access the APIs. If your desired programming language is supported by the client libraries, we recommend that you use this option.

Available languages:
- Python: https://github.com/KodyPay/kody-clientsdk-python/
- Java: https://github.com/KodyPay/kody-clientsdk-java/
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

- Python 3.7 or later
- pip / virtualenv (optional)
- gRPC and Protobuf libraries

### Step 1: Install dependencies

Add to your `requirements.txt`:

```text
grpcio-tools
```

And in your `setup.py`:

```python
install_requires=[
    'grpcio==1.66.1',
    'protobuf==5.27.2'
],
```

### Step 2: Install via pip

Install the Kody Python SDK from PyPI:

```bash
pip install kody-clientsdk-python
```

### Step 3: Import in Code

```python
import kody_clientsdk_python.pay.v1.pay_pb2 as kody_model
import kody_clientsdk_python.pay.v1.pay_pb2_grpc as kody_client
```

## Authentication

The client library uses a combination of a `Store ID` and an `API key`.

These credentials will be shared with you during the technical integration onboarding process. During development, you’ll be given a **test Store ID** and **test API key**. For production, you’ll receive live credentials securely linked to your onboarded store.

### Host names

- Development and test: `https://grpc-staging.kodypay.com`
- Live: `https://grpc.kodypay.com`

### API Authentication

All client requests authenticate using gRPC metadata with the `x-api-key`.

```python
# Create request and set metadata
get_terminals_request = kody_model.TerminalsRequest(store_id="STORE ID")
metadata = [("x-api-key", "API KEY")]

# Setup gRPC channel and client stub
channel = grpc.secure_channel("HOSTNAME", grpc.ssl_channel_credentials())
kody_service = kody_client.KodyPayTerminalServiceStub(channel)

# Make the call
get_terminals_response = kody_service.Terminals(get_terminals_request, metadata=metadata)
```

> 🔒 Store your `API KEY` securely using environment variables. [How to Handle Secrets in Python](https://blog.gitguardian.com/how-to-handle-secrets-in-python/)

## Documentation

For full API documentation, protocol definitions, and integration guides, please visit:
📚 https://api-docs.kody.com

## Sample Code

- Python: https://github.com/KodyPay/kody-clientsdk-python/tree/main/versions/3_12/samples
- Java: https://github.com/KodyPay/kody-clientsdk-java/tree/main/samples
- PHP: https://github.com/KodyPay/kody-clientsdk-php/tree/main/samples
- .Net: https://github.com/KodyPay/kody-clientsdk-dotnet/tree/main/samples

## License

This project is licensed under the MIT License.

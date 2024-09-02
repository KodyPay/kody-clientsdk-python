# Kody Python gRPC client

## Description
The Kody gRPC Client is an SDK generated from protobuf protocols to facilitate communication with the Kody Payments Gateway. This library provides a simple and efficient way to integrate Kody payment functionalities into your applications.

## Installation
Add to your `requirements.txt` any package from the release list
`https://github.com/KodyPay/kody-clientsdk-python-3.6/releases/download/v<version>/kody_clientsdk_python-<version>.tar.gz`

### Configuration

Update the `config.ini` file with your `apiKey`, `storeId` and `terminalId`.

```ini
[default]
address=grpc-staging.kodypay.com:443
apiKey=Put your API key here
storeId=Use your Kody store ID
terminalId=Use your terminal ID
```

## Running the Examples
Below are the available examples you can find in the `samples` subproject:
- Online payments
    - `ecom_query_blocking.py`
    - `ecom_query_async.py`
- Terminal payments
    - `terminal_query_blocking.py`
    - `terminal_query_async.py`
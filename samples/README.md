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

```bash
python3 samples/terminal/terminal_query_blocking.py
```

## Troubleshooting

If you encounter issues, ensure:

- PYTHONPATH is correctly exported (e.g. `export PYTHONPATH="${PYTHONPATH}:/kody-clientsdk-puthon-3.6"`)
- Your `config.ini` is correctly filled out.
- Contact Kody support or tech team
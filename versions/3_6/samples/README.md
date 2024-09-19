### Environment

You can use your native python environment (Python 3.6) or use [pyenv](https://github.com/pyenv/pyenv) to create a virtual environment for python 3.6.

### Configuration

Export the following environment variables:

```bash
export KODY_API_KEY=<Put your API key here>
export KODY_STORE_ID=<Use your Kody store ID>
export KODY_TERMINAL_ID=<Use your terminal ID>
export KODY_ADDRESS=grpc-staging.kodypay.com:443
export SHOW_TIPS=<Use True or False>
```

Make sure you add into yor pythonpath the path to the samples directory:

```bash
export PYTHONPATH="${PYTHONPATH}:/path_to_samples"
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

- PYTHONPATH is correctly exported (e.g. `export PYTHONPATH="${PYTHONPATH}:/path_to_samples"`).
- Your `config.ini` is correctly filled out.
- Contact Kody support or tech team.
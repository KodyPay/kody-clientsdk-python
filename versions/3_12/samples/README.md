### Environment

You can use your native python environment (Python 3.12) or use [pyenv](https://github.com/pyenv/pyenv) to create a virtual environment for python 3.12.

### Configuration

The necessary configuration can be set directly within the Python scripts. For example, in the `process_payment.py` file, specify the following variables:

- **address**: The gRPC server address (e.g., `grpc-staging.kodypay.com`).
- **store_id**: Your Kody store ID.
- **terminal_id**: Your terminal ID.
- **api_key**: Your API key.
- **amount**: The transaction amount.

## Running the Examples
Below are the available examples you can find in the `samples` subproject:
- Online payments
    - `process_payment.py`
    - `get_payment_details.py`
    - `refund_payment.py`
- Terminal payments
    - `list_terminals.py`
    - `process_payment.py`
    - `refund_payment.py`
    - `get_payment_details.py`

```bash
python3 -m samples.terminal.list_terminals
```

## Troubleshooting

If you encounter issues, ensure:

- The required variables are correctly set in the Python scripts.
- Contact Kody support or tech team.
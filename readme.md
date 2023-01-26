
# Monero Payment Service

This project is a FastAPI service that allows customers to make payments using Monero.

## Prerequisites

-   Python 3.7 or higher
-   FastAPI
-   Requests
-   Monero RPC connection parameters (username, password, host, and port)

## Installation

1.  Clone the repository:

`git clone https://github.com/<username>/monero-payment-service.git` 

2.  Install the required Python packages:

`pip install fastapi requests` 

3.  Set up the Monero RPC connection parameters:

Open `app.py` and set the `rpc_user`, `rpc_password`, `rpc_host`, and `rpc_port` variables to the appropriate values for your Monero RPC connection.

4.  Run the service:

`python app.py` 

## Usage

The service has the following API endpoints:

-   `/payment`: Generates a Monero wallet address and payment amount for the customer's order and renders it in a HTML template.
-   `/check_payment/{wallet_address}`: Queries the Monero blockchain for information about the wallet address and returns the payment amount received and confirmation status as a JSON object.

## Examples

To make a payment, access the `/payment` endpoint in a web browser:

`http://localhost:8000/payment` 

This will display the Monero wallet address and payment amount for the customer's order.

To check the payment status, use the `/check_payment/{wallet_address}` endpoint and specify the wallet address as a URL parameter:

`http://localhost:8000/check_payment/<wallet_address>` 

This will return a JSON object with the payment amount received and confirmation status:

`{
    "received": 1000000,
    "confirmed": true
}`
## Troubleshooting

If you encounter any problems while using the project, here are some possible solutions:

-   Make sure you have installed all of the required Python packages and have set up the Monero RPC connection parameters correctly.
-   Check the logs for any error messages that may help identify the problem.
-   If you are having trouble connecting to the Monero RPC server, make sure that the server is running and that the connection parameters are correct.
-   If you are having trouble with the API endpoints, make sure that you are using the correct URL and parameters.

## Contributions

We welcome contributions to the Monero Payment Service! If you would like to contribute, please follow these guidelines:

-   Fork the repository and create a new branch for your changes.
-   Make your changes in the new branch, and test them thoroughly.
-   Submit a pull request with a clear explanation of your changes and any relevant information.
-   If you are reporting a bug, please include as much detail as possible, including the steps to reproduce the bug and any relevant error messages.

Thank you for your interest in contributing to the Monero Payment Service!

from fastapi import FastAPI
import requests
import uvicorn
from requests import Response, request
from starlette.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)


@app.post("/make_transaction")
def make_transaction(to_address: str, amount: int):
    # Set up RPC connection parameters
    rpc_user = "monero_rpc_user"
    rpc_password = "monero_rpc_password"
    rpc_host = "localhost"
    rpc_port = "18081"

    # Build RPC request
    url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}/json_rpc"
    headers = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "transfer",
        "params": {
            "destinations": [{"amount": amount, "address": to_address}],
            "priority": 0,
            "unlock_time": 0,
        },
    }

    # Make RPC request
    response = requests.post(url, json=data, headers=headers)

    # Return response
    return response.json()


@app.get("/check_transaction_confirmation/{txid}")
def check_transaction_confirmation(txid: str):
    import requests

    # Set up RPC connection parameters
    rpc_user = "monero_rpc_user"
    rpc_password = "monero_rpc_password"
    rpc_host = "localhost"
    rpc_port = "18081"

    # Build RPC request
    url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}/json_rpc"
    headers = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "get_transactions",
        "params": {"txs_hashes": [txid]},
    }

    # Make RPC request
    response = requests.post(url, json=data, headers=headers)

    # Get transaction information
    tx_info = response.json()["result"]["transactions"][0]

    # Check if transaction is confirmed
    if tx_info["in_pool"] is False and tx_info["block_height"] is not None:
        return {"confirmed": True}
    else:
        return {"confirmed": False}


@app.get("/payment")
def payment(response: Response):
    # Set up RPC connection parameters
    rpc_user = "monero_rpc_user"
    rpc_password = "monero_rpc_password"
    rpc_host = "localhost"
    rpc_port = "18081"

    # Build RPC request to generate new address
    url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}/json_rpc"
    headers = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "create_address",
        "params": {},
    }

    # Make RPC request
    response = requests.post(url, json=data, headers=headers)

    # Get new address
    new_address = response.json()["result"]["address"]

    # Set payment amount
    payment_amount = 1000000  # 1 Monero

    # Render HTML template
    return templates.TemplateResponse(
        "payment.html",
        {
            "request": request,
            "wallet_address": new_address,
            "payment_amount": payment_amount,
        },
    )


@app.get("/check_payment/{wallet_address}")
def check_payment(wallet_address: str):
    # Check payment for the given wallet address
    import requests

    # Set up RPC connection parameters
    rpc_user = "monero_rpc_user"
    rpc_password = "monero_rpc_password"
    rpc_host = "localhost"
    rpc_port = "18081"

    # Build RPC request to get balance of wallet address
    url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}/json_rpc"
    headers = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "get_balance",
        "params": {"account_index": 0, "address": wallet_address},
    }

    # Make RPC request
    response = requests.post(url, json=data, headers=headers)

    # Get balance
    balance = response.json()["result"]["balance"]

    # Build RPC request to get transaction history of wallet address
    data = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "get_transfers",
        "params": {"in": True, "account_index": 0, "address": wallet_address},
    }

    # Make RPC request
    response = requests.post(url, json=data, headers=headers)

    # Get transaction history
    tx_history = response.json()["result"]["in"]

    # Check if any transactions have been received
    received = 0
    confirmed = False
    if len(tx_history) > 0:
        # Transactions have been received
        received = sum([tx["amount"] for tx in tx_history])
        confirmed = all([tx["confirmations"] > 0 for tx in tx_history])

    return {"received": received, "confirmed": confirmed}


@app.get("/")
def index():
    # Render HTML template
    return templates.TemplateResponse(
        "payment.html",
        {
            "request": request,
        },
    )

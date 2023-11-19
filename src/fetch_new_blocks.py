from dotenv import load_dotenv
import os
from web3 import Web3

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key
alchemy_api_key = os.getenv('ALCHEMY_API_KEY')
if not alchemy_api_key:
    raise ValueError("Alchemy API key not found in .env file.")

alchemy_url = f"https://base-mainnet.g.alchemy.com/v2/{alchemy_api_key}"

# Connect to Base using Alchemy
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Ensure connection is established
if not w3.is_connected():
    raise ConnectionError("Failed to connect to Base blockchain.")

# Fetch the latest block
latest_block = w3.eth.get_block('latest', full_transactions=True)
print("Latest Block Details:")
print(latest_block)

# Iterate through transactions in the latest block
for tx in latest_block['transactions']:
    # Check for contract creation (to address is None)
    if tx['to'] is None:
        print(f"Contract Creation Transaction Found: {tx['hash'].hex()}")
        # Additional logic to analyze the contract can be added here


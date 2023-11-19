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

# Function to process a block
def process_block(block_number):
    block = w3.eth.get_block(block_number, full_transactions=True)
    print(f"Processing Block: {block['number']}")
    for tx in block['transactions']:
        # Check for contract creation (to address is None)
        if tx['to'] is None:
            print(f"Potential NFT Contract Creation: {tx['hash'].hex()}")
            # Here, you can add logic to store this transaction in your database

# Fetch and process the latest block
latest_block_number = w3.eth.block_number
process_block(latest_block_number)


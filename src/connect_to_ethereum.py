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

# Check if the connection is successful
if w3.is_connected():  # Updated this line
    print("Connected to Base blockchain!")
else:
    print("Failed to connect to Base blockchain.")

# Example: Fetch the latest block number
latest_block = w3.eth.block_number
print(f"Latest block number: {latest_block}")


from dotenv import load_dotenv
import os
import psycopg2
from web3 import Web3
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Database and Alchemy connection details
db_connection_string = os.getenv('DATABASE_URL')
alchemy_api_key = os.getenv('ALCHEMY_API_KEY')

# Connect to the database
conn = psycopg2.connect(db_connection_string)
cur = conn.cursor()

# Test database connection
def test_db_connection():
    try:
        cur.execute("SELECT NOW();")
        db_time = cur.fetchone()
        print(f"Database connection successful. Current database time: {db_time[0]}")
    except Exception as e:
        print(f"Database connection test failed: {e}")

test_db_connection()

# Connect to Base using Alchemy
w3 = Web3(Web3.HTTPProvider(f"https://base-mainnet.g.alchemy.com/v2/{alchemy_api_key}"))

if not w3.is_connected():
    raise ConnectionError("Failed to connect to Base blockchain.")

# Function to process a block and store contract creations
def process_block(block_number):
    block = w3.eth.get_block(block_number, full_transactions=True)
    print(f"Processing Block: {block['number']}")
    for tx in block['transactions']:
        if tx['to'] is None:
            cur.execute(
                "INSERT INTO contract_creations (tx_hash, block_number, timestamp, contract_address) VALUES (%s, %s, %s, %s) ON CONFLICT (tx_hash) DO NOTHING",
                (tx['hash'].hex(), block['number'], datetime.utcfromtimestamp(block['timestamp']), None)
            )
            conn.commit()

# Fetch and process the latest block
latest_block_number = w3.eth.block_number
process_block(latest_block_number)

# Close the database connection
cur.close()
conn.close()


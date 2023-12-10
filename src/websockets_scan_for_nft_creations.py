from web3 import Web3
import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime
import rlp

# Load environment variables from .env file
load_dotenv()

# Database and Alchemy connection details
db_connection_string = os.getenv('DATABASE_URL')
alchemy_api_key = os.getenv('ALCHEMY_API_KEY')

# Establish database connection
def connect_to_db():
    try:
        conn = psycopg2.connect(db_connection_string)
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None, None

# Connect to the database
conn, cur = connect_to_db()
if conn is None:
    exit(1)  # Exit if database connection fails

# Alchemy WebSocket URL
websocket_url = f"wss://base-mainnet.g.alchemy.com/v2/{alchemy_api_key}"

# Connect to Base using Alchemy over WebSocket
try:
    w3 = Web3(Web3.WebsocketProvider(websocket_url))
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to Base blockchain via WebSocket.")
except Exception as e:
    print(f"Error connecting to the blockchain: {e}")
    cur.close()
    conn.close()
    exit(1)

# Factory contract address (lowercased for comparison)
factory_contract_address = "0x0000000000003D61b3d0a96B70b9c9006947759C".lower()

# Function to log contract creation
def log_contract_creation(tx, block, contract_address):
    try:
        cur.execute(
            "INSERT INTO contract_creations (tx_hash, block_number, timestamp, contract_address) VALUES (%s, %s, %s, %s) ON CONFLICT (tx_hash) DO NOTHING",
            (tx.hash.hex(), block.number, datetime.utcfromtimestamp(block.timestamp), contract_address)
        )
        conn.commit()
        print(f"Logged NFT creation: Contract Address {contract_address}")
    except Exception as e:
        print(f"Error executing SQL command: {e}")
        conn.rollback()

# Function to process a block and log contract creations
def process_block(block_hash):
    try:
        block = w3.eth.get_block(block_hash, full_transactions=True)
        print(f"Scanning Block: {block.number}")

        for tx in block.transactions:
            if tx.to is None:  # Potential direct NFT contract creation
                sender_address_bytes = bytes.fromhex(tx['from'][2:])
                nonce_bytes = tx['nonce'].to_bytes(8, byteorder='big')
                hashed = Web3.keccak(rlp.encode([sender_address_bytes, nonce_bytes]))
                contract_address = '0x' + hashed[-20:].hex()
                log_contract_creation(tx, block, contract_address)
            elif tx.to.lower() == factory_contract_address:  # Creation via factory contract
                log_contract_creation(tx, block, tx.to)

    except Exception as e:
        print(f"Error processing block {block_hash.hex()}: {e}")
        conn.rollback()  # Reset the transaction if error occurred in block processing

# Subscribe to new blocks
try:
    new_block_filter = w3.eth.filter('latest')
except Exception as e:
    print(f"Error creating block filter: {e}")
    cur.close()
    conn.close()
    exit(1)

# Main loop
try:
    while True:
        for block_hash in new_block_filter.get_new_entries():
            process_block(block_hash)
except KeyboardInterrupt:
    print("Script interrupted by user.")
finally:
    cur.close()
    conn.close()
    print("Database connection closed.")

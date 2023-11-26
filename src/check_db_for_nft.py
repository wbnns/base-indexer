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

# Function to display potential NFT contracts
def display_nft_contracts():
    cur.execute("SELECT * FROM contract_creations")
    contracts = cur.fetchall()

    if contracts:
        print("Found contract creations:")
        for contract in contracts:
            print(f"Transaction Hash: {contract[0]}, Block Number: {contract[1]}, Timestamp: {contract[2]}, Contract Address: {contract[3]}")
    else:
        print("No contract creations found.")

# Display NFT contracts
display_nft_contracts()

# Close the database connection
cur.close()
conn.close()


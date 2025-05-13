import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8000))
RELOAD = os.getenv('RELOAD', 'True').lower() == 'true'

if __name__ == '__main__':
    print(f"Starting API server on {HOST}:{PORT}")
    uvicorn.run("src.api.app:app", host=HOST, port=PORT, reload=RELOAD)
import uvicorn
import webbrowser
import threading
import sys
import argparse
from .api import app


def start_server():
    uvicorn.run(app, host="localhost", port=8000)


def main():
    parser = argparse.ArgumentParser(
        description="fetch transaction data for a given Solana address and display it as a network graph."
    )

    parser.add_argument("address", help="Solana Address")
    args = parser.parse_args()

    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    webbrowser.open(f"http://localhost:8000/{args.address}")

    server_thread.join()


if __name__ == "__main__":
    main()

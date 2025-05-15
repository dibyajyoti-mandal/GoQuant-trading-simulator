import asyncio
from websocket_client import OrderBookClient

async def main():
    URL = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
    SYMBOL = "BTC-USDT-SWAP"
    client = OrderBookClient(url=URL, symbol=SYMBOL)

    async def run_and_print():
        await client.connect()

    task = asyncio.create_task(run_and_print())

    # Log output every 5 seconds
    while True:
        await asyncio.sleep(5)
        best_bid, best_ask = client.get_top_of_book()
        ask_depth = client.get_cumulative_depth('ask', 100)
        bid_depth = client.get_cumulative_depth('bid', 100)
        print("\n------- Top of Book:")
        print(f"Best Bid: {best_bid}")
        print(f"Best Ask: {best_ask}")
        print("- Depth for $100 Market Buy:")
        for price, qty in ask_depth:
            print(f"  Ask {price} x {qty:.4f}")
        print("- Depth for $100 Market Sell:")
        for price, qty in bid_depth:
            print(f"  Bid {price} x {qty:.4f}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
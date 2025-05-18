import asyncio
from tests.websocket_with_slippage import OrderBookClient

url = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
symbol = "BTC-USDT-SWAP"

client = OrderBookClient(url, symbol)

asyncio.run(client.connect())

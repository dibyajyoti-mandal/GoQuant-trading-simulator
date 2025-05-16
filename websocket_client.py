import asyncio
import websockets
import json
from loguru import logger
import time
from datetime import datetime

class OrderBookClient:
    def __init__(self, url: str, symbol: str):
        self.url = url
        self.symbol = symbol
        self.orderbook = {"asks": [], "bids": [], "timestamp": None}
        self.latencies = []

    async def connect(self):
        logger.info(f"Connecting to {self.url}")
        async with websockets.connect(self.url) as ws:
            await self.listen(ws)

    async def listen(self, ws):
        while True:
            start_time = time.perf_counter()
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=10)
                tick = json.loads(message)
                self.process_tick(tick)
                latency = time.perf_counter() - start_time
                self.latencies.append(latency)
                logger.info(f"Tick @ {tick['timestamp']} processed in {latency:.6f}s")
            except asyncio.TimeoutError:
                logger.warning("WebSocket timeout. Retrying to connect...")

    def process_tick(self, tick):
        self.orderbook['asks'] = sorted(
            [[float(p), float(q)] for p, q in tick['asks']], key=lambda x: x[0]
        )
        self.orderbook['bids'] = sorted(
            [[float(p), float(q)] for p, q in tick['bids']], key=lambda x: -x[0]
        )
        self.orderbook['timestamp'] = tick['timestamp']

    def get_top_of_book(self):
        best_ask = self.orderbook['asks'][0] if self.orderbook['asks'] else None
        best_bid = self.orderbook['bids'][0] if self.orderbook['bids'] else None
        return best_bid, best_ask

    def get_cumulative_depth(self, side='ask', usd_amount=100):
        #Returns (price, quantity) list until cumulative notional >= usd_amount
        book = self.orderbook[side + 's']
        cumulative = 0
        selected_levels = []
        for price, quantity in book:
            notional = price * quantity
            if cumulative >= usd_amount:
                break
            needed = min(quantity, (usd_amount - cumulative) / price)
            selected_levels.append((price, needed))
            cumulative += price * needed
        return selected_levels



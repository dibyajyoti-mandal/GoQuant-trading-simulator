import asyncio
import websockets
import json
from loguru import logger
import time
from datetime import datetime
from models.slippage_model import estimate_slippage
from models.fee_model import estimate_fee

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

                buy_slip = estimate_slippage(self.orderbook, usd_amount=10_000, side='buy')
                sell_slip = estimate_slippage(self.orderbook, usd_amount=10_000, side='sell')

                fee = estimate_fee(usd_amount=10_000, role='taker')

                logger.info(
                    f"Tick @ {tick['timestamp']} | "
                    f"Latency: {latency:.6f}s | "
                    f"Buy Slippage: {buy_slip:.9f}% | "
                    f"Sell Slippage: {sell_slip:.9f}% | "
                    f"Fee: ${fee:.6f}"
                )

            except asyncio.TimeoutError:
                logger.warning("WebSocket timeout. Retrying...")




    def process_tick(self, tick):
        self.orderbook['asks'] = sorted(
            [[float(p), float(q)] for p, q in tick['asks']], key=lambda x: x[0]
        )
        self.orderbook['bids'] = sorted(
            [[float(p), float(q)] for p, q in tick['bids']], key=lambda x: -x[0]
        )
        self.orderbook['timestamp'] = tick['timestamp']

def estimate_slippage(orderbook: dict, usd_amount: float = 10000, side: str = 'buy') -> float:
    """
    Estimates slippage as the % difference between average execution price and mid-price.
    """
    if side not in ['buy', 'sell']:
        raise ValueError("Side must be 'buy' or 'sell'")

    asks = orderbook['asks']
    bids = orderbook['bids']
    
    if not asks or not bids:
        raise ValueError("Orderbook is empty")

    best_bid = bids[0][0]
    best_ask = asks[0][0]
    mid_price = (best_bid + best_ask) / 2

    book_side = asks if side == 'buy' else bids

    total_cost = 0
    total_qty = 0
    remaining_usd = usd_amount

    for price, quantity in book_side:
        notional = price * quantity
        if remaining_usd <= 0:
            break

        if notional >= remaining_usd:
            qty_to_take = remaining_usd / price
            total_cost += qty_to_take * price
            total_qty += qty_to_take
            break
        else:
            total_cost += notional
            total_qty += quantity
            remaining_usd -= notional

    if total_qty == 0:
        return 0.0  # Can't simulate

    avg_execution_price = total_cost / total_qty

    if side == 'buy':
        slippage_pct = (avg_execution_price - mid_price) / mid_price
    else:
        slippage_pct = (mid_price - avg_execution_price) / mid_price

    return round(slippage_pct * 100, 9)



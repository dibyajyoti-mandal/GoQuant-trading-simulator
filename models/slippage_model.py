def estimate_slippage(orderbook: dict, usd_amount: float = 100, side: str = 'buy') -> float:
    """
    Estimates slippage as the % difference between average execution price and mid-price.
    
    Parameters:
        orderbook (dict): Dictionary with 'asks', 'bids', and 'timestamp'.
        usd_amount (float): Notional value to simulate (in USD).
        side (str): 'buy' or 'sell'

    Returns:
        float: Slippage in percentage terms.
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

    # Choose book side depending on trade direction
    book_side = asks if side == 'buy' else bids

    total_cost = 0
    remaining_usd = usd_amount

    for price, quantity in book_side:
        notional = price * quantity
        if remaining_usd <= notional:
            quantity_to_take = remaining_usd / price
            total_cost += quantity_to_take * price
            break
        else:
            total_cost += notional
            remaining_usd -= notional

    avg_execution_price = total_cost / (usd_amount / mid_price)

    # Compute slippage %
    if side == 'buy':
        slippage_pct = (avg_execution_price - mid_price) / mid_price
    else:
        slippage_pct = (mid_price - avg_execution_price) / mid_price

    return slippage_pct * 100  # Convert to %
def estimate_fee(order_value_usd: float, fee_rate: float = 0.001) -> float:
    """
    for every buy/sell on an exchange -> fee for executing the trade
    Estimate trading fee for a market order.
    For tier 1 : consider trading fee of 0.1% (0.001) for market orders.
    """
    return order_value_usd * fee_rate
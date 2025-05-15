def estimate_fee(order_value_usd: float, fee_rate: float = 0.001) -> float:
    """
    Estimate trading fee for a market order.
    
    Args:
        order_value_usd (float): Total notional of the order (e.g., 100 USD).
        fee_rate (float): Taker fee rate (default is 0.10% = 0.001).
    
    Returns:
        float: Fee amount in USD.
    """
    return order_value_usd * fee_rate
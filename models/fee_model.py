def estimate_fee(usd_amount: float, side: str = 'buy', role: str = 'taker') -> float:
    if role == 'taker':
        fee_rate = 0.001  # 0.10%
    elif role == 'maker':
        fee_rate = 0.0008  # 0.08%
    else:
        raise ValueError("Role must be 'maker' or 'taker'")

    return usd_amount * fee_rate

import cvxpy as cp
import numpy as np
import pandas as pd

def optimize_portfolio(returns, big_weight, alt_weight, cash_weight, current_balance, big_tokens=["BTC", "ETH"],
                       cash_tokens=["USDT", "USDC", "BUSD"]):

    n = returns.shape[1]
    mu = returns.mean().values
    Sigma = returns.cov().values

    w = cp.Variable(n)
    gamma = cp.Parameter(nonneg=True)
    ret = mu.T @ w
    risk = cp.quad_form(w, Sigma)
    objective = cp.Maximize(ret - gamma * risk)

    constraints = [w >= 0, cp.sum(w) == 1]

    big_total = cp.sum(w[returns.columns.isin(big_tokens)])
    alt_total = cp.sum(w[~returns.columns.isin(big_tokens + cash_tokens)])
    cash_total = cp.sum(w[returns.columns.isin(cash_tokens)])
    #
    constraints.extend([
        big_total == big_weight / 100,
        alt_total == alt_weight / 100,
        cash_total == cash_weight / 100
    ])

    prob = cp.Problem(objective, constraints)
    gamma.value = 0.5
    prob.solve(solver = cp.ECOS)

    weights = dict(zip(returns.columns, w.value))

    amounts = {}

    for token in weights.keys():
        local_amount = current_balance * weights[token]
        amounts[token] = local_amount

    return weights, amounts


def compute_returns(data, start_day=0, days=7):
    all_returns = {}

    for token, candles in data.items():
        prices = [candle.close_price for candle in candles[start_day:start_day+days*24]]
        returns = [(prices[i] - prices[i-1])/prices[i-1] for i in range(1, len(prices))]
        all_returns[token] = returns

    return pd.DataFrame(all_returns)


def next_day_update(data, current_day_index):
    
    next_day_returns = compute_returns(data, start_day=current_day_index, days=1)
    
    
    current_weights = optimize_portfolio(next_day_returns)
    
    
    next_day_data = {
        token: data[token][current_day_index+1:current_day_index+25] for token in data.keys()
    }

    
    next_day_returns = compute_returns(next_day_data, start_day=0, days=1)
    
    
    next_day_optimized_weights = optimize_portfolio(next_day_returns)
    
    return next_day_optimized_weights


def count_pnl(all_data: dict, cur_day_idx: int, weights: list) -> float:
    pass

def plot_pnl():
    pass

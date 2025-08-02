import json
from binance_client import master_api, create_client

def load_users():
    with open("user_data.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("user_data.json", "w") as f:
        json.dump(users, f)

def copy_latest_trade():
    trades = master_api.get_my_trades(symbol="BTCUSDT")
    if not trades:
        return

    latest = trades[-1]
    is_buy = latest["isBuyer"]
    qty = float(latest["qty"])

    users = load_users()
    for user in users:
        if user.get("daily_trades", 0) >= user.get("max_trades", 999):
            continue
        est_volume = qty * user.get("multiplier", 1.0)
        if user.get("daily_volume", 0.0) + est_volume > user.get("max_volume", 999999):
            continue

        client = create_client(user["api_key"], user["api_secret"])
        try:
            quantity = round(qty * user["multiplier"], 6)
            if is_buy:
                client.order_market_buy(symbol="BTCUSDT", quantity=quantity)
            else:
                client.order_market_sell(symbol="BTCUSDT", quantity=quantity)

            user["daily_trades"] += 1
            user["daily_volume"] += quantity
        except Exception as e:
            print(f"Trade failed for user {user['user_id']}: {e}")

    save_users(users)

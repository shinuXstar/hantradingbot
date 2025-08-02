import json

def reset_risks():
    with open("user_data.json", "r") as f:
        users = json.load(f)
    for user in users:
        user["daily_trades"] = 0
        user["daily_volume"] = 0.0
    with open("user_data.json", "w") as f:
        json.dump(users, f)

reset_risks()

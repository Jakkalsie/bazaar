import requests
import pandas as pd
import numpy as np


# Setup for program
def update_request():
    request = requests.get('https://api.hypixel.net/skyblock/bazaar',
                           params={'key': API_KEY})
    return request.json()


API_KEY = 'd5a0321f-aca1-4dd3-b4ac-2c35ed175787'

balance = int(input("Enter current balance: "))
time = int(input("Enter time frame: "))
splits = int(input("Enter the amount of splits: "))
setting = input("Priority setting [1: Profit] [2: Profit/Volume]: ")

names = ['Name', 'Buy Price', 'Sell Price', 'Buy Volume', 'Sell Volume']
dataset = pd.DataFrame(columns=names)

feedback = update_request()

# Add Products to dataset
for product in feedback['products']:
    if product != "ENCHANTED_CARROT_ON_A_STICK":
        dataset = dataset.append({
            'Name': product,
            'Buy Price': feedback['products'][product]['sell_summary'][0]['pricePerUnit'],
            'Sell Price': feedback['products'][product]['buy_summary'][0]['pricePerUnit'],
            'Buy Volume': feedback['products'][product]['quick_status']['buyMovingWeek'],
            'Sell Volume': feedback['products'][product]['quick_status']['sellMovingWeek'],
            'Buy Order Volume': feedback['products'][product]['quick_status']['buyVolume'],
            'Sell Order Volume': feedback['products'][product]['quick_status']['sellVolume']},
            ignore_index=True)


# Do the profit calculation
def profit_cal(splits):
    split_bal = balance / splits
    profit_dict = []
    for item in dataset_values:
        profit_per = item[2] - item[1]

        t_volume_ph = (min(item[3], item[4]) / 10080) * time
        eff_volume_ph = np.floor(np.clip(t_volume_ph, 0, split_bal / item[1]))

        order_profit = round(profit_per * eff_volume_ph)
        volume_const = min(item[3], item[4]) / (item[5] + item[6])
        profit_dict.append({
            "Name": item[0],
            "BuyPrice": item[1],
            "Profit": order_profit,
            "Effective Volume": eff_volume_ph,
            "Volume constant": volume_const})

    # Sorting by desired setting
    if setting == '1':
        profit_dict.sort(key=lambda a: a["Profit"],
                         reverse=True)
    elif setting == '2':
        profit_dict.sort(key=lambda a: a["Profit"] * a["Volume Constant"],
                         reverse=True)

    return {
        "Splits": splits,
        "Split Profit": sum([item["Profit"] for item in profit_dict[:splits]]),
        "Profit Dict": profit_dict}


# Calculating profit for the max of 6 splits
dataset_values = dataset.to_numpy()
array_splits = []
for i in range(6):
    array_splits.append(profit_cal(i + 1))

# Warning potential loss bc of splits
most_profit_split = max(array_splits, key=lambda a: a["Split Profit"])
required_split = array_splits[splits - 1]

if most_profit_split["Splits"] != required_split["Splits"]:
    print("Potential loss made because of split: " +
          str(most_profit_split["Split Profit"] - required_split["Split Profit"]) + "\n")

# Generating the dataset to be printed
final_dict = required_split["Profit Dict"]
names = ['Invested', 'Amount', 'Profit']
final_dataset = pd.DataFrame(columns=names)
for item in final_dict[:10]:
    row = pd.Series({
        'Invested': "{:,}".format(round(item["BuyPrice"] * item["Effective Volume"])),
        'Amount': "{:,}".format(item["Effective Volume"]),
        'Profit': "{:,}".format(item["Profit"])},
        name=item["Name"])
    final_dataset = final_dataset.append(row)

print(final_dataset.to_string())
input("Press Enter to continue...")

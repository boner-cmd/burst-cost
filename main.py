import json
import requests
import matplotlib.pyplot as pp

node_url = "https://wallet.burstcoin.ro/burst?requestType="
mining_info_url = node_url + "getMiningInfo"
chain_status_url = node_url + "getBlockchainStatus"
exchange_info_url = "https://myexchangeinfobucketthing.com"  # TODO replace this with a real AWS bucket link

TERABYTE = 10 ** 12
TEBIBYTE = 2 ** 40
SPACE_CONVERSION = TERABYTE / TEBIBYTE
TERABYTE_TO_GIGABYTE = 1000
DOLLAR_TO_CENT_HUNDREDTHS = 10000
CENT_TO_CENT_HUNDREDTHS = 100
BLOCK_REWARD = 148


def get_api(url):
    try:
        response = requests.get(url)
        try:
            dict_response = response.json()
        except json.JSONDecodeError:  # TODO ensure this doesn't need to be simplejson.JSONDecodeError
            print("Response body does not contain valid JSON.")
        else:
            return dict_response
    except ConnectionError:
        print("Connection error.")


def get_prices():  # TODO query the AWS bucket for price data, throw exception on failure
    return int(0.015 * DOLLAR_TO_CENT_HUNDREDTHS)


def plot_with_commit(total_commitment, plot_size_tb):
    commitment_per_tebibyte = total_commitment / (plot_size_tb * SPACE_CONVERSION)
    commitment_ratio = commitment_per_tebibyte / average_commitment  # TODO try/catch for div by zero
    commitment_factor = commitment_ratio ** 0.4515449935  # this is an approximation
    return plot_size_tb * commitment_factor  # returns effective plot space in terabytes for given commitment


def chance_to_win(effective_space_bytes, net_space):
    return effective_space_bytes / net_space  # TODO try/catch for div by zero


budget_cent_hundredths = int(float(input("Enter your maximum budget, in USD: ")) * DOLLAR_TO_CENT_HUNDREDTHS)

cost_per_drive = int(float(input("Enter your hard drive price, in USD: ")) * DOLLAR_TO_CENT_HUNDREDTHS)
if cost_per_drive == 0:
    print('Cost of hard drive space was entered as 0- just buy Signa then!')
    raise SystemExit
unit_drive_tb = float(input("Enter your hard drive size in TB: "))
unit_drive_gb = int(unit_drive_tb * TERABYTE_TO_GIGABYTE)
cost_per_gb = cost_per_drive // unit_drive_gb
max_gb = int(budget_cent_hundredths / cost_per_gb)

print('Checking exchange data cache server for price data.')
cost_per_signa = get_prices()
print('Checking node for chain data.')
mining_info = get_api(mining_info_url)
chain_status = get_api(chain_status_url)
print('Got chain data.')
# net_space_bytes = int(chain_status["cumulativeDifficulty"])
net_space_bytes = 26259690000000000  # TODO find out where to get network size
average_commitment = round(float(mining_info["averageCommitmentNQT"]) / 1e8)  # average in whole burst

# start building the table
if max_gb % unit_drive_gb == 0:
    range_max = max_gb + unit_drive_gb
else:
    range_max = max_gb + unit_drive_gb - (max_gb % unit_drive_gb)

tb_steps = [gb / 1000 for gb in range(unit_drive_gb, range_max, unit_drive_gb)]

signa_steps = []
for step in range(len(tb_steps)):
    remaining_budget = budget_cent_hundredths - (cost_per_drive * step)
    signa_steps.append(remaining_budget / cost_per_signa)

# calculate the payout of each step
earnings = []
for step in range(len(tb_steps)):
    effective_plot_in_bytes = int(plot_with_commit(tb_steps[step], signa_steps[step]) * TERABYTE)
    chance: float = chance_to_win(effective_plot_in_bytes, net_space_bytes + effective_plot_in_bytes)
    payout = chance * BLOCK_REWARD
    daily_payout = payout * 360  # assume 4 minute blocks
    earnings.append(daily_payout)

pp.plot(tb_steps, earnings)
pp.show()

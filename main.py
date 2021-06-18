import json
import requests
import matplotlib.pyplot

node_url = "https://wallet.burstcoin.ro/burst?requestType="
mining_info_url = node_url + "getMiningInfo"
chain_status_url = node_url + "getBlockchainStatus"
exchange_info_url = "https://myexchangeinfobucketthing.com"  # TODO replace this with an AWS bucket link

TERABYTE = 10 ** 12
TEBIBYTE = 2 ** 40
SPACE_CONVERSION = TERABYTE / TEBIBYTE


def get_api(url):
    try:
        response = requests.get(url)
    except ConnectionError:
        print("Connection error.")

    try:
        dict_response = response.json()
        return dict_response
    except json.JSONDecodeError:  # TODO ensure this doesn't need to be simplejson.JSONDecodeError
        print("Response body does not contain valid JSON.")


def get_prices():  # TODO actually query the AWS bucket for price data, throw exception if it fails
    return 0.02


def plot_with_commit(target_commitment, plot_size):
    commitment_ratio = target_commitment / average_commitment  # TODO try/catch this for div by zero
    commitment_factor = commitment_ratio ** 0.4515449935  # this is an approximation
    return plot_size * commitment_factor  # returns effective plot space for a given commitment


def chance_to_win(effective_space, net_space):
    return effective_space / net_space  # TODO try/catch this for div by zero


budget_cents = abs(int(float(input("Enter your maximum budget, in USD: ")) * 100))
cost_per_tb = abs(int(float(input("Enter your hard drive price per TB, in USD: ")) * 100))
if cost_per_tb == 0:
    print('Cost of hard drive space was entered as 0- just buy Signa then!')
    raise SystemExit
max_tb = budget_cents / cost_per_tb
unit_drive = float(input("Enter your hard drive size in TB: "))
print('Checking exchange data cache server for price data.')
cost_per_signa = get_prices()
signa_per_tb = cost_per_tb / cost_per_signa
print('Checking node for chain data.')
mining_info = get_api(mining_info_url)
chain_status = get_api(chain_status_url)
net_space_bytes = chain_status["cumulativeDifficulty"]
average_commitment = round(float(mining_info["averageCommitmentNQT"]) / 1e8)  # average in whole burst

# start building the table
min_step = 1 if unit_drive > 1 else unit_drive
max_step = max_tb if max_tb % min_step == 0 else max_tb - (max_tb % min_step)
tb_steps = [step for step in range(min_step, max_step, unit_drive)]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

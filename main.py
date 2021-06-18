import json
import requests
import matplotlib.pyplot

node_url = "https://wallet.burstcoin.ro/burst?requestType="
mining_info_url = node_url + "getMiningInfo"
chain_status_url = node_url + "getBlockchainStatus"
exchange_info_url = "https://myexchangeinfobucketthing.com"  # placeholder for a bucket with the data

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
    except json.JSONDecodeError:  # check to ensure this doesn't need to be simplejson.JSONDecodeError
        print("Response body does not contain valid JSON.")


def get_prices():  # placeholder for actually getting the price of Signum
    return 0.02


mining_info = get_api(mining_info_url)
chain_status = get_api(chain_status_url)

budget_cents = int(float(input("Enter your maximum budget, in USD: ")) * 100)
cost_per_tb = int(float(input("Enter your hard drive price per TB, in USD: ")) * 100)
max_tb = budget_cents / cost_per_tb  # TODO if cost per TB is 0, output to spend the whole budget on Signa and terminate
tb_increment = 1  # increment to use for each terabyte hard drive
cost_per_signa = get_prices()
signaPerTB = cost_per_tb / cost_per_signa  # ratio of cost of committed burst to cost of hard drive space
net_space = chain_status["cumulativeDifficulty"]  # in bytes
average_commitment = round(float(mining_info["averageCommitmentNQT"]) / 1e8)  # average in whole burst


# per jjos no need to use estimated capacity, can just use real capacity

# GENESIS_TARGET = 18325193796
# nRecentBlocksMined = 1
# BASE_TARGET = miningInfo["baseTarget"]
# capacityEstimationBlocks = 360  # 360 if miner has forged 3 or more blocks in the past 360 blocks, 32400 otherwise"
# estimatedCapacity = GENESIS_TARGET/1.83*nRecentBlocksMined/(BASE_TARGET * capacityEstimationBlocks)


def effective_space(target_commitment, plot_size):
    commitment_ratio = target_commitment / average_commitment
    commitment_factor = commitment_ratio ** 0.4515449935  # this is an approximation
    return plot_size * commitment_factor


def chance_to_win(user_space):
    return user_space / net_space  # user_space is another name for effective_space


def build_table():
    min_step = 1 if tb_increment > 1 else tb_increment
    max_step = max_tb if max_tb % min_step == 0 else max_tb  # TODO change "else max_tb" to a different expression
    # else expression must evaluate to less than max_tb
    tb_steps = [step for step in range(min_step, max_step, tb_increment)]


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

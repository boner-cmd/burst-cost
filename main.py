import json
import requests
import matplotlib.pyplot

miningInfoURL = "https://wallet.burstcoin.ro/burst?requestType=getMiningInfo"
exchangeInfoURL = "https://myexchangeinfobucketthing.com"  # placeholder

TERABYTE = 10 ** 12
TEBIBYTE = 2 ** 40
SPACE_CONVERSION = TERABYTE / TEBIBYTE

response = ""
dictResponse = {}

maxBudgetCents = int(float(input("Enter your maximum budget, in USD: ")) * 100)
costPerTB = int(float(input("Enter your hard drive price per TB, in USD: ")) * 100)
MAX_TERABYTES = maxBudgetCents / costPerTB
tbIncrement = 1  # increment to use for each terabyte hard drive

costPerBurst = 0.02  # placeholder, from websockets
burstPerTB = costPerTB / costPerBurst  # warn the user that we are only using whole Burst

try:
    response = requests.get(miningInfoURL)
except ConnectionError:
    print("Connection error.")

try:
    dictResponse = response.json()
except json.JSONDecodeError:  # check to ensure this doesn't need to be simplejson.JSONDecodeError
    print("Response body does not contain valid JSON.")

averageCommitment = round(float(dictResponse["averageCommitmentNQT"]) / 1e8)  # average in whole burst
targetCommitment = 0  # placeholder, defined when generating table values
COMMITMENT_RATIO = targetCommitment / averageCommitment
COMMITMENT_FACTOR = COMMITMENT_RATIO ** 0.4515449935

print(averageCommitment)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

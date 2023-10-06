import random
import sys

import questionary
from questionary import Choice

from config import ACCOUNTS
from settings import RANDOM_WALLET, IS_SLEEP, SLEEP_TO, SLEEP_FROM
from utils.sleeping import sleep
from modules_settings import *


def get_module():
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice("1) Make bridge to Base", bridge_base),
            Choice("2) Make bridge on Orbiter", bridge_orbiter),
            Choice("3) Wrap ETH", wrap_eth),
            Choice("4) Unwrap ETH", unwrap_eth),
            Choice("5) Swap on Uniswap", swap_uniswap),
            Choice("6) Swap on Pancake", swap_pancake),
            Choice("7) Swap on WooFi", swap_woofi),
            Choice("8) Swap on BaseSwap", swap_baseswap),
            Choice("9) Swap on AlienSwap", swap_alienswap),
            Choice("10) Swap on Maverick", swap_maverick),
            Choice("11) Swap on Odos", swap_odos),
            Choice("12) Swap on 1inch", swap_inch),
            Choice("13) Swap on OpenOcean", swap_openocean),
            Choice("14) Swap on XYSwap", swap_xyswap),
            Choice("15) Bungee Refuel", bungee_refuel),
            Choice("16) Deposit Aave", deposit_aave),
            Choice("17) Withdraw Aave", withdraw_aave),
            Choice("18) Mint NFT on MintFun", mint_mintfun),
            Choice("19) Send message L2Telegraph", send_message),
            Choice("20) Mint and bridge NFT L2Telegraph", bridge_nft),
            Choice("21) Swap tokens to ETH", swap_tokens),
            Choice("22) Use Multiswap", swap_multiswap),
            Choice("23) Use custom routes", custom_routes),
            Choice("24) Check transaction count", "tx_checker"),
            Choice("25) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("\n❤️ Subscribe to me – https://t.me/sybilwave\n")
        print("🤑 Donate me: 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9")
        sys.exit()
    return result


def get_wallets():
    wallets = [
        {
            "id": _id,
            "key": key,
        } for _id, key in enumerate(ACCOUNTS, start=1)
    ]

    return wallets


def run_module(module, account_id, key):
    module(account_id, key)


def main(module):
    wallets = get_wallets()

    if RANDOM_WALLET:
        random.shuffle(wallets)

    for account in wallets:
        run_module(module, account["id"], account["key"])

        if account != wallets[-1] and IS_SLEEP:
            sleep(SLEEP_FROM, SLEEP_TO)


if __name__ == '__main__':
    print("❤️ Subscribe to me – https://t.me/sybilwave\n")

    module = get_module()
    if module == "tx_checker":
        get_tx_count()
    else:
        main(module)

    print("\n❤️ Subscribe to me – https://t.me/sybilwave\n")
    print("🤑 Donate me: 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9")

import random

from loguru import logger
from web3 import Web3
from config import BASE_TOKENS
from modules import *
from utils.sleeping import sleep


class Multiswap(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="base")

        self.swap_modules = {
            "uniswap": Uniswap,
            "pancake": Pancake,
            "woofi": WooFi,
            "baseswap": BaseSwap,
            "alienswap": AlienSwap,
            "maverick": Maverick,
            "odos": Odos,
            "inch": Inch,
            "xyswap": XYSwap,
            "openocean": OpenOcean,
        }

    def get_swap_module(self, use_dex: list):
        swap_module = random.choice(use_dex)

        return self.swap_modules[swap_module]

    async def swap(
            self,
            use_dex: list,
            sleep_from: int,
            sleep_to: int,
            min_swap: int,
            max_swap: int,
            slippage: int,
            random_swap_token: bool,
            min_percent: int,
            max_percent: int
    ):
        quantity_swap = random.randint(min_swap, max_swap)

        if random_swap_token:
            path = [random.choice(["ETH", "USDBC"]) for _ in range(0, quantity_swap)]
            USDBC_balance = await self.get_balance(BASE_TOKENS["USDBC"])
            if path[0] == "USDBC" and USDBC_balance["balance"] <= 1:
                path[0] = "ETH"
        else:
            path = ["ETH" if _ % 2 == 0 else "USDBC" for _ in range(0, quantity_swap)]

        logger.info(f"[{self.account_id}][{self.address}] Start MultiSwap | quantity swaps: {quantity_swap}")

        for _, token in enumerate(path):
            if token == "ETH":
                decimal = 6
                to_token = "USDBC"

                balance = await self.w3.eth.get_balance(self.address)

                min_amount = float(Web3.from_wei(int(balance / 100 * min_percent), "ether"))
                max_amount = float(Web3.from_wei(int(balance / 100 * max_percent), "ether"))
            else:
                decimal = 18
                to_token = "ETH"

                balance = await self.get_balance(BASE_TOKENS["USDBC"])

                min_amount = balance["balance"] if balance["balance"] <= 1 else balance["balance"] / 100 * min_percent
                max_amount = balance["balance"] if balance["balance"] <= 1 else balance["balance"] / 100 * max_percent

            swap_module = self.get_swap_module(use_dex)(self.account_id, self.private_key)
            await swap_module.swap(
                token,
                to_token,
                min_amount,
                max_amount,
                decimal,
                slippage,
                False,
                min_percent,
                max_percent
            )

            if _ + 1 != len(path):
                await sleep(sleep_from, sleep_to)

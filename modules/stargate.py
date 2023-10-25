import random
from typing import Dict, List

from loguru import logger
from config import STARGATE_CONTRACTS, STARGATE_BRIDGE_ABI, STARGATE_ROUTER_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class Stargate(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="base")

        self.chain_ids = {
            "arbitrum": 110,
            "optimism": 111,
            "linea": 183,
        }

        self.contract = self.get_contract(STARGATE_CONTRACTS["bridge"], STARGATE_BRIDGE_ABI)

    async def get_l0_fee(self, chain_id: int):
        contract = self.get_contract(STARGATE_CONTRACTS["router"], STARGATE_ROUTER_ABI)

        fee = await contract.functions.quoteLayerZeroFee(
            chain_id,
            1,
            self.address,
            "0x",
            {
                'dstGasForCall': 0,
                'dstNativeAmount': 0,
                'dstNativeAddr': "0x0000000000000000000000000000000000000001"
            }
        ).call()

        return int(fee[0] * 1.2)

    async def bridge_eth(self, chain: str, amount: int, slippage: float):
        logger.info(
            f"[{self.account_id}][{self.address}] Stargate bridge to {chain.title()} | " +
            f"{self.w3.from_wei(amount, 'ether')} ETH"
        )

        l0_fee = await self.get_l0_fee(self.chain_ids[chain])

        tx_data = await self.get_tx_data(amount + l0_fee)

        transaction = await self.contract.functions.swapETH(
            self.chain_ids[chain],
            self.address,
            self.address,
            amount,
            int(amount - (amount / 100 * slippage))
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def bridge(
            self,
            chain_list: List,
            min_amount: float,
            max_amount: float,
            decimal: int,
            slippage: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = await self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        await self.bridge_eth(random.choice(chain_list), amount_wei, slippage)

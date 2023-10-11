import random
from typing import Dict, Union

from web3 import Web3
from loguru import logger

from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account

from config import (
    RPC,
    BASE_BRIDGE_CONTRACT,
    BASE_BRIDGE_ABI,
    BASE_TOKENS,
    WETH_ABI
)


class Base(Account):
    def __init__(self, account_id: int, private_key: str, chain: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain=chain)

        self.base_w3 = Web3(Web3.HTTPProvider(random.choice(RPC[chain]["rpc"])))

    async def get_tx_data(self, value: Union[int, None] = None) -> Dict:
        tx = {
            "chainId": await self.w3.eth.chain_id,
            "from": self.address,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
        }

        if value:
            tx.update({"value": value})

        return tx

    @retry
    @check_gas
    async def deposit(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
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

        logger.info(f"[{self.account_id}][{self.address}] Bridge to Base | {amount} ETH")

        contract = self.get_contract(BASE_BRIDGE_CONTRACT, BASE_BRIDGE_ABI)

        tx_data = await self.get_tx_data(amount_wei)

        transaction = await contract.functions.depositTransaction(
            self.address,
            amount_wei,
            100000,
            False,
            "0x01"
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def wrap_eth(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
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

        weth_contract = self.get_contract(BASE_TOKENS["WETH"], WETH_ABI)

        logger.info(f"[{self.account_id}][{self.address}] Wrap {amount} ETH")

        tx_data = await self.get_tx_data(amount_wei)

        transaction = await weth_contract.functions.deposit().build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def unwrap_eth(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = await self.get_amount(
            "WETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        weth_contract = self.get_contract(BASE_TOKENS["WETH"], WETH_ABI)

        logger.info(f"[{self.account_id}][{self.address}] Unwrap {amount} ETH")

        tx_data = await self.get_tx_data()

        transaction = await weth_contract.functions.withdraw(amount_wei).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

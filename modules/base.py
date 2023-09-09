import random

from web3 import Web3
from loguru import logger
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

    def get_tx_data(self, value: int):
        tx = {
            "chainId": self.w3.eth.chain_id,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "from": self.address,
            "value": value
        }
        return tx

    def deposit(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = self.get_amount(
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

        tx_data = self.get_tx_data(amount_wei)

        try:
            transaction = contract.functions.depositTransaction(
                self.address,
                amount_wei,
                100000,
                False,
                "0x01"
            ).build_transaction(tx_data)

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
        except Exception as e:
            logger.error(f"Deposit transaction on L1 network failed | error: {e}")

    def wrap_eth(self, min_amount: float, max_amount: float, decimal: int, all_amount: bool, min_percent: int,
                 max_percent: int):
        amount_wei, amount, balance = self.get_amount(
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

        try:

            tx = {
                "from": self.address,
                "gasPrice": self.w3.eth.gas_price,
                "nonce": self.w3.eth.get_transaction_count(self.address),
                "value": amount_wei
            }

            transaction = weth_contract.functions.deposit().build_transaction(tx)

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
        except Exception as e:
            logger.error(f"[{self.account_id}][{self.address}] Error | {e}")

    def unwrap_eth(self, min_amount: float, max_amount: float, decimal: int, all_amount: bool, min_percent: int,
                   max_percent: int):
        amount_wei, amount, balance = self.get_amount(
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

        try:
            tx = {
                "from": self.address,
                "gasPrice": self.w3.eth.gas_price,
                "nonce": self.w3.eth.get_transaction_count(self.address)
            }

            transaction = weth_contract.functions.withdraw(amount_wei).build_transaction(tx)

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
        except Exception as e:
            logger.error(f"[{self.account_id}][{self.address}] Error | {e}")

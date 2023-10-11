from typing import Dict

from loguru import logger
from web3 import Web3
from config import AAVE_CONTRACT, AAVE_WETH_CONTRACT, AAVE_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class Aave(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="base")

        self.contract = self.get_contract(AAVE_CONTRACT, AAVE_ABI)

    async def get_tx_data(self) -> Dict:
        tx = {
            "chainId": await self.w3.eth.chain_id,
            "from": self.address,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
        }

        return tx

    async def get_deposit_amount(self):
        aave_weth_contract = self.get_contract(AAVE_WETH_CONTRACT)

        amount = await aave_weth_contract.functions.balanceOf(self.address).call()

        return amount

    @retry
    @check_gas
    async def deposit(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            sleep_from: int,
            sleep_to: int,
            make_withdraw: bool,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ) -> None:
        amount_wei, amount, balance = await self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        logger.info(f"[{self.account_id}][{self.address}] Make deposit on Aave | {amount} ETH")

        tx_data = await self.get_tx_data()
        tx_data.update({"value": amount_wei})

        transaction = await self.contract.functions.depositETH(
            Web3.to_checksum_address("0xA238Dd80C259a72e81d7e4664a9801593F98d1c5"),
            self.address,
            0
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

        if make_withdraw:
            await sleep(sleep_from, sleep_to)

            await self.withdraw()

    @retry
    @check_gas
    async def withdraw(self) -> None:
        amount = await self.get_deposit_amount()

        if amount > 0:
            logger.info(
                f"[{self.account_id}][{self.address}] Make withdraw from Aave | " +
                f"{Web3.from_wei(amount, 'ether')} ETH"
            )

            await self.approve(amount, "0xD4a0e0b9149BCee3C920d2E00b5dE09138fd8bb7", AAVE_CONTRACT)

            tx_data = await self.get_tx_data()
            tx_data.update({"value": 0, "nonce": await self.w3.eth.get_transaction_count(self.address)})

            transaction = await self.contract.functions.withdrawETH(
                Web3.to_checksum_address("0xA238Dd80C259a72e81d7e4664a9801593F98d1c5"),
                amount,
                self.address
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Deposit not found")

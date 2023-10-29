from loguru import logger
from config import MOONWELL_CONTRACT, MOONWELL_WETH_CONTRACT, MOONWELL_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class MoonWell(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="base")

        self.contract = self.get_contract(MOONWELL_CONTRACT, MOONWELL_ABI)
        self.weth_contract = self.get_contract(MOONWELL_WETH_CONTRACT, MOONWELL_ABI)

    async def get_deposit_amount(self):
        amount = await self.weth_contract.functions.balanceOf(self.address).call()

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

        logger.info(f"[{self.account_id}][{self.address}] Make deposit on Moonwell | {amount} ETH")

        tx_data = await self.get_tx_data(amount_wei)

        transaction = await self.contract.functions.mint(self.address).build_transaction(tx_data)

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
                f"[{self.account_id}][{self.address}] Make withdraw from Moonwell | " +
                f"{self.w3.from_wei(amount, 'ether')} ETH"
            )

            tx_data = await self.get_tx_data()

            transaction = await self.weth_contract.functions.redeem(amount).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Deposit not found")

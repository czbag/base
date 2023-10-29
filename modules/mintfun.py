import random

from loguru import logger

from config import MINTFUN_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class MintFun(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="base")

    @retry
    @check_gas
    async def mint(self, nft_contracts_data: dict):
        mint_contract = random.choice(list(nft_contracts_data))

        amount = nft_contracts_data[mint_contract]

        contract = self.get_contract(mint_contract, MINTFUN_ABI)

        nft_name = await contract.functions.name().call()

        logger.info(f"[{self.account_id}][{self.address}] Mint {amount} NFT [{nft_name}] on Mint.Fun")

        tx_data = await self.get_tx_data()

        mint_data = self.address if amount == 1 else amount

        transaction = await contract.functions.mint(mint_data).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

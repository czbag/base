from typing import Dict

from loguru import logger
from web3 import Web3

from config import MINTFUN_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class MintFun(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="base")

    async def get_tx_data(self) -> Dict:
        tx = {
            "chainId": await self.w3.eth.chain_id,
            "from": self.address,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
        }

        return tx

    @retry
    @check_gas
    async def mint(self, nft_contract: str, amount: int):
        contract = self.get_contract(nft_contract, MINTFUN_ABI)

        nft_name = await contract.functions.name().call()

        logger.info(f"[{self.account_id}][{self.address}] Mint {amount} NFT [{nft_name}] on Mint.Fun")

        tx_data = await self.get_tx_data()

        transaction = await contract.functions.mint(amount).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

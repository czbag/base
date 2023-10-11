import time
from typing import Dict

from loguru import logger
from web3 import Web3
from config import SAFE_ABI, SAFE_CONTRACT, ZERO_ADDRESS
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class GnosisSafe(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="base")

        self.contract = self.get_contract(SAFE_CONTRACT, SAFE_ABI)

    async def get_tx_data(self) -> Dict:
        tx = {
            "chainId": await self.w3.eth.chain_id,
            "from": self.address,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
        }

        return tx

    @retry
    @check_gas
    async def create_safe(self):
        logger.info(f"[{self.account_id}][{self.address}] Create gnosis safe")

        setup_data = self.contract.encodeABI(
            fn_name="setup",
            args=[
                [self.address],
                1,
                ZERO_ADDRESS,
                "0x",
                Web3.to_checksum_address("0x017062a1dE2FE6b99BE3d9d37841FeD19F573804"),
                ZERO_ADDRESS,
                0,
                ZERO_ADDRESS
            ]
        )

        tx_data = await self.get_tx_data()

        transaction = await self.contract.functions.createProxyWithNonce(
            Web3.to_checksum_address("0xfb1bffC9d739B8D520DaF37dF666da4C687191EA"),
            setup_data,
            int(time.time()*1000)
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

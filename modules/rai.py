import random
from typing import Dict

from loguru import logger
from web3 import Web3

from config import RAI_CONTRACT, RAI_ABI, BASE_TOKENS
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class Rai(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="base")

        self.contract = self.get_contract(RAI_CONTRACT, RAI_ABI)

    async def get_tx_data(self) -> Dict:
        tx = {
            "chainId": await self.w3.eth.chain_id,
            "from": self.address,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
        }

        return tx

    @retry
    @check_gas
    async def create(self):
        logger.info(f"[{self.account_id}][{self.address}] Create Rai portfolio")

        tokens = [i for i in BASE_TOKENS if i != "ETH"]

        components = [
            Web3.to_checksum_address(BASE_TOKENS[token]) for token in random.sample(
                tokens, random.randint(1, len(tokens))
            )
        ]

        amounts = random.sample(range(1000000, 99999999999999999), len(components))

        name = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(5, 20)))
        symbol = "".join(random.sample([chr(i) for i in range(65, 91)], random.randint(2, 7)))

        tx_data = await self.get_tx_data()

        transaction = await self.contract.functions.create(
            components,
            amounts,
            [
                Web3.to_checksum_address("0x1e6Dbd0E827cd243d458ed73B9Ae1a6Db89B8668"),
                Web3.to_checksum_address("0x4E69553b0aEf0949Fd38Bbf3EbeD866B431C9E68")
            ],
            self.address,
            name.title() if random.randint(0, 1) else name,
            symbol

        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

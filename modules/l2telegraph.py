from typing import Dict

from loguru import logger
from web3 import Web3

from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account
from config import (
    L2TELEGRAPH_MESSAGE_CONTRACT,
    L2TELEGRAPH_NFT_CONTRACT,
    L2TELEGRAPH_MESSAGE_ABI,
    L2TELEGRAPH_NFT_ABI
)


class L2Telegraph(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="base")

    async def get_tx_data(self) -> Dict:
        tx = {
            "chainId": await self.w3.eth.chain_id,
            "from": self.address,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
        }

        return tx

    async def get_estimate_fee(self, contract_address: str, abi: dict):
        contract = self.get_contract(contract_address, abi)

        fee = await contract.functions.estimateFees(
            175,
            self.address,
            "0x",
            False,
            "0x"
        ).call()

        return int(fee[0] * 1.2)

    async def get_nft_id(self, txn_hash: str):
        receipts = await self.w3.eth.get_transaction_receipt(txn_hash)

        nft_id = int(receipts["logs"][0]["topics"][-1].hex(), 0)

        return nft_id

    @retry
    @check_gas
    async def send_message(self):
        logger.info(f"[{self.account_id}][{self.address}] Send message")

        l0_fee = await self.get_estimate_fee(L2TELEGRAPH_MESSAGE_CONTRACT, L2TELEGRAPH_MESSAGE_ABI)

        tx_data = await self.get_tx_data()
        tx_data.update({"value": Web3.to_wei(0.00025, "ether") + l0_fee})

        contract = self.get_contract(L2TELEGRAPH_MESSAGE_CONTRACT, L2TELEGRAPH_MESSAGE_ABI)

        transaction = await contract.functions.sendMessage(
            ' ',
            175,
            "0x5f26ea1e4d47071a4d9a2c2611c2ae0665d64b6d64e0f6164ac110b67df9a4848707ffbcb86c87a9"
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    async def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint NFT")

        tx_data = await self.get_tx_data()
        tx_data.update({"value": Web3.to_wei(0.0005, "ether")})

        contract = self.get_contract(L2TELEGRAPH_NFT_CONTRACT, L2TELEGRAPH_NFT_ABI)

        transaction = await contract.functions.mint().build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

        nft_id = await self.get_nft_id(txn_hash.hex())

        return nft_id

    @retry
    @check_gas
    async def bridge(self, sleep_from, sleep_to):
        l0_fee = await self.get_estimate_fee(L2TELEGRAPH_NFT_CONTRACT, L2TELEGRAPH_NFT_ABI)

        nft_id = await self.mint()

        await sleep(sleep_from, sleep_to)

        tx_data = await self.get_tx_data()
        tx_data.update({"value": l0_fee})
        tx_data.update({"nonce": await self.w3.eth.get_transaction_count(self.address)})

        logger.info(f"[{self.account_id}][{self.address}] Bridge NFT [{nft_id}]")

        contract = self.get_contract(L2TELEGRAPH_NFT_CONTRACT, L2TELEGRAPH_NFT_ABI)

        transaction = await contract.functions.crossChain(
            175,
            "0x5b10ae182c297ec76fe6fe0e3da7c4797cede02d36a358b3ba1fb368e35b71ea40c7f4ab89bfd8e1",
            nft_id
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

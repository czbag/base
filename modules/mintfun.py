from loguru import logger
from web3 import Web3

from config import MINTFUN_ABI
from .account import Account


class MintFun(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="base")
        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address),
        }

    def mint(self, nft_contract: str, amount: int):
        contract = self.get_contract(nft_contract, MINTFUN_ABI)

        nft_name = contract.functions.name().call()

        logger.info(f"[{self.account_id}][{self.address}] Mint {amount} NFT [{nft_name}] on Mint.Fun")

        try:
            transaction = contract.functions.mint(amount).build_transaction(self.tx)

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
        except Exception as e:
            logger.error(f"[{self.account_id}][{self.address}] Error | {e}")

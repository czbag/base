import json

with open('data/rpc.json') as file:
    RPC = json.load(file)

with open('data/abi/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open("accounts.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]

with open('data/abi/base/bridge.json') as file:
    BASE_BRIDGE_ABI = json.load(file)

with open('data/abi/base/weth.json') as file:
    WETH_ABI = json.load(file)

with open("data/abi/uniswap/router.json", "r") as file:
    UNISWAP_ROUTER_ABI = json.load(file)

with open("data/abi/pancake/factory.json", "r") as file:
    UNISWAP_FACTORY_ABI = json.load(file)

with open("data/abi/uniswap/quoter.json", "r") as file:
    UNISWAP_QUOTER_ABI = json.load(file)

with open("data/abi/pancake/router.json", "r") as file:
    PANCAKE_ROUTER_ABI = json.load(file)

with open("data/abi/pancake/factory.json", "r") as file:
    PANCAKE_FACTORY_ABI = json.load(file)

with open("data/abi/pancake/quoter.json", "r") as file:
    PANCAKE_QUOTER_ABI = json.load(file)

with open("data/abi/woofi/router.json", "r") as file:
    WOOFI_ROUTER_ABI = json.load(file)

with open("data/abi/baseswap/router.json", "r") as file:
    BASESWAP_ROUTER_ABI = json.load(file)

with open("data/abi/bungee/abi.json", "r") as file:
    BUNGEE_ABI = json.load(file)

with open("data/abi/aave/abi.json", "r") as file:
    AAVE_ABI = json.load(file)

with open("data/abi/l2telegraph/send_message.json", "r") as file:
    L2TELEGRAPH_MESSAGE_ABI = json.load(file)

with open("data/abi/l2telegraph/bridge_nft.json", "r") as file:
    L2TELEGRAPH_NFT_ABI = json.load(file)

with open("data/abi/mintfun/abi.json", "r") as file:
    MINTFUN_ABI = json.load(file)

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

BASE_BRIDGE_CONTRACT = "0x49048044D57e1C92A77f79988d21Fa8fAF74E97e"

ORBITER_CONTRACT = "0xe4edb277e41dc89ab076a1f049f4a3efa700bce8"

BASE_TOKENS = {
    "ETH": "0x4200000000000000000000000000000000000006",
    "WETH": "0x4200000000000000000000000000000000000006",
    "USDC": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",
}

UNISWAP_CONTRACTS = {
    "router": "0x2626664c2603336E57B271c5C0b26F421741e481",
    "factory": "0x33128a8fC17869897dcE68Ed026d694621f6FDfD",
    "quoter": "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a",
}

PANCAKE_CONTRACTS = {
    "router": "0x678Aa4bF4E210cf2166753e054d5b7c31cc7fa86",
    "factory": "0x0BFbCF9fa4f9C56B0F40a671Ad40E0805A091865",
    "quoter": "0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997"
}

WOOFI_CONTRACTS = {
    "router": "0x27425e9fb6a9a625e8484cfd9620851d1fa322e5"
}

BASESWAP_CONTRACTS = {
    "router": "0x327Df1E6de05895d2ab08513aaDD9313Fe505d86"
}

ODOS_CONTRACT = {
    "router": "0x19ceead7105607cd444f5ad10dd51356436095a1",
    "use_ref": True
}

BUNGEE_CONTRACT = "0xe8c5b8488feafb5df316be73ede3bdc26571a773"

AAVE_CONTRACT = "0x18cd499e3d7ed42feba981ac9236a278e4cdc2ee"

AAVE_WETH_CONTRACT = "0xD4a0e0b9149BCee3C920d2E00b5dE09138fd8bb7"

MINTFUN_CONTRACT = "0xf39ac57beaf8f97b89db7a9203a4e47c17cf4391"

L2TELEGRAPH_MESSAGE_CONTRACT = "0x64e0f6164ac110b67df9a4848707ffbcb86c87a9"

L2TELEGRAPH_NFT_CONTRACT = "0x36a358b3ba1fb368e35b71ea40c7f4ab89bfd8e1"

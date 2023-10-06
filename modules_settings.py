import asyncio

from modules import *


def bridge_base(account_id, key):
    """
    Deposit from official bridge
    ______________________________________________________
    all_amount - bridge from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 5
    max_percent = 10

    base = Base(account_id, key, "ethereum")
    base.deposit(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


def bridge_orbiter(account_id, key):
    """
    Bridge from orbiter
    ______________________________________________________
    from_chain – ethereum, base, polygon_zkevm, arbitrum, optimism, zksync | Select one
    to_chain – ethereum, base, polygon_zkevm, arbitrum, optimism, zksync | Select one
    """

    from_chain = "arbitrum"
    to_chain = "base"

    min_amount = 0.005
    max_amount = 0.0051
    decimal = 4

    all_amount = False

    min_percent = 5
    max_percent = 10

    orbiter = Orbiter(account_id, key, from_chain)
    orbiter.bridge(to_chain, min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


def wrap_eth(account_id, key):
    """
    Wrap ETH
    ______________________________________________________
    all_amount - wrap from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 5
    max_percent = 10

    base = Base(account_id, key, "base")
    base.wrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


def unwrap_eth(account_id, key):
    """
    Unwrap ETH
    ______________________________________________________
    all_amount - unwrap from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 100
    max_percent = 100

    base = Base(account_id, key, "base")
    base.unwrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


def swap_uniswap(account_id, key):
    """
    Make swap on Uniswap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.001
    max_amount = 0.002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    uniswap = Uniswap(account_id, key)
    uniswap.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def swap_pancake(account_id, key):
    """
    Make swap on PancakeSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDC"

    min_amount = 0.001
    max_amount = 0.002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 10
    max_percent = 15

    pancake = Pancake(account_id, key)
    pancake.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def swap_woofi(account_id, key):
    """
    Make swap on WooFi
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    woofi = WooFi(account_id, key)
    woofi.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def swap_baseswap(account_id, key):
    """
    Make swap on BaseSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    baseswap = BaseSwap(account_id, key)
    baseswap.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def swap_alienswap(account_id, key):
    """
    Make swap on AlienSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDC"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 10
    max_percent = 10

    alienswap = AlienSwap(account_id, key)
    alienswap.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                   max_percent)


def swap_odos(account_id, key):
    """
    Make swap on Odos
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    odos = Odos(account_id, key)
    odos.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


def swap_inch(account_id, key):
    """
    Make swap on 1inch
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "WETH"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    inch_dex = Inch(account_id, key)
    inch_dex.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def swap_openocean(account_id, key):
    """
    Make swap on OpenOcean
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "WETH"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0001
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    openocean = OpenOcean(account_id, key)
    openocean.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


def swap_xyswap(account_id, key):
    """
    Make swap on XYSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "WETH"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0001
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    xyswap = XYSwap(account_id, key)
    xyswap.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


def swap_maverick(account_id, key):
    """
    Make swap on Maverick
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0001
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 10
    max_percent = 10

    maverick = Maverick(account_id, key)
    maverick.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def bungee_refuel(account_id, key):
    """
    Make refuel on Bungee
    ______________________________________________________
    to_chain – Choose DESTINATION chain: BSC, OPTIMISM, GNOSIS, POLYGON, ZKSYNC, ARBITRUM, AVALANCHE, AURORA, ZK_EVM

    Disclaimer - The chain will be randomly selected
    ______________________________________________________
    random_amount – True - amount random from min to max | False - use min amount
    """

    chain_list = ["BSC", "GNOSIS", "AURORA"]

    random_amount = False

    bungee = Bungee(account_id, key)
    bungee.refuel(chain_list, random_amount)


def deposit_aave(account_id, key):
    """
    Make deposit on Aave
    ______________________________________________________
    make_withdraw - True, if need withdraw after deposit

    all_amount - deposit from min_percent to max_percent
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    sleep_from = 5
    sleep_to = 24

    make_withdraw = True

    all_amount = True

    min_percent = 5
    max_percent = 10

    aave = Aave(account_id, key)
    aave.deposit(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


def bridge_nft(account_id, key):
    """
    Make mint NFT and bridge NFT on L2Telegraph
    """

    sleep_from = 5
    sleep_to = 20

    l2telegraph = L2Telegraph(account_id, key)
    l2telegraph.bridge(sleep_from, sleep_to)


def mint_mintfun(account_id, key):
    """
    Mint NFT on Mint.Fun
    ______________________________________________________
    Disclaimer - The Mint function should be called "mint", to make sure of this, look at the name in Rabby Wallet or in explorer
    """

    nft_contract = "0x"
    amount = 0

    mintfun = MintFun(account_id, key)
    mintfun.mint(nft_contract, amount)


def swap_tokens(account_id, key):
    """
    SwapTokens module: Automatically swap tokens to ETH
    ______________________________________________________
    use_dex - Choose any dex: uniswap, pancake, woofi, baseswap, alienswap, maverick, odos, inch, xyswap, openocean
    """

    use_dex = [
        "uniswap", "pancake", "woofi", "baseswap",
        "alienswap", "maverick", "odos", "inch",
        "xyswap", "openocean"
    ]

    use_tokens = ["USDC"]

    sleep_from = 300
    sleep_to = 600

    slippage = 1

    min_percent = 100
    max_percent = 100

    swap_tokens = SwapTokens(account_id, key)
    swap_tokens.swap(use_dex, use_tokens, sleep_from, sleep_to, slippage, min_percent, max_percent)


def swap_multiswap(account_id, key):
    """
    Multi-Swap module: Automatically performs the specified number of swaps in one of the dexes.
    ______________________________________________________
    use_dex - Choose any dex: uniswap, pancake, woofi, baseswap, alienswap, maverick, odos, inch, xyswap, openocean
    quantity_swap - Quantity swaps
    ______________________________________________________
    random_swap_token - If True the swap path will be [ETH -> USDC -> USDC -> ETH] (random!)
    If False the swap path will be [ETH -> USDC -> ETH -> USDC]
    """

    use_dex = ["uniswap", "pancake", "woofi", "baseswap", "odos"]

    min_swap = 2
    max_swap = 3

    sleep_from = 300
    sleep_to = 700

    slippage = 1

    random_swap_token = True

    min_percent = 5
    max_percent = 10

    multi = Multiswap(account_id, key)
    multi.swap(use_dex, sleep_from, sleep_to, min_swap, max_swap, slippage, random_swap_token, min_percent, max_percent)


def custom_routes(account_id, key):
    """
    You can use these methods:
    bridge_base, bridge_orbiter, wrap_eth, unwrap_eth
    swap_uniswap, swap_pancake, swap_woofi, swap_baseswap, swap_odos
    bungee_refuel, deposit_aave, withdraw_aave,
    mint_mintfun, bridge_nft, send_message
    swap_multiswap
    ______________________________________________________
    Disclaimer - You can add modules to [] to select random ones,
    example [module_1, module_2, [module_3, module_4], module 5]
    The script will start with module 1, 2, 5 and select a random one from module 3 and 4
    """

    use_modules = [[bridge_nft, send_message], deposit_aave, mint_mintfun]

    sleep_from = 10
    sleep_to = 20

    random_module = True

    routes = Routes(account_id, key)
    routes.start(use_modules, sleep_from, sleep_to, random_module)


#########################################
########### NO NEED TO CHANGE ###########
#########################################

def withdraw_aave(account_id, key):
    aave = Aave(account_id, key)
    aave.withdraw()


def send_message(account_id, key):
    l2telegraph = L2Telegraph(account_id, key)
    l2telegraph.send_message()


def get_tx_count():
    asyncio.run(check_tx())

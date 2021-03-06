from brownie import FundMe, MockV3Aggregator, config, network

from scripts import helpful_scripts


def deploy_fund_me():
    account = helpful_scripts.get_account()

    # Pass the price feed address to our fundme contract
    # If we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    if network.show_active() not in helpful_scripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        helpful_scripts.deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address, {"from": account}, publish_source=config["networks"][network.show_active()].get("verify")
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()

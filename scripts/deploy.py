from brownie import *
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    accounts.add(os.getenv("pk"))
    acc = accounts.at(os.getenv("myAccount"), force=True)
    router = '0x61935CbDd02287B511119DDb11Aeb42F1593b7Ef'

    swap_proxy = SwapProxy.deploy(
        router,
        {'from': acc}
        
    )

    print(f'Deployed SwapProxy at {swap_proxy}')

    run('swap')
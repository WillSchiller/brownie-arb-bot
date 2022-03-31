from brownie import *
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    accounts.add(os.getenv("pk"))
    acc = accounts.at(os.getenv("myAccount"), force=True)
    router = '0x1111111254fb6c44bAC0beD2854e76F90643097d'

    swap_proxy = SwapProxy.deploy(
        router,
        {'from': acc}
        
    )

    print(f'Deployed SwapProxy at {swap_proxy}')

    run('swap')
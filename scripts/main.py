import json 
import requests
from web3 import Web3, EthereumTesterProvider
from dotenv import load_dotenv
import os
from brownie import *
from .abi import oneInchV4, zeroX

load_dotenv()

oneInchv4 = oneInchV4()
zerox = zeroX()

w3 = Web3(Web3.HTTPProvider( os.getenv('RPC')))

baseAssetAddress = os.getenv('baseAssetAddress')
quoteAssetAddress = os.getenv('quoteAssetAddress')

def main():
    try:
        base = baseAssetAddress[2:]
        quote = quoteAssetAddress[2:]
        res = requests.get(f'https://api.0x.org/sra/v3/orderbook?baseAssetData=0xf47261b0000000000000000000000000{base}&quoteAssetData=0xf47261b0000000000000000000000000{quote}&perPage=1000')
        _0x_txs = res.json()['bids']['records'] 
        arb_results = map(checkArb, _0x_txs)
        arb_results = list(arb_results)
        #print(arb_results)
    except Exception as e:
        print(f"error:{e}")

def checkArb(r):
  zrxOrder, metadata = (r['order'], r['metaData'])
  inputAssetAmount = zrxOrder['takerAssetAmount']
  out2 = Web3.fromWei(int(zrxOrder['makerAssetAmount']), 'ether')
  amount = zrxOrder['makerAssetAmount']
  oneInchOrder = requests.get(f'https://api.1inch.exchange/v4.0/1/quote?fromTokenAddress={quoteAssetAddress}&toTokenAddress={baseAssetAddress}&amount={amount}').json()
  outputAssetAmount = oneInchOrder['toTokenAmount']
  netProfit =   Web3.fromWei(int(outputAssetAmount), 'ether') - Web3.fromWei(int(inputAssetAmount), 'ether') 
  if netProfit > 0.1:
    print(netProfit)
    print(out2)
    print(Web3.fromWei(int(outputAssetAmount), 'ether'))
    print(Web3.fromWei(int(inputAssetAmount), 'ether'))
    trade(zrxOrder, oneInchOrder)

def trade(zrxOrder, oneInchOrder):
  acc = accounts.at(os.getenv("myAccount"), force=True)
  #swap_proxy = SwapProxy[len(SwapProxy) - 1]
  #print(swap_proxy)
  print(zrxOrder)
  print("================")
  print(oneInchOrder)

# ----------------------------------------------------- # 
# DONT FORGET FLASHBOTS ;) HAHAH // NO FRONT RUN PLEASE
# ----------------------------------------------------- #
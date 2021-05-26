import gather
from fastapi import FastAPI

app = FastAPI(title="Cryptocurrency API",
              version="0.0.1")

@app.get('/')
async def index():

    return {'message' : 'to learn how to use my API go to the info page at <current url>/info'}

@app.get('/info')
async def info():
    pass

@app.get('/btc')
@app.get('/BTC')
@app.get('/Bitcoin')
async def bitcoin():

    content, err = gather.retrieve_data(key='BTC')

    if not err:
        return content
    
    return {"Error": err}

@app.get('/doge')
@app.get('/DOGE')
@app.get('/Dogecoin')
async def dogecoin():

    content, err = gather.retrieve_data(key='DOG')

    return content

@app.get('/ltc')
@app.get('/LTC')
@app.get('/Litecoin')
async def litecoin():

    content, err = gather.retrieve_data(key='LTC')

    return content

@app.get('/eth')
@app.get('/ETH')
@app.get('/Ethereum')
async def ethereum():

    content, err = gather.retrieve_data(key='ETH')

    return content

@app.get('/bch')
@app.get('/BCH')
@app.get('/BitcoinCash')
async def bitcoinCash():

    content, err = gather.retrieve_data(key='BCH')

    return content

@app.get('/dash')
@app.get('/DASH')
async def dash():

    content, err = gather.retrieve_data(key='DSH')

    return content

@app.get('/Cardano')
@app.get('/ada')
@app.get('/ADA')
async def cardano():

    content, err = gather.retrieve_data(key='ADA')

    return content
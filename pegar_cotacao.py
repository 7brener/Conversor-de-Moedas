import requests

def pegar_cotacao_moeda(moeda_origem, moeda_destino):
    link = f"https://economia.awesomeapi.com.br/last/{moeda_origem}-{moeda_destino}"
    requisicao = requests.get(link)

    cotacao = requisicao.json()[f"{moeda_origem}{moeda_destino}"]["bid"]

    # para se quiser formatar as casas decimais depois
    return float(cotacao) 

def cotacoes_coingecko(nome_cripto):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={nome_cripto}&vs_currencies=usd'
    requisicao = requests.get(url)
    moedas = requisicao.json()
    cotacao = moedas[nome_cripto]['usd']
    return float(cotacao)

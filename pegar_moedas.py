import xmltodict
import os
import sys
from pprint import pp

# Com isso, independetemente do local que o .exe seja executado, ele vai achar os arquivos .xml
def resource_path(rel_path):
    ''' _MEIPASS só existe quando o programa está rodando como um executável.
    Os arquivos extras (como XML, imagens etc.) são extraídos para uma pasta temporária, 
    cujo caminho está em sys._MEIPASS'''
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

def nome_moedas():
    with open(resource_path('moedas.xml'), 'rb') as arquivo_moedas:
        dict_moedas = xmltodict.parse(arquivo_moedas)
        moedas = dict_moedas['xml']
    return moedas

def conversoes_disponiveis():
    with open(resource_path('conversoes.xml'), 'rb') as arquivo_conversoes:
        dict_conversoes = xmltodict.parse(arquivo_conversoes)
        dict_conversoes = dict_conversoes['xml']

        conversoes_disponiveis = {}
        for par in dict_conversoes:
            moeda_origem, moeda_destino = par.split('-')
            if moeda_origem not in conversoes_disponiveis:
                conversoes_disponiveis[moeda_origem] = [moeda_destino]
            else:
                conversoes_disponiveis[moeda_origem].append(moeda_destino)

        return conversoes_disponiveis



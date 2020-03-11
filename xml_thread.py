from xml.dom import minidom
from threading import Timer
from multiprocessing.pool import ThreadPool
import requests
import os

pool = ThreadPool(processes=4)
logs = './TXT/'


def json_products_xml(xml_products):
    json_file = dict()
    for product in xml_products:
        id = product.getElementsByTagName('cProd')
        prod = product.getElementsByTagName('xProd')
        ncm = product.getElementsByTagName('NCM')
        cfop = product.getElementsByTagName('CFOP')
        metric = product.getElementsByTagName('uCom')
        quant = product.getElementsByTagName('qCom')
        v_unit = product.getElementsByTagName('vProd')

        json_file[id[0].firstChild.nodeValue] = {
            'product_code': id[0].firstChild.nodeValue,
            'product_name': prod[0].firstChild.nodeValue,
            'product_ncm': ncm[0].firstChild.nodeValue,
            'product_cfop': cfop[0].firstChild.nodeValue,
            'product_metric': metric[0].firstChild.nodeValue,
            'product_quant': quant[0].firstChild.nodeValue.split('.')[0],
            'product_price': v_unit[0].firstChild.nodeValue
        }
    return json_file


def extract_products_xml(path, token):
    files_xml = os.listdir(path['dir'])
    count = 0
    for file in files_xml:
        if file.endswith(".xml"):
            if file.split('.')[1] == 'xml':
                count += 1
                doc_xml = minidom.parse(path['xml_dir'] + file)
                products = doc_xml.getElementsByTagName('prod')
                try:
                    Timer(2.0, os.remove(path['xml_dir'] + file))
                    cadastrar_produtos(token, json_products_xml(products))
                except Exception:
                    cadastrar_produtos(token, json_products_xml(products))
            else:
                try:
                    Timer(2.0, os.remove(path['xml_dir'] + file))
                except Exception:
                    pass
        files_xml = os.listdir(path['dir'])
    if (count > 0):
        return True
    return None


def salvar_txt(diretorio, registro):
    if (not os.path.isdir(diretorio)):
        os.mkdir(diretorio)
    try:
        arquivo = open(f'{diretorio}PRODODUTOS_CADASTRADOS.txt', 'a')
        arquivo.writelines(str(registro) + '\n')
        arquivo.close()
    except FileNotFoundError:
        arquivo = open(f'{diretorio}PRODODUTOS_CADASTRADOS.txt', 'a')
        arquivo.writelines(str(registro) + '\n')
        arquivo.close()


def cadastrar_produtos(token, jsonfile):
    cadastrados = list()
    url = 'https://app-apisystem.herokuapp.com/cadastro-produtos'
    headers = {'Authorization': f'Bearer {token}'}
    for product in jsonfile:
        input_product = jsonfile[product]
        req = requests.post(url, headers=headers, json=input_product)
        if (req.status_code == 200):
            cadastrados.append(product)
    salvar_txt(logs, cadastrados)

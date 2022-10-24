from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
import pandas as pd
import json, requests
from bs4 import BeautifulSoup


#
#dados_2017 = ibge_2017[ibge_2017['Ano'] == 2017].reset_index(drop = True)

#


app = FastAPI()

@app.get("/")
async def home():
    api_url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    df_estados = pd.read_json(api_url)
    df_estados["fonte"] = "IBGE"
    response = df_estados.to_json(orient='records', force_ascii=False)
    return json.loads(response)

@app.get("/estados")
def home():
    api_url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    df_estados = pd.read_json(api_url)
    df_estados["fonte"] = "IBGE"
    response = df_estados.to_json(orient='records', force_ascii=False)
    return json.loads(response)


@app.get('/estado/{UF}')
def get_UF(
    UF: str = Path(
        None,
        description="Preencha com o ID do item que deseja visualizar")):


    api_url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF_ESTADO}'

    request = requests.get(api_url.format(UF_ESTADO=UF))
    response = json.loads(request.content)

    
    df_indicador = pd.DataFrame()

    url = "https://www.ibge.gov.br/cidades-e-estados/{UF_ESTADO}.html"

    res =requests.get(url.format(UF_ESTADO=UF))

    data = BeautifulSoup(res.text, 'html')

    data1 = data.find('ul', {"class":"resultados-padrao"})
    

    for li in data1.find_all("li"):
        #print(li.find({"class":"ind-label"}))
        coluna = li.find("div", {"class": "ind-label"}).text

        #print(li.find({"class":"ind-value"}))
        valor = li.find("p", {"class": "ind-value"}).text
        df_indicador.at[0,coluna] = valor
    #df_estado["fonte"] = "IBGE"

    

    df_agro5 = pd.read_csv('../dados/df_agro5.csv')
    df_agro5_filtered = df_agro5.query('Local == "{estado}"'.format(estado = response["nome"]))
    df_agro5_filtered.drop(df_agro5_filtered.columns[[0, 1]],axis = 1, inplace=True)
        
    df_edu = pd.read_csv('../dados/df_edu_1.csv')
    df_edu_filtered = df_edu.query('SG_UF_IES == "{UF_ESTADO}"'.format(UF_ESTADO = UF))
    df_edu_filtered["fonte"] = "INEP"

    json_edu = df_edu_filtered.to_json(orient='records', force_ascii=False)
    json_indicadores = df_indicador.to_json(orient='records', force_ascii=False)
    json_agro5 = df_agro5_filtered.to_json(orient='records', force_ascii=False)
    #json_agro5.drop(["Unnamed", "Local"], inplace=True)
    

    response["Indicadores"] = json.loads(json_indicadores)
    response["Agro"] = json.loads(json_agro5)
    response["Educação"] = json.loads(json_edu)
    response["fonte"] = "IBGE"
    

    #response = df_UF.to_json(orient='records', force_ascii=False)
    #response = df_agro5_filtered.to_json(orient='records', force_ascii=False)
    return response


@app.get('/estado/{UF}/{municipio}')
def get_municipio(
    UF: str = Path(
        None,
        description="Preencha com o UF do item que deseja visualizar"),
    municipio: str = Path(
        None,
        description="Preencha com o municipio do item que deseja visualizar")):

    
    df_indicador = pd.DataFrame()

    url = "https://www.ibge.gov.br/cidades-e-estados/{UF_ESTADO}/{municipio_nome}.html"

    res =requests.get(url.format(UF_ESTADO=UF, municipio_nome = municipio))

    soup = BeautifulSoup(res.text, 'html')

    indicador = soup.find('ul', {"class":"resultados-padrao"})
    codigo_municipio = int(soup.find('p', {"class":"codigo"}).text.split(" ")[1])
    
    

    for li in indicador.find_all("li"):
        #print(li.find({"class":"ind-label"}))
        coluna = li.find("div", {"class": "ind-label"}).text

        #print(li.find({"class":"ind-value"}))
        valor = li.find("p", {"class": "ind-value"}).text
        df_indicador.at[0,coluna] = valor
    #df_estado["fonte"] = "IBGE"

    

    #df_municipio 




    api_url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{municipio_id}'
    #df_municipio = pd.read_json(api_url.format(municipio_id=codigo_municipio), orient='index').T
    request = requests.get(api_url.format(municipio_id=codigo_municipio))
    response = json.loads(request.content)

    df_postos_saude = pd.read_csv('../dados/postos_saude.csv', encoding = "UTF-8", sep = ',')
    df_postos_saude.drop(df_postos_saude.columns[[0, 1]],axis = 1, inplace=True)
    df_postos_saude.drop('municipio.microrregiao.mesorregiao.UF.id', inplace=True, axis=1)
    df_postos_saude.drop('municipio.microrregiao.mesorregiao.UF.sigla', inplace=True, axis=1)
    df_postos_saude.drop('municipio.microrregiao.mesorregiao.UF.nome', inplace=True, axis=1)
    df_postos_saude.drop('municipio.microrregiao.mesorregiao.UF.regiao.id', inplace=True, axis=1) 
    df_postos_saude.drop('municipio.microrregiao.mesorregiao.UF.regiao.sigla', inplace=True, axis=1)
    df_postos_saude.drop('municipio.microrregiao.mesorregiao.UF.regiao.nome', inplace=True, axis=1)
    df_postos_saude.drop('municipio.regiao-imediata.id', inplace=True, axis=1)
    df_postos_saude.drop('municipio.regiao-imediata.nome', inplace=True, axis=1)
    df_postos_saude.drop('municipio.regiao-imediata.regiao-intermediaria.id', inplace=True, axis=1)
    df_postos_saude.drop('municipio.regiao-imediata.regiao-intermediaria.nome', inplace=True, axis=1)
    df_postos_saude.drop('municipio.regiao-imediata.regiao-intermediaria.UF.id', inplace=True, axis=1)
    df_postos_saude.drop('municipio.regiao-imediata.regiao-intermediaria.UF.sigla', inplace=True, axis=1)
    df_postos_saude.drop('municipio.regiao-imediata.regiao-intermediaria.UF.nome', inplace=True, axis=1)
    df_postos_saude.drop('municipio.regiao-imediata.regiao-intermediaria.UF.regiao.id', inplace=True, axis=1)
    df_postos_saude.drop('municipio.regiao-imediata.regiao-intermediaria.UF.regiao.sigla', inplace=True, axis=1)
    df_postos_saude.drop('municipio.regiao-imediata.regiao-intermediaria.UF.regiao.nome', inplace=True, axis=1)
    df_postos_saude.drop('municipio.microrregiao.nome', inplace=True, axis=1)
    df_postos_saude.drop('municipio.microrregiao.id', inplace=True, axis=1)

    df_postos_saude_filter = df_postos_saude[df_postos_saude['municipio.id'] == 4127700]
    df_postos_saude_filter["fonte"] = "DataSUS"
  

    #df_agro5 = pd.read_csv('../dados/df_agro5.csv')
    #df_agro5_filtered = df_agro5.query('Local == "{estado}"'.format(estado = df_UF["nome"][0]))
    #df_agro5_filtered.drop(df_agro5_filtered.columns[[0, 1]],axis = 1, inplace=True)
        
    json_indicadores = df_indicador.to_json(orient='records', force_ascii=False)
    json_postos_saude = df_postos_saude_filter.to_json(orient='records', force_ascii=False)


    response["Indicadores"] = json.loads(json_indicadores)
    response["Saude"] = json.loads(json_postos_saude)
    response["fonte"] = "IBGE"


    #response["Saude"] = json_postos_saude

    return response


#https://servicodados.ibge.gov.br/api/docs/localidades
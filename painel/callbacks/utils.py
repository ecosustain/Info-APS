"""Módulo com funções utilitárias para o painel"""

import pandas as pd

estados_brasileiros = [
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
]


def get_json_municipios():
    """Função para obter o json com os municípios do Brasil"""
    municipios = pd.read_json("data/reg_mun.json")
    return municipios


municipios = get_json_municipios()


def get_regioes(estado):
    """Função para obter um dicionário com as regiões de um estado"""
    # TODO implementar via API
    regioes_estado = municipios[municipios["uf"] == estado][
        ["regiao", "no_regiao"]
    ].drop_duplicates()
    regioes_dict = dict(
        zip(regioes_estado["regiao"], regioes_estado["no_regiao"])
    )
    # Remover o primeiro caractere de cada valor caso seja um espaço
    regioes_dict = {
        k: v[1:] if v[0] == " " else v for k, v in regioes_dict.items()
    }
    # ordenar o dicionário pelo valor
    regioes_dict = dict(sorted(regioes_dict.items(), key=lambda item: item[1]))
    return regioes_dict


def get_regiao_municipio(estado, municipio):
    """Função para obter a região de um município"""
    regiao = municipios[
        (municipios["uf"] == estado)
        & (municipios["municipio"] == municipio)
    ]["no_regiao"].values[0]
    if len(regiao) < 3:
        print(f"Erro ao obter a região do município {municipio}")
        return None
    return regiao


def get_municipios_regiao(regiao):
    """Função para obter um dicionario dos ibge e municipios de uma região"""
    # TODO implementar via API
    municipios_regiao = municipios[municipios["no_regiao"] == regiao][
        ["ibge", "municipio"]
    ].drop_duplicates()
    municipios_dict = dict(
        zip(municipios_regiao["ibge"], municipios_regiao["municipio"])
    )
    return municipios_dict


def get_ibge_code(estado, mun):
    """Função para obter o cód IBGE de um município a partir
    do nome e do estado"""
    # TODO implementar via API
    cod = municipios[
        (municipios["uf"] == estado) & (municipios["municipio"] == mun)
    ]["ibge"]
    if len(cod) != 1:
        print(f"Erro ao obter o código do município {mun} no estado {estado}")
        return None
    return cod.values[0]


def get_code_regiao(estado, regiao):
    """Função para obter o código da região de um estado"""
    # TODO implementar via API
    cod = municipios[
        (municipios["uf"] == estado) & (municipios["no_regiao"] == regiao)
    ]["regiao"]
    if len(cod) == 0:
        print(f"Erro ao obter o código da região {regiao} no estado {estado}")
        return None
    return cod.values[0]


def get_type(estado, regiao, municipio):
    """Função para obter o tipo de localidade"""
    if estado is None and regiao is None and municipio is None:
        return "brasil"
    elif estado is not None and regiao is None and municipio is None:
        return "estado"
    elif estado is not None and regiao is not None and municipio is None:
        return "regiao"
    elif estado is not None and municipio is not None:
        return "municipio"
    return None


def get_population(estado, regiao, mun):
    """Função para obter a população de um município, estado ou do Brasil"""
    # TODO implementar via API
    if estado is None and regiao is None and mun is None:
        # soma de todas as populações
        total = municipios["cadastros"].sum()
        return total
    if regiao is None and mun is None:
        # soma da população da estado
        total = municipios[municipios["uf"] == estado]["cadastros"].sum()
        return total
    if mun is None:
        # soma da população do regiao
        total = municipios[municipios["no_regiao"] == regiao][
            "cadastros"
        ].sum()
        return total

    # população do município específico
    total = municipios[
        (municipios["uf"] == estado) & (municipios["municipio"] == mun)
    ]["cadastros"].sum()
    return total


# Função para formatar números grandes
def formatar_numero(numero):
    """Função para formatar números grandes"""
    if numero >= 1_000_000_000:
        return f"{numero / 1_000_000_000:.1f}B"
    elif numero >= 1_000_000:
        return f"{numero / 1_000_000:.1f}M"
    elif numero >= 1_000:
        return f"{numero / 1_000:.1f}K"
    return str(numero)

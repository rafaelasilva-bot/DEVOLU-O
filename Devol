[gemini-code-1789665990311.py](https://github.com/user-attachments/files/32347144/gemini-code-1789665990311.py)
import pandas as pd
import streamlit as st
import xml.etree.ElementTree as ET

st.set_page_config(
    page_title="Determinar Natureza de Operação - ERP", page_icon="⚙️"
)
st.title("⚙️ Mapeador de Natureza de Operação para Devoluções")


# Tabela de regras extraída da aba 'Natureza de op' do Excel da empresa
REGRAS_NATUREZA_ERP = [
    # CFOP 1202 / 2202 (Comprado/Revenda)
    {
        "cfop": "1202",
        "icms": "T",
        "ipi": 0.0,
        "pis_cofins": 70.0,
        "nat_op_erp": "1202A",
        "cod_completo": "1202T0070",
    },
    {
        "cfop": "1202",
        "icms": "T",
        "ipi": 1.0,
        "pis_cofins": 70.0,
        "nat_op_erp": "1202B",
        "cod_completo": "1202T0170",
    },
    {
        "cfop": "1202",
        "icms": "T",
        "ipi": 3.0,
        "pis_cofins": 54.0,
        "nat_op_erp": "1202C",
        "cod_completo": "1202T0354",
    },
    {
        "cfop": "1202",
        "icms": "T",
        "ipi": 1.0,
        "pis_cofins": 54.0,
        "nat_op_erp": "1202D",
        "cod_completo": "1202T0154",
    },
    {
        "cfop": "1202",
        "icms": "R",
        "ipi": 1.0,
        "pis_cofins": 54.0,
        "nat_op_erp": "1202E",
        "cod_completo": "1202R0154",
    },
    {
        "cfop": "1202",
        "icms": "T",
        "ipi": 1.0,
        "pis_cofins": 73.0,
        "nat_op_erp": "1202F",
        "cod_completo": "1202T0173",
    },
    {
        "cfop": "1202",
        "icms": "R",
        "ipi": 1.0,
        "pis_cofins": 73.0,
        "nat_op_erp": "1202G",
        "cod_completo": "1202R0173",
    },
    {
        "cfop": "1202",
        "icms": "I",
        "ipi": 3.0,
        "pis_cofins": 54.0,
        "nat_op_erp": "1202H",
        "cod_completo": "1202I0354",
    },
    {
        "cfop": "1202",
        "icms": "I",
        "ipi": 1.0,
        "pis_cofins": 70.0,
        "nat_op_erp": "1202I",
        "cod_completo": "1202I0170",
    },
    {
        "cfop": "1202",
        "icms": "I",
        "ipi": 1.0,
        "pis_cofins": 73.0,
        "nat_op_erp": "1202J",
        "cod_completo": "1202I0173",
    },
    {
        "cfop": "1202",
        "icms": "T",
        "ipi": 0.0,
        "pis_cofins": 54.0,
        "nat_op_erp": "1202K",
        "cod_completo": "1202T0054",
    },
    # CFOP 2202 (Interestadual Comprado/Revenda)
    {
        "cfop": "2202",
        "icms": "T",
        "ipi": 0.0,
        "pis_cofins": 70.0,
        "nat_op_erp": "2202A",
        "cod_completo": "2202T0070",
    },
    {
        "cfop": "2202",
        "icms": "T",
        "ipi": 1.0,
        "pis_cofins": 70.0,
        "nat_op_erp": "2202B",
        "cod_completo": "2202T0170",
    },
    {
        "cfop": "2202",
        "icms": "T",
        "ipi": 3.0,
        "pis_cofins": 54.0,
        "nat_op_erp": "2202C",
        "cod_completo": "2202T0354",
    },
    {
        "cfop": "2202",
        "icms": "T",
        "ipi": 1.0,
        "pis_cofins": 54.0,
        "nat_op_erp": "2202D",
        "cod_completo": "2202T0154",
    },
    {
        "cfop": "2202",
        "icms": "R",
        "ipi": 1.0,
        "pis_cofins": 54.0,
        "nat_op_erp": "2202E",
        "cod_completo": "2202R0154",
    },
    {
        "cfop": "2202",
        "icms": "T",
        "ipi": 1.0,
        "pis_cofins": 73.0,
        "nat_op_erp": "2202F",
        "cod_completo": "2202T0173",
    },
    {
        "cfop": "2202",
        "icms": "R",
        "ipi": 1.0,
        "pis_cofins": 73.0,
        "nat_op_erp": "2202G",
        "cod_completo": "2202R0173",
    },
    {
        "cfop": "2202",
        "icms": "R",
        "ipi": 1.0,
        "pis_cofins": 70.0,
        "nat_op_erp": "2202H",
        "cod_completo": "2202R0170",
    },
    {
        "cfop": "2202",
        "icms": "T",
        "ipi": 0.0,
        "pis_cofins": 54.0,
        "nat_op_erp": "2202I",
        "cod_completo": "2202T0054",
    },
]


def encontrar_natureza_operacao(
    cfop_origem, uf_emit, uf_dest, forma_obtencao, trib_icms, cst_ipi, cst_pis
):
    # 1. Determina se é operação Interna (1.xxx) ou Interestadual (2.xxx)
    operacao_interna = uf_emit == uf_dest

    if forma_obtencao == "Fabricado":
        cfop_base = "1201" if operacao_interna else "2201"
    else:
        cfop_base = "1202" if operacao_interna else "2202"

    # 2. Busca na matriz de regras do ERP
    for regra in REGRAS_NATUREZA_ERP:
        if (
            regra["cfop"] == cfop_base
            and regra["icms"] == trib_icms
            and regra["ipi"] == float(cst_ipi)
            and regra["pis_cofins"] == float(cst_pis)
        ):
            return {
                "CFOP_Entrada": cfop_base,
                "NAT_OP_ERP": regra["nat_op_erp"],
                "COD_COMPLETO": regra["cod_completo"],
            }

    # Fallback caso não encontre combinação exata de tributação
    return {
        "CFOP_Entrada": cfop_base,
        "NAT_OP_ERP": f"{cfop_base} (Padrão)",
        "COD_COMPLETO": "Não Mapeada",
    }


# Formulário Interativo / Leitor
st.subheader("Simulação para Nota de Origem com CFOP 6102")

col1, col2 = st.columns(2)

with col1:
    uf_cliente = st.selectbox(
        "UF Emitente (Cliente)",
        ["SP", "RJ", "MG", "PR", "SC", "RS"],
        index=0,
    )
    uf_empresa = st.selectbox(
        "UF Destinatário (Sua Empresa)",
        ["SP", "RJ", "MG", "PR", "SC", "RS"],
        index=0,
    )
    cfop_origem = st.text_input("CFOP da Nota de Saída/Cliente", "6102")
    forma_obtencao = st.selectbox(
        "Forma de Obtenção do Item", ["Comprado", "Fabricado"]
    )

with col2:
    trib_icms = st.selectbox(
        "Tributação ICMS (Aba CST ICMS)",
        ["T", "R", "I"],
        help="T = Tributada | R = Reduzida | I = Isenta",
    )
    cst_ipi = st.selectbox(
        "CST IPI Entrada",
        [0.0, 1.0, 3.0],
        help="0 = Com Crédito | 1 = Alíq Zero | 3 = N Tributado",
    )
    cst_pis = st.selectbox(
        "CST PIS/COFINS Entrada",
        [54.0, 70.0, 73.0],
        help="54 = Com Crédito | 70 = Sem Crédito | 73 = Alíq Zero",
    )

if st.button("Buscar Natureza de Operação do ERP"):
    resultado = encontrar_natureza_operacao(
        cfop_origem,
        uf_cliente,
        uf_empresa,
        forma_obtencao,
        trib_icms,
        cst_ipi,
        cst_pis,
    )

    st.success(f"### Natureza de Operação ERP: **{resultado['NAT_OP_ERP']}**")
    st.write(f"**CFOP de Entrada:** {resultado['CFOP_Entrada']}")
    st.write(f"**Código Interno / Mapeamento:** `{resultado['COD_COMPLETO']}`")

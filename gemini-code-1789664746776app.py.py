import pandas as pd
import streamlit as st
import xml.etree.ElementTree as ET

# Configuração da página
st.set_page_config(
    page_title="Assistente de Devoluções - CFOP", page_icon="📦"
)
st.title("📦 Assistente de Devolução de Notas Fiscais")


# Função principal de regra de negócio
def obter_cfop_devolucao(
    cfop_origem, uf_emitente, uf_destinatario, forma_obtencao
):
    operacao_interna = uf_emitente == uf_destinatario
    cfop_resultante = "N/A"
    natureza = "Regra não encontrada para o CFOP de origem"

    # Limpa formatação do CFOP
    cfop_clean = str(cfop_origem).replace(".", "").strip()

    if cfop_clean in ["5101", "6101", "5102", "6102"]:
        if forma_obtencao == "Fabricado":
            cfop_resultante = "1.202" if operacao_interna else "2.202"
            natureza = "Devolução de venda de produção do estabelecimento"
        elif forma_obtencao == "Comprado":
            cfop_resultante = "1.102" if operacao_interna else "2.102"
            natureza = "Devolução de compra para comercialização"

    return {"CFOP_Entrada": cfop_resultante, "Natureza_Operacao": natureza}


# Interface do Usuário
tab1, tab2 = st.tabs(["📄 Processar XML", "🎛️ Teste Manual"])

with tab1:
    st.subheader("Importar XML da Nota Fiscal")
    uploaded_file = st.file_uploader(
        "Arraste ou selecione o arquivo XML da NF-e", type=["xml"]
    )

    if uploaded_file is not None:
        try:
            tree = ET.parse(uploaded_file)
            root = tree.getroot()
            ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

            uf_emit = root.find(".//nfe:emit/nfe:enderEmit/nfe:UF", ns).text
            uf_dest = root.find(".//nfe:dest/nfe:enderDest/nfe:UF", ns).text
            cfop_xml = root.find(".//nfe:det/nfe:prod/nfe:CFOP", ns).text

            st.info(
                f"**UF Origem:** {uf_emit} | **UF Destino:** {uf_dest} | **CFOP XML:** {cfop_xml}"
            )

            forma_obtencao = st.radio(
                "Forma de Obtenção do Produto:",
                ["Fabricado", "Comprado"],
                index=0,
            )

            if st.button("Determinar CFOP de Entrada"):
                res = obter_cfop_devolucao(
                    cfop_xml, uf_emit, uf_dest, forma_obtencao
                )
                st.success(f"**CFOP Recomendado:** {res['CFOP_Entrada']}")
                st.write(
                    f"**Natureza da Operação:** {res['Natureza_Operacao']}"
                )
        except Exception as e:
            st.error(f"Erro ao ler o XML: {e}")

with tab2:
    st.subheader("Simulador de Regra")
    col1, col2 = st.columns(2)

    with col1:
        uf_emit = st.selectbox(
            "UF Emitente (Cliente)", ["SP", "RJ", "MG", "PR", "SC", "RS"]
        )
        uf_dest = st.selectbox("UF Destinatário (Sua Empresa)", ["SP", "RJ", "MG", "PR", "SC", "RS"])
        cfop_orig = st.text_input("CFOP da Nota de Origem", "5102")

    with col2:
        forma_obt = st.selectbox(
            "Forma de Obtenção", ["Fabricado", "Comprado"]
        )

    if st.button("Testar Regra"):
        resultado = obter_cfop_devolucao(
            cfop_orig, uf_emit, uf_dest, forma_obt
        )
        st.metric(label="CFOP de Entrada", value=resultado["CFOP_Entrada"])
        st.info(f"**Natureza da Operação:** {resultado['Natureza_Operacao']}")
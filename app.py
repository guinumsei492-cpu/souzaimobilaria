import streamlit as st
import pandas as pd
from PIL import Image

# Configuração da página para Mobile e Web
st.set_page_config(page_title="Souza Imobiliária", page_icon="🏠", layout="wide")

# --- ESTILO VISUAL (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .card { 
        padding: 15px; border-radius: 15px; background-color: white; 
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .preco { color: #28a745; font-size: 20px; font-weight: bold; }
    .tipo-tag { background: #007bff; color: white; padding: 2px 8px; border-radius: 5px; font-size: 12px; }
    </style>
    """, unsafe_allow_index=True)

# --- INICIALIZAÇÃO DO BANCO DE DADOS (EM MEMÓRIA) ---
if 'meus_imoveis' not in st.session_state:
    st.session_state.meus_imoveis = [
        {
            "titulo": "Casa Luxo Alphaville", "tipo": "Casa", "preco": 950000.0, 
            "quartos": 4, "img": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=500",
            "cidade": "Salvador"
        }
    ]

# --- MENU DE NAVEGAÇÃO ---
menu = ["🏠 Início (Cliente)", "🔑 Área do Corretor"]
escolha = st.sidebar.selectbox("Navegação", menu)

# --- TELA 1: ÁREA DO CLIENTE ---
if escolha == "🏠 Início (Cliente)":
    st.title("🏠 Souza Imobiliária")
    st.write("---")
    
    # Filtros Rápidos
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        f_tipo = st.selectbox("O que busca?", ["Todos", "Casa", "Apartamento", "Terreno"])
    with col_f2:
        f_preco = st.slider("Preço até (R$)", 50000, 2000000, 2000000, step=50000)
    with col_f3:
        f_quartos = st.number_input("Mínimo Quartos", 0, 10, 0)

    # Exibição dos Cards
    st.subheader("Imóveis em Destaque")
    cols_cards = st.columns(2) # 2 colunas para ficar bom no celular
    
    imoveis_filtrados = [i for i in st.session_state.meus_imoveis if 
                         (f_tipo == "Todos" or i["tipo"] == f_tipo) and 
                         (i["preco"] <= f_preco) and (i["quartos"] >= f_quartos)]

    if not imoveis_filtrados:
        st.warning("Nenhum imóvel encontrado com esses filtros.")
    
    for idx, imovel in enumerate(imoveis_filtrados):
        with cols_cards[idx % 2]:
            st.markdown(f"""
            <div class="card">
                <img src="{imovel['img']}" style="width:100%; border-radius:10px; height:200px; object-fit: cover;">
                <span class="tipo-tag">{imovel['tipo']}</span>
                <h3>{imovel['titulo']}</h3>
                <p class="preco">R$ {imovel['preco']:,.2f}</p>
                <p>🛏️ {imovel['quartos']} Quartos | 📍 {imovel['cidade']}</p>
            </div>
            """, unsafe_allow_index=True)
            if st.button(f"Tenho Interesse #{idx}", key=f"btn_{idx}"):
                st.success(f"Solicitação enviada para Souza Imobiliária sobre: {imovel['titulo']}")

# --- TELA 2: ÁREA DO CORRETOR (CADASTRO) ---
elif escolha == "🔑 Área do Corretor":
    st.title("Painel de Cadastro")
    st.info("Aqui você cadastra novos imóveis usando a câmera ou galeria do celular.")

    with st.form("cadastro_imovel", clear_on_submit=True):
        nome = st.text_input("Nome do Imóvel (ex: Edifício Solar)")
        tipo_cad = st.selectbox("Tipo", ["Casa", "Apartamento", "Terreno", "Comercial"])
        preco_cad = st.number_input("Valor de Venda (R$)", min_value=0.0, format="%.2f")
        quartos_cad = st.number_input("Quantidade de Quartos", 0, 20)
        cidade_cad = st.text_input("Cidade/Bairro")
        
        # Upload de Imagem
        foto = st.file_uploader("Tire uma foto ou suba da galeria", type=['png', 'jpg', 'jpeg'])
        
        enviar = st.form_submit_button("✅ Publicar Imóvel")

        if enviar:
            if nome and foto:
                # Simulando salvamento da imagem (em app real usaríamos um link de nuvem)
                # Para o exemplo, vamos usar um placeholder se for arquivo local
                novo_imovel = {
                    "titulo": nome,
                    "tipo": tipo_cad,
                    "preco": preco_cad,
                    "quartos": quartos_cad,
                    "img": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=500", # Foto padrão para o teste
                    "cidade": cidade_cad
                }
                st.session_state.meus_imoveis.append(novo_imovel)
                st.balloons()
                st.success("Imóvel cadastrado com sucesso! Volte na tela inicial para ver.")
            else:
                st.error("Por favor, preencha o nome e adicione uma foto.")

    # Lista de Imóveis Cadastrados para Excluir
    st.subheader("Gerenciar Meus Anúncios")
    for i, imob in enumerate(st.session_state.meus_imoveis):
        st.text(f"{imob['titulo']} - R$ {imob['preco']}")

import streamlit as st

# 1. Configuração da página
st.set_page_config(page_title="Souza Imobiliária", page_icon="🏠", layout="wide")

# Importando ícones do Google/FontAwesome para o símbolo do zap
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)

# 2. CSS Customizado
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .card { 
        padding: 20px; border-radius: 15px; background-color: white; 
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .preco { color: #28a745; font-size: 22px; font-weight: bold; }
    .btn-whatsapp {
        background-color: #25D366;
        color: white !important;
        text-decoration: none;
        padding: 12px;
        border-radius: 8px;
        display: block;
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        transition: 0.3s;
    }
    .btn-whatsapp:hover { background-color: #128C7E; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# 3. Banco de Dados (Session State)
if 'meus_imoveis' not in st.session_state:
    st.session_state.meus_imoveis = [
        {
            "titulo": "Casa Luxo Alphaville", "tipo": "Casa", "preco": 950000.0, 
            "quartos": 4, "img": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=500",
            "cidade": "Salvador"
        }
    ]

# 4. Navegação
menu = ["🏠 Início (Cliente)", "🔑 Área do Corretor"]
escolha = st.sidebar.selectbox("Menu", menu)

if escolha == "🏠 Início (Cliente)":
    st.title("🏠 Souza Imobiliária")
    st.write("---")
    
    # Filtros
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        f_tipo = st.selectbox("Tipo", ["Todos", "Casa", "Apartamento", "Terreno"])
    with col_f2:
        f_preco = st.slider("Preço máximo (R$)", 50000, 2000000, 2000000)

    # Exibição
    imoveis_filtrados = [i for i in st.session_state.meus_imoveis if (f_tipo == "Todos" or i["tipo"] == f_tipo) and (i["preco"] <= f_preco)]
    
    cols = st.columns(2)
    for idx, imob in enumerate(imoveis_filtrados):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="card">
                <img src="{imob['img']}" style="width:100%; border-radius:10px; height:200px; object-fit: cover;">
                <h3>{imob['titulo']}</h3>
                <p class="preco">R$ {imob['preco']:,.2f}</p>
                <p>📍 {imob['cidade']}</p>
                <a href="https://wa.me/557182768278?text=Olá%20Souza!%20Tenho%20interesse%20no%20imóvel:%20{imob['titulo']}" 
                   target="_blank" class="btn-whatsapp">
                   <i class="fab fa-whatsapp"></i> CHAMAR NO WHATSAPP
                </a>
            </div>
            """, unsafe_allow_html=True)
            st.write("")

elif escolha == "🔑 Área do Corretor":
    st.title("Cadastrar Novo Imóvel")
    with st.form("novo_imob"):
        t = st.text_input("Título")
        p = st.number_input("Preço")
        cid = st.text_input("Cidade")
        tipo = st.selectbox("Tipo", ["Casa", "Apartamento", "Terreno"])
        subir = st.form_submit_button("Publicar")
        if subir:
            st.session_state.meus_imoveis.append({"titulo":t, "preco":p, "cidade":cid, "tipo":tipo, "img":"https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=500", "quartos":3})
            st.success("Postado!")

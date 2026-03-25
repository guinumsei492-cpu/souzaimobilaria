import streamlit as st

# 1. Configuração da página
st.set_page_config(page_title="Souza Imobiliária", page_icon="🏠", layout="wide")

# Link para Manifesto PWA e ícones
st.markdown('<link rel="manifest" href="manifest.json">', unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)

# 2. CSS Profissional
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .card { 
        padding: 15px; border-radius: 15px; background-color: white; 
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1); margin-bottom: 10px;
    }
    .preco { color: #28a745; font-size: 22px; font-weight: bold; margin: 5px 0; }
    .btn-whatsapp {
        background-color: #25D366; color: white !important; text-decoration: none;
        padding: 12px; border-radius: 8px; display: block; text-align: center;
        font-weight: bold; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Banco de Dados Temporário (Session State)
if 'meus_imoveis' not in st.session_state:
    st.session_state.meus_imoveis = [
        {
            "id": 1, "titulo": "Casa Luxo Alphaville", "tipo": "Casa", "preco": 950000.0, 
            "cidade": "Salvador", "quartos": 4,
            "fotos": ["https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800"]
        },
        {
            "id": 2, "titulo": "Apartamento Vista Mar", "tipo": "Apartamento", "preco": 450000.0, 
            "cidade": "Lauro de Freitas", "quartos": 2,
            "fotos": ["https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800"]
        }
    ]

# 4. Navegação
menu = ["🏠 Início (Cliente)", "🔑 Área do Corretor"]
escolha = st.sidebar.selectbox("Menu", menu)

if escolha == "🏠 Início (Cliente)":
    st.title("🏠 Souza Imobiliária")
    
    # Filtros
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        f_tipo = st.selectbox("Tipo", ["Todos", "Casa", "Apartamento", "Terreno"])
    with col_f2:
        f_preco = st.slider("Preço Máximo", 50000, 2000000, 2000000)

    st.write("---")

    imoveis_filtrados = [i for i in st.session_state.meus_imoveis if (f_tipo == "Todos" or i["tipo"] == f_tipo) and (i["preco"] <= f_preco)]

    for imob in imoveis_filtrados:
        with st.container():
            col_img, col_info = st.columns([1, 1])
            
            with col_img:
                # Verificação de segurança para a foto
                imagem_exibir = imob["fotos"][0] if imob["fotos"] else "https://via.placeholder.com/800x600?text=Sem+Foto"
                st.image(imagem_exibir, use_container_width=True)
            
            with col_info:
                st.subheader(imob["titulo"])
                st.markdown(f"<p class='preco'>R$ {imob['preco']:,.2f}</p>", unsafe_allow_html=True)
                st.write(f"📍 {imob['cidade']} | 🛏️ {imob['quartos']} Quartos")
                
                if st.button(f"🔍 Ver detalhes e fotos", key=f"det_{imob['id']}"):
                    st.session_state[f"ver_{imob['id']}"] = True

            if st.session_state.get(f"ver_{imob['id']}", False):
                with st.expander(f"Galeria: {imob['titulo']}", expanded=True):
                    if imob["fotos"]:
                        st.image(imob["fotos"], use_container_width=True)
                    
                    link_zap = f"https://wa.me/557182768278?text=Olá%20Souza!%20Interesse:%20{imob['titulo']}"
                    st.markdown(f'<a href="{link_zap}" target="_blank" class="btn-whatsapp">CHAMAR NO ZAP</a>', unsafe_allow_html=True)
                    
                    if st.button("Fechar", key=f"close_{imob['id']}"):
                        st.session_state[f"ver_{imob['id']}"] = False
                        st.rerun()
            st.write("---")

elif escolha == "🔑 Área do Corretor":
    st.title("Cadastrar Imóvel")
    with st.form("novo_imob", clear_on_submit=True):
        t = st.text_input("Título")
        p = st.number_input("Preço", min_value=0.0)
        cid = st.text_input("Cidade")
        tipo = st.selectbox("Tipo", ["Casa", "Apartamento", "Terreno"])
        upload = st.file_uploader("Fotos", accept_multiple_files=True)
        subir = st.form_submit_button("Publicar")
        
        if subir:
            # Se não subir foto, usa uma imagem padrão para não dar erro
            lista_fotos = ["https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=800"]
            
            novo = {
                "id": len(st.session_state.meus_imoveis) + 1,
                "titulo": t, "tipo": tipo, "preco": p, "cidade": cid, "quartos": 3,
                "fotos": lista_fotos
            }
            st.session_state.meus_imoveis.append(novo)
            st.success("Imóvel cadastrado! Vá ao Início para ver.")

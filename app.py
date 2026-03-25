import streamlit as st

# 1. Configuração da página (DEVE SER A PRIMEIRA LINHA)
st.set_page_config(page_title="Souza Imobiliária", page_icon="🏠", layout="wide")

# Link para Manifesto PWA e Ícones
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
    .img-vitrine { width: 100%; border-radius: 10px; height: 200px; object-fit: cover; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# 3. Banco de Dados Temporário
if 'meus_imoveis' not in st.session_state:
    st.session_state.meus_imoveis = [
        {
            "id": 1, "titulo": "Casa Luxo Alphaville", "tipo": "Casa", "preco": 950000.0, 
            "cidade": "Salvador", "quartos": 4,
            "fotos": [
                "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800",
                "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800",
                "https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800"
            ]
        },
        {
            "id": 2, "titulo": "Apartamento Vista Mar", "tipo": "Apartamento", "preco": 450000.0, 
            "cidade": "Lauro de Freitas", "quartos": 2,
            "fotos": [
                "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800",
                "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800"
            ]
        }
    ]

# 4. Interface
menu = ["🏠 Início (Cliente)", "🔑 Área do Corretor"]
escolha = st.sidebar.selectbox("Menu de Navegação", menu)

if escolha == "🏠 Início (Cliente)":
    st.title("🏠 Souza Imobiliária")
    
    # Filtros Rápidos
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        f_tipo = st.selectbox("O que você procura?", ["Todos", "Casa", "Apartamento", "Terreno"])
    with col_f2:
        f_preco = st.slider("Preço Máximo", 50000, 2000000, 2000000)

    st.write("---")

    imoveis_filtrados = [i for i in st.session_state.meus_imoveis if (f_tipo == "Todos" or i["tipo"] == f_tipo) and (i["preco"] <= f_preco)]

    # Grid de Imóveis
    for imob in imoveis_filtrados:
        with st.container():
            col_img, col_info = st.columns([1, 1])
            
            with col_img:
                st.image(imob["fotos"][0], use_container_width=True, caption="Toque para ver mais fotos abaixo")
            
            with col_info:
                st.subheader(imob["titulo"])
                st.markdown(f"<p class='preco'>R$ {imob['preco']:,.2f}</p>", unsafe_allow_html=True)
                st.write(f"📍 {imob['cidade']} | 🛏️ {imob['quartos']} Quartos")
                
                # Botão Ver Fotos
                if st.button(f"🔍 Ver detalhes e fotos", key=f"det_{imob['id']}"):
                    st.session_state[f"ver_{imob['id']}"] = True

            # Galeria de Fotos (Aparece ao clicar)
            if st.session_state.get(f"ver_{imob['id']}", False):
                with st.expander(f"Galeria de Fotos: {imob['titulo']}", expanded=True):
                    cols_fotos = st.columns(len(imob["fotos"]))
                    for i, link_foto in enumerate(imob["fotos"]):
                        with cols_fotos[i]:
                            st.image(link_foto, use_container_width=True)
                    
                    # Botão WhatsApp dentro dos detalhes
                    link_zap = f"https://wa.me/557182768278?text=Olá%20Souza!%20Quero%20saber%20mais%20sobre:%20{imob['titulo']}"
                    st.markdown(f'<a href="{link_zap}" target="_blank" class="btn-whatsapp"><i class="fab fa-whatsapp"></i> ME INTERESSEI! CHAMAR NO ZAP</a>', unsafe_allow_html=True)
                    
                    if st.button("Fechar Galeria", key=f"close_{imob['id']}"):
                        st.session_state[f"ver_{imob['id']}"] = False
                        st.rerun()
            st.write("---")

elif escolha == "🔑 Área do Corretor":
    st.title("Painel do Corretor")
    st.warning("As fotos enviadas aqui ficam salvas apenas nesta sessão. Para fixar, use um banco de dados.")

    with st.form("form_cadastro"):
        nome = st.text_input("Nome do Imóvel")
        preco = st.number_input("Preço", min_value=0.0)
        cidade = st.text_input("Bairro/Cidade")
        tipo = st.selectbox("Categoria", ["Casa", "Apartamento", "Terreno"])
        upload = st.file_uploader("Selecione as fotos (Câmera ou Galeria)", accept_multiple_files=True)
        
        btn = st.form_submit_button("✅ Publicar no App")
        
        if btn:
            if nome and upload:
                # Aqui simplificamos usando a primeira foto enviada ou um placeholder
                novo = {
                    "id": len(st.session_state.meus_imoveis) + 1,
                    "titulo": nome, "tipo": tipo, "preco": preco, "cidade": cidade, "quartos": 3,
                    "fotos": ["https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=800"]
                }
                st.session_state.meus_imoveis.append(novo)
                st.success("Imóvel cadastrado com sucesso!")
            else:
                st.error("Preencha o nome e envie pelo menos uma foto.")

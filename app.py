import streamlit as st
import os # Para construir caminhos de arquivo de forma robusta
from PIL import Image # Biblioteca Pillow para carregar a imagem do ícone



# para lembrarem os ícones, usei os emojis
# icon %F0%9F%93%8C = "📌"
# icon %F0%9F%93%8A = "📊"
# icon %F0%9F%93%88 = "📈"


# --- CONFIGURAÇÃO DA PÁGINA (DEVE SER A PRIMEIRA CHAMADA DO STREAMLIT) ---
# Caminho para a pasta de assets

# Função para carregar o conteúdo de um arquivo CSS
# Essa função lê o arquivo CSS e retorna seu conteúdo como uma string.
# O parâmetro css_file_path é o caminho para o arquivo CSS.
# O arquivo CSS deve estar no mesmo diretório que o script app.py
# ou em um subdiretório chamado assets.
# O caminho completo para o arquivo CSS é construído usando os.path.join
# e os.path.dirname(__file__) para garantir que o caminho funcione
# corretamente em diferentes sistemas operacionais.
# O arquivo CSS deve ser lido como texto, então usamos open() com o modo 'r'.
def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return f.read()

# Definindo o diretório de ativos (assets)
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
# Definindo o caminho para o ícone do aplicativo
ICON_PATH = os.path.join(ASSETS_DIR, "icon_nai_cz.png")


# Tenta carregar o ícone. Se não encontrar, usa um emoji como fallback.
try:
    page_icon_img = Image.open(ICON_PATH)
except FileNotFoundError:
    page_icon_img = "💡" # Um emoji como fallback se a imagem não for encontrada
    st.warning(f"Ícone não encontrado em {ICON_PATH}. Usando emoji padrão.")

# Configuração da página
# Aqui você pode definir o título, ícone, layout e estado inicial da barra lateral
# O título e o ícone aparecem na aba do navegador
# O layout pode ser "centered" ou "wide"
# O estado inicial da barra lateral pode ser "auto", "expanded" ou "collapsed"
# O layout "wide" faz com que o conteúdo ocupe toda a largura da tela
# O layout "centered" centraliza o conteúdo na tela
st.set_page_config(
    page_title="Meu Site Padrão",  # Título que aparece na aba do navegador
    page_icon=page_icon_img,       # Pode ser um caminho para uma imagem, um emoji, ou um objeto Image da Pillow
    layout="wide",                 # Outras opções: "centered"
    initial_sidebar_state="expanded" # Outras opções: "auto", "collapsed"
)


# Carregar e aplicar o CSS global (style.css)
# Este CSS será aplicado sempre, independente do tema
global_css_path = os.path.join(ASSETS_DIR, "style.css")
if os.path.exists(global_css_path):
    global_css = load_css_file(global_css_path)
    st.markdown(f"<style>{global_css}</style>", unsafe_allow_html=True)
else:
    st.warning(f"Arquivo CSS global não encontrado: {global_css_path}")


# Função para aplicar o CSS do tema escolhido
def apply_theme_css(theme_name):
    css_file_name = ""
    if theme_name == "Escuro":
        css_file_name = "dark_theme.css"
    elif theme_name == "Claro":
        css_file_name = "light_theme.css"
    # Adicione mais temas se necessário

    if css_file_name:
        theme_css_path = os.path.join(ASSETS_DIR, css_file_name)
        if os.path.exists(theme_css_path):
            theme_css = load_css_file(theme_css_path)
            # Usamos uma chave única para o st.markdown do tema para que ele seja substituído
            # ao invés de acumulado quando o tema muda.
            st.markdown(f"<style id='theme-style'>{theme_css}</style>", unsafe_allow_html=True)
        else:
            st.warning(f"Arquivo CSS do tema '{theme_name}' não encontrado: {theme_css_path}")

# --- GERENCIAMENTO DO ESTADO DO TEMA (SESSION STATE) ---

# Inicializar o session_state para o tema
if 'selected_theme' not in st.session_state:
    # O config.toml ainda define o tema base inicial que o Streamlit usa para seus componentes.
    # Nosso CSS customizado vai sobrescrever/complementar isso.
    # Se você tem `base = "dark"` no config.toml, seu tema inicial aqui deve ser "Escuro".
    st.session_state.selected_theme = "Claro" # Ou "Escuro" se for seu padrão

# Aplicar o CSS do tema atual (inicial ou após mudança)
apply_theme_css(st.session_state.selected_theme)


# --- INTERFACE DO USUÁRIO ---

#### experimental, Michel 28/04/2025
# não gostei da experiencia, vou deixar para futuro 
# PAGES = {
#     "📊 Dashboard": Dashboard.show_page,
#     "📈 Análise Detalhada": Analise_Detalhada.show_page,
# }
####

# Botão de escolha de tema na barra lateral
st.sidebar.title("🎨 Configurações")
# Adiciona uma opção de tema na barra lateral
# O índice atual do tema é obtido para manter a seleção correta
# entre as recargas da página.
# O índice é baseado na lista de temas disponíveis
# Aqui, estamos assumindo que os temas são "Claro" e "Escuro".
# Você pode adicionar mais temas à lista se necessário.
# A lista de temas deve ser a mesma que a usada na função apply_theme_css (gerenciamento do tema).
# para garantir que o índice corresponda corretamente.
theme_options = ["Claro", "Escuro"]
# Se o tema atual não estiver na lista, use o primeiro tema como padrão
if st.session_state.selected_theme not in theme_options:
    st.session_state.selected_theme = theme_options[0]
# Obtemos o índice do tema atual na lista de opções
# Isso é necessário para manter a seleção correta entre as recargas da página.
current_theme_index = theme_options.index(st.session_state.selected_theme)


# Adiciona um seletor de tema na barra lateral
# O índice atual do tema é usado para manter a seleção correta
# entre as recargas da página.
# O key é importante para que o Streamlit saiba que este widget é único
# e deve ser mantido no session_state.
# O key também é importante para evitar conflitos com outros widgets
# que possam ter o mesmo nome.
chosen_theme = st.sidebar.radio(
    "Escolha o tema:",
    options=theme_options,
    index=current_theme_index,
    key="theme_selector" # Uma chave para o widget
)

# adicionar ao slidebar um novo menu
st.sidebar.write("---")
st.sidebar.header("Menu de Navegação")
# Adiciona opções de navegação na barra lateral
# Aqui você pode adicionar links ou botões para navegar entre diferentes partes do seu app
# ou para outras páginas do seu app.
# Exemplo de opções de navegação
# Você pode usar st.sidebar.button ou st.sidebar.selectbox
# para criar botões ou caixas de seleção para navegação.
st.sidebar.write("Escolha uma opção:")

########################################################3
# estou com problemas para adicionar os botões de navegação
# Link para outra página ou seção do app
# Aqui você pode adicionar links ou botões para navegar entre diferentes partes do seu app

st.sidebar.write("1. Opção 1")
st.sidebar.write("2. Opção 2")
st.sidebar.write("3. Opção 3")

#############################################################

# Adiciona um botão para sair do app
st.sidebar.write("---")
st.sidebar.button("Sair", on_click=st.stop) # Para sair do app
# Adiciona um botão para voltar para a página inicial
st.sidebar.button("Voltar", on_click=st.stop) # Para voltar para a página inicial
# Adiciona um botão para abrir o menu de ajuda
st.sidebar.button("Ajuda", on_click=st.stop) # Para abrir o menu de ajuda

# Se a escolha do tema mudou, atualiza o session_state e re-executa o app
if chosen_theme != st.session_state.selected_theme:
    st.session_state.selected_theme = chosen_theme
    st.rerun() # Essencial para que o novo CSS seja aplicado


# Resto do seu aplicativo Streamlit
st.title("App Modelo com Temas CSS Externos")
# printa na tela com qual tema estamos
st.write(f"Tema atual: {st.session_state.selected_theme}")

st.button("Botão Primário")
st.text_input("Campo de Texto")
st.selectbox("Caixa de Seleção", ["Opção 1", "Opção 2"])
st.slider("Slider", 0, 100, 50)
st.date_input("Seletor de Data")

st.write("---")
st.write("vamos iniciar nessa base...")
# Estudo de Caso 2 - Lógica de Programação - Fundamentos de Linguagem Python Para Construção de Game

# Importa a biblioteca Streamlit
import random
import streamlit as st

# --- Configuração da Página ---
st.set_page_config(page_title="Jokenpô", page_icon="🎮", layout="centered")

# --- 1. Apresentação e Regras --

# Usamos st.title() e st.write() para exibir o cabeçalho na interface do Streamlit.
st.title("🎮 Jogo Pedra, Papel e Tesoura 🎮")

# Adicionamos um seletor de modo de jogo
modo_de_jogo = st.radio(
    "Escolha o modo de jogo:",
    ("Jogador vs. Computador", "Jogador vs. Jogador"),
    horizontal=True,
)

# --- Funções de Controle do Jogo ---
def reiniciar_jogo():
    """Reseta o placar e o estado da última jogada."""
    st.session_state.placar_p1 = 0
    st.session_state.placar_oponente = 0
    st.session_state.resultado = (None, None)
    st.session_state.ultima_jogada_p1 = None
    st.session_state.ultima_jogada_oponente = None

# Inicializa o estado do jogo na primeira execução
if 'placar_p1' not in st.session_state:
    reiniciar_jogo()
# Define o nome do oponente para o placar
oponente_nome = "Computador" if modo_de_jogo == "Jogador vs. Computador" else "Jogador 2"

st.divider()

# Usamos uma tupla para armazenar as opções válidas.
# Tuplas são boas aqui porque as opções do jogo não mudam (são imutáveis).
opcoes_validas = ("Pedra", "Papel", "Tesoura")

# Dicionário com as URLs das imagens para cada jogada
imagens = {
    "Pedra": "https://em-content.zobj.net/source/microsoft-teams/363/rock_1faa8.png", # 🪨
    "Papel": "https://em-content.zobj.net/source/microsoft-teams/363/page-with-curl_1f4c3.png", # 📃
    "Tesoura": "https://em-content.zobj.net/source/microsoft-teams/363/scissors_2702-fe0f.png" # ✂️
}

# --- Placar ---
col_placar1, col_placar2 = st.columns(2)
with col_placar1:
    st.metric("🏆 Placar Jogador 1", f"{st.session_state.placar_p1}")
with col_placar2:
    st.metric(f"🏆 Placar {oponente_nome}", f"{st.session_state.placar_oponente}")

# Botão para reiniciar o placar
if st.button("Reiniciar Placar 🔄"):
    reiniciar_jogo()
    st.rerun()

st.divider()

# --- 2. Coleta dos Dados de Entrada ---

# A interface se adapta com base no modo de jogo escolhido
if modo_de_jogo == "Jogador vs. Computador":
    st.header("Sua vez de jogar")
    jogada_jogador1 = st.selectbox("Escolha sua jogada:", opcoes_validas, key='p1_vs_cpu', index=None, placeholder="Selecione sua jogada")
    oponente = oponente_nome
else: # Modo "Jogador vs. Jogador"
    col1, col2 = st.columns(2)
    with col1:
        st.header("Jogador 1")
        jogada_jogador1 = st.selectbox("Escolha sua jogada:", opcoes_validas, key='p1_pvp', index=None, placeholder="Selecione sua jogada")
    with col2:
        st.header(oponente_nome)
        jogada_jogador2 = st.selectbox("Escolha sua jogada:", opcoes_validas, key='p2_pvp', index=None, placeholder="Selecione sua jogada")
    oponente = oponente_nome

# --- 3. Lógica do Jogo e Resultado ---

# Criamos um botão para iniciar a verificação do resultado.
if st.button("Jogar!"):
    # Determina a jogada do oponente
    if modo_de_jogo == "Jogador vs. Computador":
        jogada_oponente = random.choice(opcoes_validas) if jogada_jogador1 else None
    else:
        jogada_oponente = jogada_jogador2

    # Validação e execução da lógica do jogo
    if jogada_jogador1 and jogada_oponente:
        st.session_state.ultima_jogada_p1 = jogada_jogador1
        st.session_state.ultima_jogada_oponente = jogada_oponente
        # Caso 1: Empate
        if jogada_jogador1 == jogada_oponente:
            st.session_state.resultado = ("warning", "### Resultado: 🤝 É um empate!")

        # Caso 2: Jogador 1 vence
        elif (jogada_jogador1 == "Pedra" and jogada_oponente == "Tesoura") or \
             (jogada_jogador1 == "Tesoura" and jogada_oponente == "Papel") or \
             (jogada_jogador1 == "Papel" and jogada_oponente == "Pedra"):
            st.session_state.placar_p1 += 1
            st.session_state.resultado = ("success", "### Resultado: 🏆 Jogador 1 venceu! Parabéns!")

        # Caso 3: Oponente vence
        else:
            st.session_state.placar_oponente += 1
            st.session_state.resultado = ("error", f"### Resultado: 🤖 {oponente} venceu! Tente novamente.")
        st.rerun()
    else:
        st.warning("Ambos os jogadores precisam fazer uma jogada antes de clicar em 'Jogar!'")

# Exibe o resultado da rodada anterior, se houver
tipo_msg, texto_msg = st.session_state.resultado
if tipo_msg == "success": st.success(texto_msg)
elif tipo_msg == "warning": st.warning(texto_msg)
elif tipo_msg == "error": st.error(texto_msg)

# --- Exibição da Rodada Anterior ---
if st.session_state.ultima_jogada_p1:
    st.divider()
    # Exibição visual das jogadas com um "VS" no meio
    col_p1, col_vs, col_oponente = st.columns([2, 1, 2])
    with col_p1:
        st.subheader("Jogador 1")
        st.image(imagens[st.session_state.ultima_jogada_p1], width=150)
        st.info(f"Escolheu: **{st.session_state.ultima_jogada_p1.capitalize()}**")

    with col_vs:
        st.header("VS")

    with col_oponente:
        st.subheader(oponente_nome)
        st.image(imagens[st.session_state.ultima_jogada_oponente], width=150)
        st.info(f"Escolheu: **{st.session_state.ultima_jogada_oponente.capitalize()}**")
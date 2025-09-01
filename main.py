import streamlit as st
import pandas as pd
import os
import re

# Arquivos Excel
ARQUIVO_MUSICAS = "REPERTORIO.xlsx"   # Sua lista de músicas
ARQUIVO_VOTOS = "votos.xlsx"       # Onde os votos ficarão salvos

# Carregar lista de músicas
df = pd.read_excel(ARQUIVO_MUSICAS)
musicas = df["Música"].tolist()  # Coluna deve se chamar "Música"

# Se não existir o arquivo de votos, cria um novo
if not os.path.exists(ARQUIVO_VOTOS):
    df_votos = pd.DataFrame(columns=["Email", "Música"])
    df_votos.to_excel(ARQUIVO_VOTOS, index=False)

# Carregar votos existentes
df_votos = pd.read_excel(ARQUIVO_VOTOS)

st.title("🎶 Votação de Músicas - " \
"RC LOUVOR")

# Identificação por e-mail
email = st.text_input("Digite seu e-mail para votar:")

def validar_email(email):
    """Valida formato simples de e-mail"""
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(padrao, email) is not None

if email:
    if not validar_email(email):
        st.error("❌ E-mail inválido. Digite um e-mail válido (ex: nome@dominio.com).")
    elif email in df_votos["Email"].values:
        st.warning("⚠️ Este e-mail já votou! Cada pessoa só pode votar uma vez.")
    else:
        escolhas = st.multiselect("Escolha até 20 músicas p/ EXCLUIR do repertório:", musicas, max_selections=20)

        if st.button("Votar"):
            if escolhas:
                novos_votos = pd.DataFrame({"Email": [email]*len(escolhas), "Música": escolhas})
                df_votos = pd.concat([df_votos, novos_votos], ignore_index=True)
                df_votos.to_excel(ARQUIVO_VOTOS, index=False)
                st.success("✅ Seu voto foi registrado com sucesso!")
            else:
                st.warning("⚠️ Você precisa selecionar pelo menos 1 música.")
else:
    st.info("Por favor, insira seu e-mail para votar.")

# Exibe ranking
st.subheader("📊 Ranking de músicas")
if not df_votos.empty:
    ranking = df_votos["Música"].value_counts().reset_index()
    ranking.columns = ["Música", "Votos"]

    st.table(ranking)
    st.bar_chart(ranking.set_index("Música"))

    # Botão para exportar ranking em Excel
    st.subheader("💾 Exportar ranking")
    if st.button("Exportar ranking para Excel"):
        ranking.to_excel("ranking_final.xlsx", index=False)
        st.success("✅ Ranking exportado com sucesso! Arquivo 'ranking_final.xlsx' criado.")
else:
    st.write("Nenhum voto registrado ainda.")

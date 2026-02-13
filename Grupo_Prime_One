import streamlit as st
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configurações do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets", 
         "https://www.googleapis.com/auth/drive"]
# Substitua pelo caminho do seu arquivo JSON
creds = ServiceAccountCredentials.from_json_keyfile_name('caminho/para/sua-chave.json', scope)
client = gspread.authorize(creds)
sheet = client.open('nome-da-sua-planilha').sheet1

# Conexão ao banco SQLite
conn = sqlite3.connect('chatbots.db')
c = conn.cursor()

# Criação de tabelas (se não existirem)
c.execute('''
    CREATE TABLE IF NOT EXISTS empresas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS fluxos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empresa_id INTEGER,
        pergunta TEXT,
        resposta TEXT,
        FOREIGN KEY (empresa_id) REFERENCES empresas(id)
    )
''')
conn.commit()

# Interface Streamlit
st.title("Chatbot para Múltiplas Empresas")

menu = st.sidebar.selectbox("Menu", ["Cadastro de Empresa", "Administração de Fluxos"])

if menu == "Cadastro de Empresa":
    st.subheader("Cadastrar Empresa")
    nome_empresa = st.text_input("Nome da empresa")

    if st.button("Cadastrar"):
        if nome_empresa:
            c.execute('INSERT INTO empresas (nome) VALUES (?)', (nome_empresa,))
            conn.commit()
            st.success("Empresa cadastrada com sucesso!")
        else:
            st.error("Insira um nome para a empresa")

elif menu == "Administração de Fluxos":
    st.subheader("Fluxos por Empresa")
    empresa_selecionada = st.selectbox("Selecione a empresa", 
        options=[empresa[1] for empresa in c.execute('SELECT id, nome FROM empresas').fetchall()])

    if empresa_selecionada:
        empresa_id = c.execute('SELECT id FROM empresas WHERE nome = ?', (empresa_selecionada,)).fetchone()[0]
        fluxos = c.execute('SELECT pergunta, resposta FROM fluxos WHERE empresa_id = ?', (empresa_id,)).fetchall()
        
        st.write("Fluxos desta empresa:")
        for f in fluxos:
            st.write(f"Pergunta: {f[0]} - Resposta: {f[1]}")

        # Aqui você pode adicionar mais funcionalidades, como criar ou editar fluxos

# Envio de dados ao Google Sheets (opcional)
if st.button("Enviar dados para Google Sheets"):
    # Exemplo: você ajusta aqui com os dados do cliente
    sheet.append_row(["Cliente A", "São Paulo", "Contrato"])  # Ajuste os campos conforme sua necessidade
    st.success("Dados enviados para o Google Sheets com sucesso!")

conn.close()

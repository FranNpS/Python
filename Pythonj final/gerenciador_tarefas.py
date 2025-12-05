import streamlit as st
import json
import os
from datetime import datetime
from typing import List, Dict


st.set_page_config(
    page_title="Gerenciador de Tarefas",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)


st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Garantir que o botão de toggle do sidebar SEMPRE fique visível e acessível */
    button[kind="header"],
    button[title="View sidebar"],
    button[title="Close sidebar"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999 !important;
    }
    
    /* Garantir que o sidebar possa ser visto */
    [data-testid="stSidebar"] {
        visibility: visible !important;
    }
    
    /* Garantir que cores se adaptem ao tema */
    .stMarkdown p {
        color: inherit;
    }
    </style>
    """, unsafe_allow_html=True)


DATA_FILE = "tarefas.json"

def carregar_tarefas() -> List[Dict]:
    """Carrega tarefas do arquivo JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def salvar_tarefas(tarefas: List[Dict]):
    """Salva tarefas no arquivo JSON"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(tarefas, f, ensure_ascii=False, indent=2)
    except IOError:
        st.error("Erro ao salvar tarefas!")

def inicializar_tarefas():
    """Inicializa a lista de tarefas no session state"""
    if 'tarefas' not in st.session_state:
        st.session_state.tarefas = carregar_tarefas()
    if 'contador_id' not in st.session_state:
        if st.session_state.tarefas:
            st.session_state.contador_id = max([t['id'] for t in st.session_state.tarefas]) + 1
        else:
            st.session_state.contador_id = 1

def adicionar_tarefa(descricao: str, prioridade: str, categoria: str):
    """Adiciona uma nova tarefa"""
    if descricao.strip():
        nova_tarefa = {
            'id': st.session_state.contador_id,
            'descricao': descricao.strip(),
            'prioridade': prioridade,
            'categoria': categoria if categoria else "Sem categoria",
            'concluida': False,
            'data_criacao': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'data_conclusao': None
        }
        st.session_state.tarefas.append(nova_tarefa)
        st.session_state.contador_id += 1
        salvar_tarefas(st.session_state.tarefas)
        return True
    return False

def remover_tarefa(tarefa_id: int):
    """Remove uma tarefa"""
    st.session_state.tarefas = [t for t in st.session_state.tarefas if t['id'] != tarefa_id]
    salvar_tarefas(st.session_state.tarefas)

def alternar_conclusao(tarefa_id: int):
    """Alterna o status de conclusão de uma tarefa"""
    for tarefa in st.session_state.tarefas:
        if tarefa['id'] == tarefa_id:
            tarefa['concluida'] = not tarefa['concluida']
            if tarefa['concluida']:
                tarefa['data_conclusao'] = datetime.now().strftime("%d/%m/%Y %H:%M")
            else:
                tarefa['data_conclusao'] = None
            break
    salvar_tarefas(st.session_state.tarefas)

def obter_cor_prioridade(prioridade: str) -> str:
    """Retorna a cor correspondente à prioridade"""
    cores = {
        'Alta': '🔴',
        'Média': '🟡',
        'Baixa': '🟢'
    }
    return cores.get(prioridade, '⚪')

inicializar_tarefas()

# Título principal
st.title("✅ Gerenciador de Tarefas")

# Formulário para criar tarefas diretamente na página principal
with st.expander("➕ Criar Nova Tarefa", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        nova_descricao = st.text_area("Descrição da tarefa", height=100, placeholder="Digite a descrição da tarefa...", key="nova_descricao")
    with col2:
        nova_prioridade = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"], index=1, key="nova_prioridade")
        nova_categoria = st.text_input("Categoria", placeholder="Ex: Trabalho", key="nova_categoria")
    
    if st.button("➕ Adicionar Tarefa", type="primary", use_container_width=True):
        if adicionar_tarefa(nova_descricao, nova_prioridade, nova_categoria):
            st.success("Tarefa adicionada com sucesso! ✅")
            st.rerun()
        else:
            st.warning("Por favor, digite uma descrição para a tarefa.")

st.markdown("---")


with st.sidebar:
    st.header("➕ Nova Tarefa")
    
    descricao = st.text_area("Descrição da tarefa", height=100, placeholder="Digite a descrição da tarefa...")
    
    col1, col2 = st.columns(2)
    with col1:
        prioridade = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"], index=1)
    with col2:
        categoria = st.text_input("Categoria", placeholder="Ex: Trabalho")
    
    if st.button("Adicionar Tarefa", type="primary", use_container_width=True):
        if adicionar_tarefa(descricao, prioridade, categoria):
            st.success("Tarefa adicionada com sucesso! ✅")
            st.rerun()
        else:
            st.warning("Por favor, digite uma descrição para a tarefa.")
    
    st.markdown("---")
    

    st.header("📊 Estatísticas")
    total = len(st.session_state.tarefas)
    concluidas = sum(1 for t in st.session_state.tarefas if t['concluida'])
    pendentes = total - concluidas
    
    st.metric("Total de Tarefas", total)
    st.metric("Concluídas", concluidas)
    st.metric("Pendentes", pendentes)
    
    if total > 0:
        percentual = (concluidas / total) * 100
        st.progress(percentual / 100)
        st.caption(f"{percentual:.1f}% concluído")


col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    filtro_status = st.selectbox(
        "Filtrar por status",
        ["Todas", "Pendentes", "Concluídas"],
        key="filtro_status"
    )
with col2:
    filtro_prioridade = st.selectbox(
        "Filtrar por prioridade",
        ["Todas", "Alta", "Média", "Baixa"],
        key="filtro_prioridade"
    )
with col3:
    if st.button("🗑️ Limpar Concluídas", use_container_width=True):
        tarefas_antes = len(st.session_state.tarefas)
        st.session_state.tarefas = [t for t in st.session_state.tarefas if not t['concluida']]
        salvar_tarefas(st.session_state.tarefas)
        removidas = tarefas_antes - len(st.session_state.tarefas)
        if removidas > 0:
            st.success(f"{removidas} tarefa(s) removida(s)!")
            st.rerun()


tarefas_filtradas = st.session_state.tarefas.copy()

if filtro_status == "Pendentes":
    tarefas_filtradas = [t for t in tarefas_filtradas if not t['concluida']]
elif filtro_status == "Concluídas":
    tarefas_filtradas = [t for t in tarefas_filtradas if t['concluida']]

if filtro_prioridade != "Todas":
    tarefas_filtradas = [t for t in tarefas_filtradas if t['prioridade'] == filtro_prioridade]

def ordenar_tarefas(tarefa):
    prioridade_ordem = {"Alta": 1, "Média": 2, "Baixa": 3}
    return (tarefa['concluida'], prioridade_ordem.get(tarefa['prioridade'], 4))

tarefas_filtradas.sort(key=ordenar_tarefas)


st.markdown("---")

if not tarefas_filtradas:
    st.info("📝 Nenhuma tarefa encontrada. Adicione uma nova tarefa usando o menu lateral!")
else:
    st.subheader(f"📋 Lista de Tarefas ({len(tarefas_filtradas)})")
    
    for tarefa in tarefas_filtradas:
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 6, 1, 1])
            
            with col1:
                status_icon = "✅" if tarefa['concluida'] else "⏳"
                st.markdown(f"### {status_icon}")
            
            with col2:
                
                estilo_texto = "text-decoration: line-through; opacity: 0.6;" if tarefa['concluida'] else ""
                st.markdown(f"""
                <div style="{estilo_texto}">
                    <h4>{tarefa['descricao']}</h4>
                    <p style="opacity: 0.7; font-size: 0.9em;">
                        📁 {tarefa['categoria']} | 
                        {obter_cor_prioridade(tarefa['prioridade'])} {tarefa['prioridade']} | 
                        📅 Criada em: {tarefa['data_criacao']}
                        {f" | ✅ Concluída em: {tarefa['data_conclusao']}" if tarefa['concluida'] else ""}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                label_botao = "Desfazer" if tarefa['concluida'] else "Concluir"
                if st.button(label_botao, key=f"toggle_{tarefa['id']}", use_container_width=True):
                    alternar_conclusao(tarefa['id'])
                    st.rerun()
            
            with col4:
                if st.button("🗑️", key=f"delete_{tarefa['id']}", use_container_width=True):
                    remover_tarefa(tarefa['id'])
                    st.rerun()
            
            st.markdown("---")


st.markdown("---")
st.caption("💡 Dica: Use os filtros para organizar suas tarefas e mantenha o foco nas prioridades!")


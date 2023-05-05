import os
import streamlit as st
from streamlit_chat import message
from aprender   import ai_aprender
from conversar  import setup, chat

# Define as variaveis de sessao persistencia
if 'base' not in st.session_state:
    st.session_state['base'] = ''

if 'aprendido' not in st.session_state:
    st.session_state['aprendido'] = False

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'stored_session' not in st.session_state:
    st.session_state['stored_session'] = []

TITLE = "Chat GPT"
st.set_page_config(page_title=TITLE, page_icon=":robot:")
st.header(TITLE)


openai_api_key = st.sidebar.text_input("API-Key", type="password")
model = st.sidebar.selectbox(
    'Selecione o modelo:',
    ("gpt-3.5-turbo", "GPT-4")
)

def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state["generated"])-1,-1,-1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])

    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []

tab1, tab2 = st.tabs(["Conversar", ""])
# st.sidebar.button("Novo Chat", on_click=new_chat, type='primary')
keys = st.session_state.keys()

# Tabela com o formulario para aprender um assunto
# with tab1:
#     # Obtem o nome da base de dados (a ser salvo)
#     def get_base():
#             input_text = st.text_input(label="Nome Base", label_visibility='collapsed',
#                                     placeholder="Base de dados...", key="base_input")
#             return input_text
#     st.session_state['base'] = get_base()
        
#     # Escolha dos PDF que deve fazer parte do processo de treino
#     uploaded_files = st.file_uploader("Escolha seus PDFs", type=['pdf'], accept_multiple_files=True)

#     # Funcao para iniciar o aprendizado do conteudo
#     def aprender():
#         with st.spinner('Aprendendo...'):
#             st.session_state['aprendido'] = ai_aprender(
#                 st.session_state['base'],
#                 uploaded_files,
#             )
#     if st.session_state['base']:
#         st.button("*Aprender*", type='secondary', help="Aqui comeco a aprender os conteudos.",
#                 on_click=aprender
#         )

# Tabela para conversar com um assunto aprendido
with tab1:
    st.markdown("### Conversar:")

    if  openai_api_key:
        # Selecao so aprendizados existente (nome da colection no chomadb)
        option = st.selectbox(
            'Qual aprendizado gostaria de utilizar?',
            os.listdir('./db/chroma')
        )

        if option:

            # Objeto de conversa para utilizar no chat
            qa = setup(option, model, openai_api_key)

            # Mostra o resumo obtido no treinamento sobre o conteudo
            f = open('./resumos/'+ option +'.txt', 'r', encoding="utf8")
            st.write(f.read())
            
            # Entradas de texto do usuario
            def get_text():
                input_text = st.text_input("U Mano: ","", key="input")
                return input_text 
            user_input = get_text()
            
            if user_input:
                # Obtem resposta do modelo
                try:
                    output = chat(qa, user_input)
                
                    # Salvar o retorno no array de historico da conversa
                    st.session_state.past.append(user_input)
                    st.session_state.generated.append(output)
                except Exception as e:
                    st.error("Ocorreu algum com a chave da api!", icon="🚨")
            
            # Mostra o chat
            with st.expander("Histórico de Conversa"):
                if st.session_state['generated']:
                    for i in range(len(st.session_state['generated'])-1, -1, -1):
                        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                        message(st.session_state["generated"][i], key=str(i))
    
    else:
        st.error("Nenhuma chave encontrada!")


import streamlit as st

class ExcelValidadorUI:
    def __init__(self):
        self.set_page_config()
        self.display_header()

    def set_page_config(self):
        st.set_page_config(
            page_title="Validador de Schemas Excel",
            page_icon="resources/JP Logo.png",
            layout="wide"
        )
        st.title("Validador de Schemas Excel")

    def display_header(self):
        st.title("Insira o seu excel para validação")

    def upload_file(self):
        return st.file_uploader("Carregue seu arquivo Excel/CSV aqui", type=["xlsx", "csv"])
    
    def display_results(self, result, error):
        if error:
            # st.error(f"Erro na validação: {error}")
            st.error(f"Erro na validação!")
        else:
            st.success("O schema do arquivo Excel está correto!")

    def display_dataframe(self, result):
        st.dataframe(result, width="stretch")
        
    def display_save_button(self):
        return st.button("Salvar no Banco de Dados")
    
    def display_wrong_message(self, message: str = None):
        if message is not None:
            return st.error(message)
        else:
            return st.error("Necessário corrigir a planilha!")
        
    def expander(self, message):
        return st.expander(message)
    
    def display_error(self, e):
        return st.error(str(e))
    
    def display_success_message(self):
        return st.success("Dados salvos com sucesso no banco de dados!")
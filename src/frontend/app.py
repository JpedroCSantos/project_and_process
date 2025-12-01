from frontend import ExcelValidadorUI
from src.backend.excel_extrator import ExcelExtractor
from src.backend.db_conection import send_dataframe_to_database 

def main():
    ui = ExcelValidadorUI()
    upload_file = ui.upload_file()
    
    if upload_file:
        extractor = ExcelExtractor(upload_file)
        df, result, error = extractor.process_file()
        ui.display_results(result, error)

        if error:
            message = (f"Encontramos {len(error)} linhas com problemas no seu arquivo. Por favor, corrija-as e faça o upload novamente.")
            ui.display_wrong_message(message)
            with ui.expander("Clique aqui para ver os detalhes dos erros"):
                erros_df = extractor.get_errors_as_df(error)
                ui.display_dataframe(erros_df)
            ui.display_wrong_message()
        elif ui.display_save_button():
            result = send_dataframe_to_database(df)
            if result is not None:
                ui.display_wrong_message(result)
            ui.display_success_message()

if __name__ == "__main__":
    main()
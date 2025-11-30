from frontend import ExcelValidadorUI
from src.backend.excel_extrator import process_file, process_erros_df
from src.contracts.contract import Vendas

def main():
    ui = ExcelValidadorUI()
    upload_file = ui.upload_file()
    
    if upload_file:
        df, result, error = process_file(upload_file)
        ui.display_results(result, error)

        if error:
            message = (f"Encontramos {len(error)} linhas com problemas no seu arquivo. Por favor, corrija-as e faça o upload novamente.")
            ui.display_wrong_message(message)
            with ui.expander("Clique aqui para ver os detalhes dos erros"):
                df = process_erros_df(error)
                ui.display_dataframe(df)
            ui.display_wrong_message()
        elif ui.display_save_button():
            ui.display_success_message()
            # logging.info(" Foi enviado com sucesso o banco SQL")
            # sentry_sdk.capture_message("O banco SQL foi atualizado")

if __name__ == "__main__":
    main()
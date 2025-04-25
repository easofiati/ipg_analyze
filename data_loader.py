import base64
import io
import pandas as pd

class DataLoader:
    def load_data(self, contents, filename):
        """
        Carrega os dados do arquivo enviado pelo usuário.
        
        Args:
            contents (str): Conteúdo do arquivo em base64
            filename (str): Nome do arquivo
            
        Returns:
            pandas.DataFrame: DataFrame com os dados carregados
        """
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        try:
            if 'csv' in filename:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                df = pd.read_excel(io.BytesIO(decoded))
            else:
                raise ValueError('Formato de arquivo não suportado. Use CSV ou Excel.')
            return df
        except Exception as e:
            print(f'Erro ao carregar arquivo: {str(e)}')
            return None 
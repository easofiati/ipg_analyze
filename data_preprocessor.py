import pandas as pd
import numpy as np

class DataPreprocessor:
    def process_data(self, df):
        """
        Processa os dados brutos do DataFrame.
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados brutos
            
        Returns:
            pandas.DataFrame: DataFrame com os dados processados
        """
        try:
            # Remove linhas duplicadas
            df = df.drop_duplicates()
            
            # Remove linhas com valores nulos
            df = df.dropna()
            
            # Converte colunas numéricas para o tipo correto
            numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Remove outliers usando o método IQR
            for col in numeric_columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                df = df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]
            
            return df
        except Exception as e:
            print(f'Erro ao processar dados: {str(e)}')
            return None 
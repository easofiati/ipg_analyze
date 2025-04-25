import pandas as pd
import numpy as np

class DataFilter:
    def filter_data(self, df):
        """
        Filtra os dados avaliados com base em critérios específicos.
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados avaliados
            
        Returns:
            pandas.DataFrame: DataFrame com os dados filtrados
        """
        try:
            # Filtra registros com base no z-score
            zscore_columns = [col for col in df.columns if 'zscore' in col]
            for col in zscore_columns:
                df = df[abs(df[col]) <= 3]  # Remove valores com z-score > 3
            
            # Filtra registros com base no percentil
            percentile_columns = [col for col in df.columns if 'percentile' in col]
            for col in percentile_columns:
                df = df[(df[col] >= 0.1) & (df[col] <= 0.9)]  # Mantém dados entre 10º e 90º percentil
            
            # Remove colunas auxiliares de avaliação
            df = df.drop(columns=zscore_columns + percentile_columns)
            
            return df
        except Exception as e:
            print(f'Erro ao filtrar dados: {str(e)}')
            return None 
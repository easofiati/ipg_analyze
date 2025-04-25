import pandas as pd
import numpy as np

class DataEvaluator:
    def evaluate_data(self, df):
        """
        Avalia os dados processados e adiciona métricas de avaliação.
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados processados
            
        Returns:
            pandas.DataFrame: DataFrame com as métricas de avaliação adicionadas
        """
        try:
            # Calcula estatísticas básicas para colunas numéricas
            numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
            
            for col in numeric_columns:
                # Calcula z-score para identificar valores atípicos
                df[f'{col}_zscore'] = (df[col] - df[col].mean()) / df[col].std()
                
                # Calcula percentis
                df[f'{col}_percentile'] = df[col].rank(pct=True)
                
                # Calcula rolling mean (média móvel)
                df[f'{col}_rolling_mean'] = df[col].rolling(window=3, min_periods=1).mean()
            
            return df
        except Exception as e:
            print(f'Erro ao avaliar dados: {str(e)}')
            return None 
import pandas as pd
import numpy as np

class DataReport:
    def calculate_profit(self, df):
        """
        Calcula o lucro com base nos dados filtrados.
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados filtrados
            
        Returns:
            float: Valor do lucro calculado
        """
        try:
            # Assume que temos colunas de receita e custo
            if 'receita' in df.columns and 'custo' in df.columns:
                profit = df['receita'].sum() - df['custo'].sum()
            else:
                # Se não houver colunas específicas, calcula a média de todas as colunas numéricas
                numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
                profit = df[numeric_columns].mean().mean()
            
            return round(profit, 2)
        except Exception as e:
            print(f'Erro ao calcular lucro: {str(e)}')
            return None 
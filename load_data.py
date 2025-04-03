from get_data import *
from config import *
import warnings
warnings.filterwarnings("ignore")

######################## LOAD DATA

def load_data():

    #df_final_comh = get_df_final_comh()

    transformed_data = transform_data(indicadores_ecb)

    #quarterly_ecb_data = extract_and_combine_data(transformed_data, 'Quarterly', start_date=start_date)
    #quarterly_ecb_data['TIME_PERIOD'] = quarterly_ecb_data['TIME_PERIOD'].dt.date

    annual_ecb_data = extract_and_combine_data(transformed_data, 'Annual', start_date=start_date)
    annual_ecb_data['TIME_PERIOD'] = (annual_ecb_data['TIME_PERIOD']).astype(str).str[-4:].astype(int)

    monthly_ecb_data = extract_and_combine_data(transformed_data, 'Monthly', start_date=start_date)
    monthly_ecb_data['TIME_PERIOD'] = pd.to_datetime(monthly_ecb_data['TIME_PERIOD'])
    #monthly_ecb_data['TIME_PERIOD'] = monthly_ecb_data['TIME_PERIOD'].dt.date
    monthly_ecb_data['TIME_PERIOD'] = monthly_ecb_data['TIME_PERIOD'].dt.year

    # Calcular a média do desemprego por ano
    mean_unemployment_per_year = monthly_ecb_data.groupby('TIME_PERIOD')['Unemployment rate, Portugal'].mean().reset_index()
    mean_unemployment_per_year

    annual_data = annual_ecb_data.merge(mean_unemployment_per_year, how='left', on='TIME_PERIOD')

    #df_bpstat = df_final_comh.copy()
    #df_bpstat.columns = ['_'.join(col) for col in df_bpstat.columns]
    #df_bpstat = df_bpstat.reset_index().rename(columns={'index': 'TIME_PERIOD'})
    #df_bpstat =  df_bpstat.drop(columns=["Autonomia Financeira_C17 Paper", "Financiamentos obtidos em % ativo_C17 Paper"])
    #df_bpstat['TIME_PERIOD'] = pd.to_datetime(df_bpstat['TIME_PERIOD'])
    #df_bpstat['TIME_PERIOD'] = df_bpstat['TIME_PERIOD'].dt.year

    df_final = get_df_final().rename(columns={'Date': 'TIME_PERIOD'})
    df_final['TIME_PERIOD'] = pd.to_datetime(df_final['TIME_PERIOD'])
    df_final['TIME_PERIOD'] = df_final['TIME_PERIOD'].dt.year

    final_dataset = annual_data.merge(df_final, on='TIME_PERIOD', how='left')
    final_dataset

    return  annual_data, df_final, final_dataset
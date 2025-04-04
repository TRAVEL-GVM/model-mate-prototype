import streamlit as st
from viz import *
from get_data import *
from config import *
from load_data import load_data
import warnings
warnings.filterwarnings("ignore")
from xlsxwriter import Workbook
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from pca_section import *

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


@st.cache_data(ttl=3600*24)  # Atualiza os dados a cada 3600 segundos (1 hora)
def get_data_cached():
    return load_data()

#################################################### BUILD DASHBOARD ############################################


st.set_page_config(page_title=dashboard_main_title, layout="wide")
st.markdown(f"<h1 style='color:{default_color1};'>{dashboard_main_title}</h1>", unsafe_allow_html=True)

# white Logo
st.sidebar.markdown(f'<a><img src="{travel_logo_url}" alt="Logo" style="width: 100%;"></a>', unsafe_allow_html=True)

#################### gathering data ###################################################

annual_data, df_final, final_dataset = get_data_cached()

###########################################################################################

st.sidebar.header("MENU:")
indicador = st.sidebar.selectbox(
    "CHOOSE A SECTION:", sidebar_indicators
)

#################################################### PCA ############################################################################################

if indicador == "Principal Components Analysis":

    indicador = st.sidebar.selectbox(
    "Choose a dataset to analyse:", ('Macroeconomic ECB data', 'BPSTAT Data', 'Macroeconomic ECB & BPSTAT data')
    )

    if indicador == 'Macroeconomic ECB data':

        st.markdown(container_style_html, unsafe_allow_html=True)

        with st.container():
            st.markdown(f"""    
            <div style='text-align: center; margin-bottom: 30px;'>
                <h1 style='color: {default_color1};'>Macroconomic ECB data - Principal Component Analysis</h1>
                <p style='color: #666; font-size: 16px;'>Make your PCA analysis</p>
            </div>
            """, unsafe_allow_html=True)

            # Seção de visualização de dados
        with st.expander("🔍 Data preview", expanded=False):
            st.dataframe(annual_data.head(3), use_container_width=True, hide_index=True)

        # Seleção de colunas (sem nenhuma coluna selecionada por padrão)
        selected_columns = st.multiselect(
            "Choose the macroeconomic variables for the PCA:", options=annual_data.columns.tolist()[1:], default=['Unemployment rate, Portugal',
                                                                               'Gross domestic product at market prices, Portugal',
                                                                               'Government final consumption, Portugal']
        )

        if not selected_columns:
            st.warning("Please, select at least 3 columns for the PCA.")
        else:

            with st.expander("🔍 Dataframe for PCA", expanded=False):
                # Verificar se o usuário selecionou colunas
                if selected_columns:
                    # Mostrar o DataFrame com as colunas selecionadas
                    st.markdown(f"""<div style='text-align: center;'>
                                        <h6 style='color: {default_color1};'>Dataframe with the selected columns</h6>
                                    </div>""", unsafe_allow_html=True)
                    
                    st.dataframe(annual_data[selected_columns], use_container_width=True, hide_index=True)
                else:
                    st.markdown(f"""<div style='text-align: center;'>
                                        <h6 style='color: {default_color1};'>Select variables for PCA</h6>
                                    </div>""", unsafe_allow_html=True)
                    
            with st.expander("🔍 Results for PCA", expanded=True):
                plot_pca_results(annual_data[selected_columns], len(selected_columns))

            with st.expander("**Select the number of factors for PCA for a more specific analysis**", expanded=False):
                num_factors = st.number_input(
                    "Choose the number of factors:", min_value=1, max_value=annual_data[selected_columns].shape[1] - 1, value=2
                )

                # Exibir a análise PCA se o número de fatores for válido
                if num_factors > 0:
                    plot_pca_results(annual_data[selected_columns], num_factors)
                else:
                    st.warning("Please, select a valid number of factors less than the number of columns selected.")



    elif indicador == 'BPSTAT Data':

        st.markdown(container_style_html, unsafe_allow_html=True)

        with st.container():
            st.markdown(f"""    
            <div style='text-align: center; margin-bottom: 30px;'>
                <h1 style='color: {default_color1};'>BPSTAT Data - Principal Component Analysis</h1>
                <p style='color: #666; font-size: 16px;'>Make your PCA analysis</p>
            </div>
            """, unsafe_allow_html=True)

            # Seção de visualização de dados
        with st.expander("🔍 Data preview", expanded=False):
            st.dataframe(df_final.head(3), use_container_width=True, hide_index=True)

        # Seleção de colunas (sem nenhuma coluna selecionada por padrão)
        selected_columns = st.multiselect(
            "Choose the variables for the PCA:", options=df_final.columns.tolist()[1:], default=['Current ratio-J58 Publishing',
                                                                                                               'Current ratio-F Construction',
                                                                                                               'Current ratio-C20 Chemicals',
                                                                                                               'Current ratio-I56 Food service activities']
        )

        if not selected_columns:
            st.warning("Please, select at least 3 columns for the PCA.")
        else:

            with st.expander("🔍 Dataframe for PCA", expanded=False):
                # Verificar se o usuário selecionou colunas
                if selected_columns:
                    # Mostrar o DataFrame com as colunas selecionadas
                    st.markdown(f"""<div style='text-align: center;'>
                                        <h6 style='color: {default_color1};'>Dataframe with the selected columns</h6>
                                    </div>""", unsafe_allow_html=True)
                    
                    st.dataframe(df_final[selected_columns], use_container_width=True, hide_index=True)
                else:
                    st.markdown(f"""<div style='text-align: center;'>
                                        <h6 style='color: {default_color1};'>Select variables for PCA</h6>
                                    </div>""", unsafe_allow_html=True)
                    
            with st.expander("🔍 Results for PCA", expanded=True):
                plot_pca_results(df_final[selected_columns], len(selected_columns))

            with st.expander("**Select the number of factors for PCA for a more specific analysis**", expanded=False):
                num_factors = st.number_input(
                    "Choose the number of factors:", min_value=1, max_value=df_final[selected_columns].shape[1] - 1, value=2
                )

                # Exibir a análise PCA se o número de fatores for válido
                if num_factors > 0:
                    plot_pca_results(df_final[selected_columns], num_factors)
                else:
                    st.warning("Please, select a valid number of factors less than the number of columns selected.")
        
    elif indicador == 'Macroeconomic ECB & BPSTAT data':
        
        st.markdown(container_style_html, unsafe_allow_html=True)

        with st.container():
            st.markdown(f"""    
            <div style='text-align: center; margin-bottom: 30px;'>
                <h1 style='color: {default_color1};'>BPSTAT Data - Principal Component Analysis</h1>
                <p style='color: #666; font-size: 16px;'>Make your PCA analysis</p>
            </div>
            """, unsafe_allow_html=True)

            # Seção de visualização de dados
        with st.expander("🔍 Data preview", expanded=False):
            st.dataframe(final_dataset.head(3), use_container_width=True, hide_index=True)

        # Seleção de colunas (sem nenhuma coluna selecionada por padrão)
        selected_columns = st.multiselect(
            "Choose the variables for the PCA:", options=final_dataset.columns.tolist()[1:], default=['Current ratio-J58 Publishing',
                                                                                                               'Current ratio-F Construction',
                                                                                                               'Current ratio-C20 Chemicals',
                                                                                                               'Current ratio-I56 Food service activities']
        )

        if not selected_columns:
            st.warning("Please, select at least 3 columns for the PCA.")
        else:

            with st.expander("🔍 Dataframe for PCA", expanded=False):
                # Verificar se o usuário selecionou colunas
                if selected_columns:
                    # Mostrar o DataFrame com as colunas selecionadas
                    st.markdown(f"""<div style='text-align: center;'>
                                        <h6 style='color: {default_color1};'>Dataframe with the selected columns</h6>
                                    </div>""", unsafe_allow_html=True)
                    
                    st.dataframe(final_dataset[selected_columns], use_container_width=True, hide_index=True)
                else:
                    st.markdown(f"""<div style='text-align: center;'>
                                        <h6 style='color: {default_color1};'>Select variables for PCA</h6>
                                    </div>""", unsafe_allow_html=True)
                    
            with st.expander("🔍 Results for PCA", expanded=True):
                plot_pca_results(final_dataset[selected_columns], len(selected_columns))

            with st.expander("**Select the number of factors for PCA for a more specific analysis**", expanded=False):
                num_factors = st.number_input(
                    "Choose the number of factors:", min_value=1, max_value=df_final[selected_columns].shape[1] - 1, value=2
                )

                # Exibir a análise PCA se o número de fatores for válido
                if num_factors > 0:
                    plot_pca_results(final_dataset[selected_columns], num_factors)
                else:
                    st.warning("Please, select a valid number of factors less than the number of columns selected.")      


############################################################################################################################################

elif indicador == "Correlation Matrix":

    st.markdown(container_style_html, unsafe_allow_html=True)

    with st.container():
        st.markdown(f"""    
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 style='color: {default_color1};'>Correlation analysis</h1>
            <p style='color: #666; font-size: 16px;'>Make your correlation Matrixs</p>
        </div>
        """, unsafe_allow_html=True)

        # Seção de visualização de dados
    with st.expander("🔍 Data preview", expanded=False):
        df_corr_styled = dataframe_with_green_background(final_dataset.head(5))

        # Exibir autovetores
        st.markdown(df_corr_styled, unsafe_allow_html=True)
        #st.dataframe(final_dataset.head(3), use_container_width=True, hide_index=True)

    with st.expander("🔍 Data preview", expanded=True):

        start_date, end_date = st.slider(
            'Select the date range',
            min_value=final_dataset['TIME_PERIOD'].min(),
            max_value=final_dataset['TIME_PERIOD'].max(),
            value=(2010, 2023)
        )

        corr_selected_columns = st.multiselect(
            'Select columns for correlation matrix',
            options=final_dataset.columns[1:],
            default=final_dataset.columns[1:6],
            label_visibility="visible",
            help="Press Ctrl to select more than one column",
            key='selected_columns',
        )

        corr_selected_columns.append('TIME_PERIOD')

        st.markdown(button_css, unsafe_allow_html=True)

        if st.button('Generate Correlation Matrix'):
            #st.write(final_dataset[
            #    (final_dataset['TIME_PERIOD'] >= start_date) & (final_dataset['TIME_PERIOD'] <= end_date) 
            #     ][corr_selected_columns]
            #)
            df_corr_plot = final_dataset[
                                (final_dataset['TIME_PERIOD'] >= start_date) & (final_dataset['TIME_PERIOD'] <= end_date) 
                                        ][corr_selected_columns]

            plot_interact_corr_matrix(df_corr_plot, start_date, end_date, corr_selected_columns)


elif indicador == 'Plots':

    plot_selected_columns = st.multiselect(
    'Select columns to plot',
    options=final_dataset.columns[1:],
    default=['Unemployment rate, Portugal', 'Government final consumption, Portugal'])

    plot_selected_columns.append('TIME_PERIOD')

    plot_interactive_graph(final_dataset[plot_selected_columns])


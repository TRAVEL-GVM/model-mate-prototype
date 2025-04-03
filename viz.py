import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import plotly.graph_objects as go
import plotly.express as px
from config import *

def dataframe_with_green_background(df):

    html = '<table border="1" class="dataframe">'

    html += f'<thead><tr style="background-color: {default_color1}; color: white; font-weight: bold;">'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead>'
    
    html += '<tbody>'
    for row in df.itertuples(index=False):
        html += '<tr>'
        for value in row:
            if isinstance(value, (int, float)):
                value = f'{value:.2f}'
            html += f'<td>{value}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    
    return html

def dataframe_with_green_background_v2(df):
    # Obter o nome da coluna do índice, se existir
    index_name = df.index.name if df.index.name else "."

    html = '<table border="1" class="dataframe">'

    # Cabeçalho da tabela
    html += f'<thead><tr style="background-color: {default_color1}; color: white; font-weight: bold;">'
    html += f'<th>{index_name}</th>'  # Adiciona a coluna de índice
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead>'

    # Corpo da tabela
    html += '<tbody>'
    for idx, row in zip(df.index, df.itertuples(index=False)):
        html += '<tr>'
        # Pintar a célula do índice de verde
        html += f'<td style="background-color: {default_color1}; color: white;">{idx}</td>'
        for value in row:
            if isinstance(value, (int, float)):
                value = f'{value:.2f}'
            html += f'<td>{value}</td>'
        html += '</tr>'
    html += '</tbody></table>'

    return html





def plot_interact_corr_matrix(df, start_date, end_date, selected_columns):

    df_filtered = df[(df['TIME_PERIOD'] >= start_date) & (df['TIME_PERIOD'] <= end_date)]

    if selected_columns:
        df_corr = df_filtered[selected_columns]
        corr_matrix = df_corr.drop(columns=['TIME_PERIOD'], errors='ignore').corr()

        plt.figure(figsize=(12, 12))
        sns.heatmap(corr_matrix, annot=True, cmap='Greens', vmin=-1, vmax=1)
        plt.suptitle(f'Correlation matrix    ({str(start_date)} - {str(end_date)})', fontweight='bold',
                     color=default_color1, fontsize=18)

        plt.tight_layout()

        st.pyplot(plt.gcf())

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', transparent=True)
        buffer.seek(0)

        st.download_button(
            label="Download Correlation Matrix",
            data=buffer,
            file_name="correlation_matrix.png",
            mime="image/png"
        )

    else:
        st.write("Select at least 1 column to generate the correlation matrix.")


def plot_interactive_graph(df):
    if len(df.columns) > 1:
        fig = px.line(
            df,
            x='TIME_PERIOD',
            y=df.columns,
            title="Time Evolution of Selected Variables",
            markers=True
        )

        fig.update_layout(
            width=1200,
            height=600,
            legend=dict(
                orientation="v",
                x=40,
                xanchor="right",
                y=1,
                font=dict(size=9)
            )
        )

        st.plotly_chart(fig)
    else:
        st.write("Please select at least one variable to plot.")
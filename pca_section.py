import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import streamlit as st
from config import *
from viz import *


def plot_pca_results(df, num_factors):
    # Verificar quantas linhas com nulos serão eliminadas
    rows_before = df.shape[0]
    df_clean = df.dropna()
    rows_after = df_clean.shape[0]
    rows_dropped = rows_before - rows_after

    # Exibir aviso no Streamlit se houver remoção de linhas
    if rows_dropped > 0:
        st.warning(f"{rows_dropped} rows were dropped due to missing values.")
    
    # Escalar os dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean.values)
    
    # Aplicar PCA
    pca = PCA(n_components=num_factors)
    pca.fit(X_scaled)

    # Autovalores, autovetores e variância explicada
    eigenvalues = pca.explained_variance_
    eigenvectors = pca.components_
    explained_variance_ratio = pca.explained_variance_ratio_

    sns.set(style="whitegrid", palette="pastel", font_scale=1.2)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5))

    fatores_x = [f'F{i}' for i in range(1, num_factors + 1)]

    # Primeiro subplot: Proporção da Variância Explicada por cada fator
    sns.barplot(x=fatores_x, y=explained_variance_ratio, ax=ax1, color='green', alpha=0.8)
    ax1.set_xlabel('Fatores', fontsize=8, labelpad=10)
    ax1.set_ylabel('Proporção da Variância Explicada', fontsize=11, labelpad=10)
    ax1.set_title('Proporção da Variância Explicada\npor cada Fator', fontsize=12, pad=20)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    for i, value in enumerate(explained_variance_ratio):
        ax1.text(i, value, f'{value:.2f}', ha='center', va='bottom', fontsize=10, color='black')

    # Segundo subplot: Variância Acumulada
    cumulative_variance = np.cumsum(explained_variance_ratio)
    sns.barplot(x=fatores_x, y=cumulative_variance, ax=ax2, color='green', alpha=0.5)
    ax2.set_xlabel('Fatores', fontsize=8, labelpad=10)
    ax2.set_ylabel('Variância Acumulada', fontsize=11, labelpad=10)
    ax2.set_title('Variância Acumulada pelos Fatores', fontsize=12, pad=20)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    for i, value in enumerate(cumulative_variance):
        ax2.text(i, value, f'{value:.2f}', ha='center', va='bottom', fontsize=10, color='black')

    # Terceiro subplot: Método de Keiser (Eigenvalues)
    sns.barplot(x=fatores_x, y=eigenvalues, ax=ax3, color='pink', alpha=0.8)
    ax3.set_xlabel('Fatores', fontsize=8, labelpad=10)
    ax3.set_ylabel('Eigenvalues', fontsize=11, labelpad=10)
    ax3.set_title('Método de Keiser', fontsize=13, pad=20)
    ax3.grid(axis='y', linestyle='--', alpha=0.7)

    for i, value in enumerate(eigenvalues):
        ax3.text(i, value + 0.01, f'{value:.2f}', ha='center', va='bottom', fontsize=10, color='black')

    plt.tight_layout()

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

    st.markdown("### Eigenvectors")

    styled_df = dataframe_with_green_background_v2(pd.DataFrame(eigenvectors, columns=df_clean.columns, index=fatores_x).T)

    # Exibir autovetores
    st.markdown(styled_df, unsafe_allow_html=True)
    #st.dataframe(styled_df)



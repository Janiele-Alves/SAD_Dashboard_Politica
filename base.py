import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    st.title("Leitura de CSV com Streamlit")

    st.sidebar.write("Candidatos")
    st.sidebar.write("Main Page")
    st.sidebar.write("Page 2")
    st.sidebar.markdown("---")

    # Filtro barra lateral
    st.sidebar.header("Filtros")
    uploaded_file = st.file_uploader("Escolha o arquivo CSV", type="csv", label_visibility="collapsed")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1', on_bad_lines='skip', delimiter=';')
            df.columns = df.columns.str.replace('"', '', regex=False)
            st.markdown("<h3 style='margin-top: 50px;'>PRÉVIA DOS DADOS</h3>", unsafe_allow_html=True)
            st.dataframe(df, height=300)  
            
            if 'NM_UE' in df.columns:
                unidades = df["NM_UE"].unique()
                selected_unidade = st.sidebar.selectbox("Selecione a Unidade Eleitoral", [""] + list(unidades), key='unidade')

            if 'DS_CARGO' in df.columns:
                cargos = df["DS_CARGO"].unique()
                selected_cargo = st.sidebar.selectbox("Selecione o Cargo", [""] + list(cargos), key='cargo')

            if selected_unidade and selected_cargo:
                df_filtered = df[(df["NM_UE"] == selected_unidade) & (df["DS_CARGO"] == selected_cargo)]
                
                #1 Gráfico de distribuição do grau de instrução
                if 'DS_GRAU_INSTRUCAO' in df.columns:
                    st.subheader("Distribuição do Grau de Instrução")
                    plt.figure(figsize=(10, 6))
                    ax = sns.countplot(data=df_filtered, x='DS_GRAU_INSTRUCAO', 
                                       order=df_filtered['DS_GRAU_INSTRUCAO'].value_counts().index, 
                                       palette=['#096cca'])

                    ax.set_title("Distribuição do Grau de Instrução", loc='left') 
                    plt.ylabel("Contagem", color='white')
                    plt.xticks(rotation=45, color='white')
                    plt.yticks(color='white')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.spines['left'].set_visible(False)
                    ax.spines['bottom'].set_visible(False)
                    ax.grid(False)
                    plt.gcf().patch.set_facecolor('black')
                    ax.set_facecolor('black')
                    st.pyplot(plt)

                    #2 Gráfico de grau de instrução por gênero
                    if 'DS_GENERO' in df.columns:
                        st.subheader("Distribuição do Grau de Instrução por Gênero")
                        plt.figure(figsize=(10, 6))
                        ax2 = sns.countplot(data=df_filtered, x='DS_GRAU_INSTRUCAO', hue='DS_GENERO', 
                                            order=df_filtered['DS_GRAU_INSTRUCAO'].value_counts().index,
                                            palette=['#82caf9', '#096cca', 'red', '#8aff8a', '#d5b3b5', 'navy']) 
                         
                        # Configuração de texto e título
                        ax2.set_title("Grau de Instrução por Gênero", loc='left', color='white')
                        plt.ylabel("Contagem", color='white')
                        plt.xticks(rotation=45, color='white')
                        plt.yticks(color='white')
                        ax2.spines['top'].set_visible(False)
                        ax2.spines['right'].set_visible(False)
                        ax2.spines['left'].set_visible(False)
                        ax2.spines['bottom'].set_visible(False)
                        ax2.grid(False)
                        plt.gcf().patch.set_facecolor('black')
                        ax2.set_facecolor('black')
                        st.pyplot(plt)

                    #3 Gráfico : Distribuição de Cor/Raça dos Candidatos
                    if 'DS_COR_RACA' in df.columns:
                        st.markdown("Distribuição da cor/raça dos candidatos")

                        # Gráfico de pizza
                        plt.figure(figsize=(8, 8))
                        raca_data = df_filtered['DS_COR_RACA'].value_counts()
                        labels = raca_data.index
                        sizes = raca_data.values
                        colors = ['#82caf9', '#096cca', 'red', '#8aff8a', '#d5b3b5', 'navy']
                        fig, ax = plt.subplots()
                        ax.pie(sizes, colors=colors, autopct='%1.1f%%', textprops={'color': 'white'})  
                        plt.gcf().patch.set_facecolor('black')
                        ax.set_facecolor('black')
                        centre_circle = plt.Circle((0, 0), 0.70, fc='black') 
                        fig.gca().add_artist(centre_circle)
                        plt.axis('equal') 
                        plt.legend(labels=labels, loc="upper right", frameon=False, bbox_to_anchor=(1.3, 1), labelcolor="white")
                        st.pyplot(fig)

                        #4 Gráfico: Distribuição de Gêneros dos Candidatos
                        if 'DS_GENERO' in df.columns:
                            st.markdown(
                                """
                                <div style="background-color: black; padding: 10px; border-radius: 10px;">
                                    <h2 style="color: white; text-align: left;"><strong>Distribuição por Gênero</strong></h2>
                                    Distribuição de Gênero dos Candidatos
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            plt.figure(figsize=(8, 8))

                            genero_data = df_filtered['DS_GENERO'].value_counts()
                            labels = genero_data.index
                            sizes = genero_data.values
                            colors = ['#82caf9', '#096cca']  
                            fig, ax = plt.subplots()
                            ax.pie(sizes, colors=colors, autopct='%1.1f%%', textprops={'color': 'white'})  
                            plt.gcf().patch.set_facecolor('black')
                            ax.set_facecolor('black')
                            centre_circle = plt.Circle((0, 0), 0.70, fc='black')  
                            fig.gca().add_artist(centre_circle)
                            plt.axis('equal') 

                            plt.legend(labels=['Masculino', 'Feminino'], loc="upper right", frameon=False, bbox_to_anchor=(1.3, 1), labelcolor="white")
                            st.pyplot(fig)
                           
                        # 5. Quantidade de Candidatas Femininas por Partido - Gráfico de Barras
                        candidatas_femininas = df_filtered[df_filtered['DS_GENERO'] == 'FEMININO']
                        partido_fem_counts = candidatas_femininas['SG_PARTIDO'].value_counts()

                        norm = plt.Normalize(partido_fem_counts.values.min(), partido_fem_counts.values.max())
                        colors = plt.cm.Blues(norm(partido_fem_counts.values))

                        plt.figure(figsize=(10, 8))
                        ax = plt.gca()
                        plt.gcf().patch.set_facecolor('black')  # Fundo da figura preto
                        ax.set_facecolor('black')  # Fundo do gráfico preto
                        ax.spines['top'].set_visible(False)  # Remove a linha do topo
                        ax.spines['right'].set_visible(False)  # Remove a linha da direita
                        ax.spines['left'].set_visible(False)  # Remove a linha da esquerda
                        ax.spines['bottom'].set_visible(False)  # Remove a linha de baixo
                        ax.grid(False)  # Remove as grades do gráfico

                        bars = ax.bar(partido_fem_counts.index, partido_fem_counts.values, color=colors)

                        for bar in bars:
                            yval = bar.get_height()
                            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, int(yval), ha='center', va='bottom', color='white')

                        ax.set_title('Quantidade de Candidatas Femininas por Partido', loc='left', color='white')  # Título alinhado à esquerda
                        plt.xlabel('Partido', color='white')
                        plt.ylabel('Quantidade', color='white')
                        ax.set_xticks(ax.get_xticks())
                        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, color='white')
                        ax.set_yticklabels(ax.get_yticks(), color='white')

                        sm = plt.cm.ScalarMappable(cmap='Blues', norm=norm)
                        sm.set_array([])

                        cbar_ax = plt.gcf().add_axes([0.9, 0.15, 0.03, 0.7])
                        cbar = plt.colorbar(sm, cax=cbar_ax)
                        cbar.set_label('Quantidade de Candidatas', color='white')
                        cbar.ax.yaxis.label.set_color('white')  # Cor do texto da legenda da barra
                        cbar.ax.tick_params(labelcolor='white')  # Cor dos rótulos da barra
                        st.pyplot(plt)

                        # 6. Quantidade de Candidatos Masculinos por Partido - Gráfico de Barras
                        candidatos_masculinos = df_filtered[df_filtered['DS_GENERO'] == 'MASCULINO']
                        partido_mas_counts = candidatos_masculinos['SG_PARTIDO'].value_counts()

                        norm = plt.Normalize(partido_mas_counts.values.min(), partido_mas_counts.values.max())
                        colors = plt.cm.Blues(norm(partido_mas_counts.values))

                        plt.figure(figsize=(10, 8))
                        ax = plt.gca()
                        plt.gcf().patch.set_facecolor('black')  # Fundo da figura preto
                        ax.set_facecolor('black')  # Fundo do gráfico preto
                        ax.spines['top'].set_visible(False)  # Remove a linha do topo
                        ax.spines['right'].set_visible(False)  # Remove a linha da direita
                        ax.spines['left'].set_visible(False)  # Remove a linha da esquerda
                        ax.spines['bottom'].set_visible(False)  # Remove a linha de baixo
                        ax.grid(False)  # Remove as grades do gráfico

                        bars = ax.bar(partido_mas_counts.index, partido_mas_counts.values, color=colors)

                        for bar in bars:
                            yval = bar.get_height()
                            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, int(yval), ha='center', va='bottom', color='white')

                        ax.set_title('Quantidade de Candidatos Masculinos por Partido', loc='left', color='white')  # Título alinhado à esquerda
                        plt.xlabel('Partido', color='white')
                        plt.ylabel('Quantidade', color='white')
                        ax.set_xticks(ax.get_xticks())
                        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, color='white')
                        ax.set_yticklabels(ax.get_yticks(), color='white')

                        sm = plt.cm.ScalarMappable(cmap='Blues', norm=norm)
                        sm.set_array([])

                        cbar_ax = plt.gcf().add_axes([0.9, 0.15, 0.03, 0.7])
                        cbar = plt.colorbar(sm, cax=cbar_ax)
                        cbar.set_label('Quantidade de Candidatos', color='white')
                        cbar.ax.yaxis.label.set_color('white')  # Cor do texto da legenda da barra
                        cbar.ax.tick_params(labelcolor='white')  # Cor dos rótulos da barra
                        st.pyplot(plt)

                        # 7. Proporção de Candidatos Masculinos e Femininos por Partido - Gráfico de Barras
                        proporcao_counts = df_filtered.groupby(['SG_PARTIDO', 'DS_GENERO']).size().unstack().fillna(0)
                        colors = ['#0F52BA', '#87CEFA']  
                        plt.figure(figsize=(10, 7))
                        ax = plt.gca()
                        plt.gcf().patch.set_facecolor('black')
                        ax.set_facecolor('black')
                        ax.spines['top'].set_visible(False)  
                        ax.spines['right'].set_visible(False)  
                        ax.spines['left'].set_visible(False)  
                        ax.spines['bottom'].set_visible(False)  
                        ax.grid(False)  

                        proporcao_counts.plot(kind='bar', stacked=True, color=colors, ax=ax)
                        ax.set_title('Proporção de Candidatos Masculinos e Femininos por Partido', loc='left', color='white')
                        plt.xlabel('Partido', color='white')
                        plt.ylabel('Quantidade', color='white')
                        plt.xticks(rotation=45, color='white')
                        plt.yticks(color='white')

                        for i in range(proporcao_counts.shape[0]):
                            cum_sum = 0
                            for j in range(proporcao_counts.shape[1]):
                                value = proporcao_counts.iloc[i, j]
                                cum_sum += value
                                if value > 0:
                                    ax.text(i, cum_sum - value / 2, int(value), ha='center', va='center', color='white')
                        st.pyplot(plt)

        except Exception as e:
            st.write("Erro ao processar o arquivo CSV:", e)

if __name__ == "__main__":
    main()
                           
                          
                       

                
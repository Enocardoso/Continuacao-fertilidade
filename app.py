import streamlit as st
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def periodo_fertil_ciclo(ultimo_periodo, duracao_ciclo):
    data_inicio = datetime.datetime.strptime(ultimo_periodo, "%Y-%m-%d")
    dias_para_ovulacao = duracao_ciclo - 14
    data_ovulacao = data_inicio + datetime.timedelta(days=dias_para_ovulacao)
    inicio_fertil = data_ovulacao - datetime.timedelta(days=5)
    fim_fertil = data_ovulacao + datetime.timedelta(days=1)
    return inicio_fertil.date(), fim_fertil.date(), data_ovulacao.date(), data_inicio.date()

st.title("Calculadora Avançada de Período Fértil")
st.markdown("""
Bem-vinda! Este app calcula o seu período fértil aproximado para vários ciclos futuros.

1. Escolha a data do seu último período.
2. Informe a duração média do ciclo menstrual (dias).
3. Escolha quantos ciclos futuros deseja calcular.
""")

ultimo_periodo = st.date_input("Escolha a data do último período")
duracao_ciclo = st.number_input("Duração média do ciclo (dias)", min_value=20, max_value=35, value=28)
num_ciclos = st.number_input("Número de ciclos futuros para calcular", min_value=1, max_value=12, value=3)

if st.button("Calcular"):
    st.success(f"Período fértil estimado para os próximos {num_ciclos} ciclos:")
    ciclos_info = []
    datas_totais = []
    fertil_totais = []
    data_atual = ultimo_periodo
    for i in range(num_ciclos):
        inicio, fim, ovulacao, inicio_ciclo = periodo_fertil_ciclo(data_atual.strftime("%Y-%m-%d"), duracao_ciclo)
        ciclos_info.append(f"Ciclo {i+1}: {inicio} a {fim} (Ovulação: {ovulacao})")
        datas_ciclo = [inicio_ciclo + datetime.timedelta(days=j) for j in range(duracao_ciclo)]
        fertil_ciclo = [1 if inicio <= d <= fim else 0 for d in datas_ciclo]
        datas_totais.extend(datas_ciclo)
        fertil_totais.extend(fertil_ciclo)
        data_atual = data_atual + datetime.timedelta(days=duracao_ciclo)

    for info in ciclos_info:
        st.info(info)

    fig, ax = plt.subplots(figsize=(12,3))
    colors = ['#FFB6C1' if f==1 else '#ADD8E6' for f in fertil_totais]
    ax.bar(datas_totais, [1]*len(datas_totais), color=colors)
    ax.set_yticks([])
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    plt.xticks(rotation=45)
    plt.title("Calendário do Ciclo Menstrual - Vários Ciclos")
    plt.tight_layout()
    st.pyplot(fig)

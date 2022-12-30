import regex as re
import os

uf = 'Região Norte'
uf_sigla = 'n'

df1 = 'df1' + uf_sigla
df2 = 'df2' + uf_sigla
total1 = 'total1' + uf_sigla

str1 = f"# Carga dos dados dos BUs - {uf}\n" \
        f"arquivo1 = f'dados/bweb_{{turnos[0][0]}}t_{uf_sigla.upper()}_{{turnos[0][1]}}.csv'\n" \
        f"arquivo2 = f'dados/bweb_{{turnos[1][0]}}t_{uf_sigla.upper()}_{{turnos[1][1]}}.csv'\n" \
        "\n" \
        f"{df1} = pd.read_csv(arquivo1, usecols=df_columns, encoding=enc, sep=sep)\n" \
        f"print(f'Carregado: {{arquivo1}}')\n" \
        f"{df2} = pd.read_csv(arquivo2, usecols=df_columns, encoding=enc, sep=sep)\n" \
        f"print(f'Carregado: {{arquivo2}}')\n" \
        f"\n" \
        f"# Criação do campo 'data_hora' para conter os dados de recebimento do BU\n" \
        f"{df1}['data_hora'] = pd.to_datetime({df1}['DT_BU_RECEBIDO'], format='%d/%m/%Y %H:%M:%S')\n" \
        f"{df2}['data_hora'] = pd.to_datetime({df2}['DT_BU_RECEBIDO'], format='%d/%m/%Y %H:%M:%S')\n" \
        f"\n" \
        f"# Separação dos votos para Presidente\n" \
        f"{df1} = {df1}[{df1}['CD_ELEICAO'] == 544]\n" \
        f"{df2} = {df2}[{df2}['CD_ELEICAO'] == 545]\n"

str2 = "# Graficos - Total no 1º turno\n" \
       f"gerar_grafico_porcentagem({df1}, 'Total de Votos - 1º Turno', '{uf}')\n"

str3 = "# Total de votos acumulados\n" \
       f"gerar_grafico_temporal({df1}, 'Eleições 2022 - 1º Turno - Contagem temporal para Presidente', '{uf_sigla.upper()}')\n"

str4 = f"{df1}_urnas = {df1}[{df1}['QT_VOTOS'] == 1]\n" \
       f"print(f\"Urnas com 1 voto no candidato 13: {{{df1}_urnas[{df1}_urnas['NR_VOTAVEL'] == 13]['NR_VOTAVEL'].count()}}\")\n" \
       f"print(f\"Urnas com 1 voto no candidato 22: {{{df1}_urnas[{df1}_urnas['NR_VOTAVEL'] == 22]['NR_VOTAVEL'].count()}}\")\n"

str5 = f"{df1}_urnas_22 = {df1}_urnas[{df1}_urnas['NR_VOTAVEL'] == 22]\n" \
       f"{df1}_urnas_22[['NM_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'NR_LOCAL_VOTACAO']]\n"

str6 = f"df_soma = df_diff_group({df1}, {df1}_urnas_22)\n" \
       f"gerar_grafico_urnas_suspeitas(df_soma, {df1}_urnas_22, '{uf}')\n"

str7 = "# Total de votos acumulados, caso as urnas em que o candidato 22 recebeu 1 voto não fossem computadas\n" \
       f"{df1}_sub = {df1}[~(({df1}['CD_MUNICIPIO'].isin({df1}_urnas_22['CD_MUNICIPIO'])) & \n" \
       f"            ({df1}['NR_ZONA'].isin({df1}_urnas_22['NR_ZONA'])) & \n" \
       f"            ({df1}['NR_SECAO'].isin({df1}_urnas_22['NR_SECAO'])) & \n" \
       f"            ({df1}['NR_LOCAL_VOTACAO'].isin({df1}_urnas_22['NR_LOCAL_VOTACAO'])))]\n" \
       f"gerar_grafico_porcentagem({df1}_sub, 'Total de Votos (Caso não se computassem as urnas irregulares) - 1º Turno', '{uf}')\n"

str8 = "# Total de votos acumulados, caso as urnas em que o candidato 22 recebeu 1 voto não fossem computadas\n" \
       f"gerar_grafico_temporal({df1}_sub, 'Eleições 2022 - Primeiro Turno - Apuração sem urnas viciadas', '{uf_sigla.upper()}')"

file = open("generated.txt", "w+")

file.writelines('### ' + uf.upper() + '\n')
file.writelines(str1)
file.writelines('\n##### 1.2.1.1. ' + uf.upper() + '\n')
file.writelines(str2)
file.writelines(str3)
file.writelines(str4)
file.writelines(str5)
file.writelines(str6)
file.writelines(str7)
file.writelines(str8)

file.close()

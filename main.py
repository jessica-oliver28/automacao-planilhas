"""
Sistema de Automação de Planilhas - Versão Simples
Autora: Jéssica Oliveira
Funcionalidades: ler CSV/Excel, filtrar por status ou data, e gerar relatório no excel

Objetivo: demonstrar habilidades em Python para automação de dados,
atendendo aos requisitos da vaga: tratamento de planilhas, filtros,
geração de relatórios e organização de código.
"""
 #ferramenta padrão para manipular dados em tabelas.
import pandas as pd
#datetime para garantir que as datas sejam comparadas corretamente, evitando erros comuns de formato.
from datetime import datetime
#consigo verificar se um arquivo existe antes de tentar abrir, evitando bugs.
import os


# 1.Criando dados para usar de exemplo (fazer testes)

def criar_exemplo():
  
    #Essa função só é usada se o usuário não tiver um arquivo próprio, então criei dados fictícios para demonstrar o funcionamento do script.
    
    dados = {
        "numero_processo": ["001/2026", "002/2026", "003/2026", "004/2026", "005/2026"],
        "cliente": ["Empresa A", "Empresa B", "Empresa C", "Empresa A", "Empresa D"],
        "status": ["pendente", "concluído", "pendente", "concluído", "pendente"],
        "data_abertura": ["10/01/2026", "15/02/2026", "20/03/2026", "05/04/2026", "12/05/2026"],
        "valor": [17280.00, 2509.00, 876.00, 3470.00, 438.00]
    }

    # Aqui criei um DataFrame, ou seja uma tabela, e salvo como CSV. O parâmetro index=False evita uma coluna extra de números desnecessária.
    df = pd.DataFrame(dados)
    df.to_csv("processos.csv", index=False, encoding="utf-8")
    print("Arquivo de exemplo criado: processos.csv")
    return df


# 2. Carregar os arquivos - CSV ou Excel

def carregar_arquivo(caminho):
    """
    O escritório pode receber planilhas com diversos formatos diferentes.
    Então essa função detecta a extensão e carrega corretamente.
    Caso o arquivo não for suportado, avisa o usuário de forma clara.
    """

    if caminho.endswith(".csv"):
        return pd.read_csv(caminho, encoding="utf-8")
    elif caminho.endswith((".xlsx", ".xls")):
        return pd.read_excel(caminho)
    else:
# aqui mostra o erro com uma mensagem explicativa, deixando bem claro para o usuário qual é o problema.
        raise ValueError("Formato não suportado. Use .csv, .xlsx ou .xls")



# 3. Filtrar pelo status

def filtrar_status(df, status):
    """
    Aqui eu filtro as linhas onde a coluna 'status' é igual ao valor desejado.
    Então uso .str.lower() para tornar a busca case-insensitive, assim 'PENDENTE', 'Pendente' ou 'pendente' funcionam da mesma forma sem dar erros.
    """
    return df[df["status"].str.lower() == status.lower()]


# 4. Filtrar pela data

def filtrar_data(df, data_inicio=None, data_fim=None):
    """
    Você consegue filtrar processos abertos entre duas datas.
    Se o usuário não informar início ou fim, a função ignora esse filtro.
    """

    #Aqui criei uma cópia do DataFrame original para não alterar a variável original sem querer e dar erros.
    df_temp = df.copy()
    # Converte a coluna de data, o formato dd/mm/aaaa é o padrão brasileiro, caso a planilha vier com outro formato, é só fazer o ajuste aqui.
    df_temp["data_abertura"] = pd.to_datetime(df_temp["data_abertura"], format="%d/%m/%Y")
    if data_inicio:
        df_temp = df_temp[df_temp["data_abertura"] >= pd.to_datetime(data_inicio)]
    if data_fim:
        df_temp = df_temp[df_temp["data_abertura"] <= pd.to_datetime(data_fim)]
    return df_temp


# 5. Gerar o relatório no excel

def gerar_relatorio(df, nome_saida="relatorio.xlsx"):
    #Gera um arquivo Excel com 3 abas de análise.
    with pd.ExcelWriter(nome_saida, engine="openpyxl") as writer:
        # primeira aba: Dados filtrados
        df.to_excel(writer, sheet_name="Dados Filtrados", index=False)

         # segunda aba: Resumo estatístico
        resumo = pd.DataFrame({
            "Métrica": ["Total de registros", "Valor total (R$)", "Valor medio (R$)", "Status mais comum"],
            "Valor": [
                len(df),
                df["valor"].sum(),
                df["valor"].mean(),
                df["status"].mode()[0] if not df.empty else "N/A"
            ]
        })
        resumo.to_excel(writer, sheet_name="Resumo", index=False)
        
        # terceira aba: Contagem por status
        contagem = df["status"].value_counts().reset_index()
        contagem.columns = ["Status", "Quantidade"]
        contagem.to_excel(writer, sheet_name="Contagem por Status", index=False)
    
    print(f" Relatório gerado: {nome_saida}")



    # 6. Programa principal

def main():
    """
    Função principal que faz todo o fluxo funcionar.
    Exibe um menu simples, pergunta o que o usuário quer fazer,
    aplica os filtros, mostra o resultado e pergunta se quer salvar.
    """
    print("=" * 50)
    print("AUTOMAÇÃO DE PLANILHAS - VERSAO PYTHON")
    print("=" * 50)
    
    # Verifico se existe o arquivo de entrada, se não existir, chamo a função de exemplo para não deixar o usuário sem o dado
    arquivo = "processos.csv"
    if not os.path.exists(arquivo):
        print("Nenhum arquivo encontrado. Criando dados de exemplo...")
        df = criar_exemplo()
    else:
        print(f"Carregando {arquivo}...")
        df = carregar_arquivo(arquivo)
    
    print(f"Total de registros: {len(df)}")
    
    # Menu de filtros- usei números para facilitar para o usuário
    print("\n Opções de filtro:")
    print("1 - Mostrar todos")
    print("2 - Filtrar por status (pendente/concluido)")
    print("3 - Filtrar por data (ex: 01/01/2024 ate 31/12/2024)")
    opcao = input("Escolha (1/2/3): ")
    
    df_filtrado = df   # inicio o DataFrame completo
    
    if opcao == "2":
        status = input("Digite o status (pendente/concluido): ")
        df_filtrado = filtrar_status(df, status)
        print(f" Mostrando {len(df_filtrado)} processos com status '{status}'")
    elif opcao == "3":
        inicio = input("Data início (DD/MM/AAAA) ou Enter para ignorar: ")
        fim = input("Data fim (DD/MM/AAAA) ou Enter para ignorar: ")
        # Só passo o valor se o usuário digitou algo, senão digitar, mando NONE.
        df_filtrado = filtrar_data(df, inicio if inicio else None, fim if fim else None)
        print(f" Mostrando {len(df_filtrado)} processos no período selecionado")
    else:
        print(" Mostrando todos os processos")
    
    # Exibe os primeiros registros na tela
    print("\n RESULTADO:")
    print(df_filtrado.to_string(index=False))
    
    # Perguntar se quer salvar
    salvar = input("\n Deseja salvar esse resultado em Excel? (s/n): ")
    if salvar.lower() == "s":
        gerar_relatorio(df_filtrado, "relatório_filtrado.xlsx")
    
    print("\n Fim da automação.")

if __name__ == "__main__":
    main()

    """
    Essa condição garante que o código só rode se o arquivo for executado diretamente.
    Se ele for importado como módulo em outro script, o main() não roda automaticamente.
    É uma boa prática para reaproveitamento de código.
    """
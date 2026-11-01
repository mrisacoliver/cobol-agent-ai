from crewai import Agent, Crew, Process, Task

# =====================================================================
# CÓDIGO COBOL DE EXEMPLO PARA TRADUÇÃO
# =====================================================================
codigo_cobol_exemplo = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. CALCJUROS.
       
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-VALOR-PRINCIPAL    PIC 9(7)V99 VALUE 1000.00.
       01 WS-TAXA-JUROS         PIC 9(1)V99 VALUE 0.05.
       01 WS-DIAS-ATRASO        PIC 9(3)    VALUE 30.
       01 WS-VALOR-FINAL        PIC 9(7)V99.
       01 WS-MULTA              PIC 9(5)V99.

       PROCEDURE DIVISION.
           IF WS-DIAS-ATRASO > 0 THEN
               COMPUTE WS-MULTA = WS-VALOR-PRINCIPAL * 0.02
               COMPUTE WS-VALOR-FINAL = WS-VALOR-PRINCIPAL + WS-MULTA + 
                       (WS-VALOR-PRINCIPAL * WS-TAXA-JUROS * (WS-DIAS-ATRASO / 30))
           ELSE
               MOVE WS-VALOR-PRINCIPAL TO WS-VALOR-FINAL
           END-IF.

           DISPLAY "VALOR FINAL: " WS-VALOR-FINAL.
           STOP RUN.
"""

# =====================================================================
# PASSO 1: DEFINIÇÃO DOS AGENTES
# =====================================================================

# Agente 1: Analista de Código Legado
analista_cobol = Agent(
    role="Analista Especialista em COBOL Mainframe",
    goal="Analisar códigos COBOL legados, entender a lógica de negócios e gerar documentação detalhada.",
    backstory=(
        "Você é um engenheiro de software sênior com 30 anos de experiência em mainframes IBM. "
        "Sua especialidade é ler código COBOL complexo, mapear o fluxo de dados e extrair "
        "as regras de negócio de forma clara e estruturada em Português."
    ),
    verbose=True
)

# Agente 2: Arquiteto e Tradutor Python
tradutor_python = Agent(
    role="Engenheiro de Software Python Sênior",
    goal="Traduzir regras de negócio documentadas de COBOL para código Python moderno, limpo e legível.",
    backstory=(
        "Você é um especialista em arquitetura de código Python. Você garante que a lógica vinda do COBOL "
        "seja reescrita utilizando boas práticas (PEP 8, tipagem estática e precisão com decimal.Decimal para finanças)."
    ),
    verbose=True
)

# Agente 3: Engenheiro de QA e Testes
engenheiro_qa = Agent(
    role="Engenheiro de Garantia de Qualidade e Testes",
    goal="Gerar testes unitários em Pytest para garantir que o código Python traduzido corresponda exatamente à regra do COBOL.",
    backstory=(
        "Você é rigoroso com testes de validação. Seu papel é criar cenários de teste com Pytest "
        "para garantir que bordas, precisão decimal e fluxos condicionais funcionem perfeitamente."
    ),
    verbose=True
)

# =====================================================================
# PASSO 2: DEFINIÇÃO DAS TAREFAS
# =====================================================================

# Tarefa 1: Mapeamento e Documentação
tarefa_analise = Task(
    description=(
        f"Analise o seguinte código COBOL e crie uma documentação funcional detalhada:\n\n{codigo_cobol_exemplo}\n\n"
        "Sua documentação deve incluir:\n"
        "1. Objetivo do programa.\n"
        "2. Mapeamento das variáveis da DATA DIVISION e seus tipos.\n"
        "3. Descrição passo a passo da regra de negócio na PROCEDURE DIVISION."
    ),
    expected_output="Documentação em Markdown detalhando o comportamento do programa COBOL e suas regras de cálculo.",
    agent=analista_cobol
)

# Tarefa 2: Tradução para Python
tarefa_traducao = Task(
    description=(
        "Com base na documentação gerada pelo Analista, escreva o código Python equivalente.\n"
        "Regras obrigatórias:\n"
        "- Use a biblioteca `decimal.Decimal` para todos os campos monetários/taxas para evitar erros de ponto flutuante.\n"
        "- Crie uma função ou classe bem estruturada com type hints.\n"
        "- Inclua docstrings explicativas."
    ),
    expected_output="Código Python completo, limpo e executável que implementa a mesma lógica do COBOL.",
    agent=tradutor_python
)

# Tarefa 3: Geração de Testes Unitários
tarefa_testes = Task(
    description=(
        "Escreva um arquivo de testes unitários usando `pytest` para a função Python criada pelo Tradutor.\n"
        "Inclua cenários com dias de atraso zerados, atraso positivo e validação de precisão decimal."
    ),
    expected_output="Código Python completo de testes com a biblioteca pytest.",
    agent=engenheiro_qa
)

# =====================================================================
# PASSO 3: EXECUÇÃO DA EQUIPE
# =====================================================================
equipe_modernizacao = Crew(
    agents=[analista_cobol, tradutor_python, engenheiro_qa],
    tasks=[tarefa_analise, tarefa_traducao, tarefa_testes],
    process=Process.sequential
)

if __name__ == "__main__":
    resultado = equipe_modernizacao.kickoff()
    print("\n================ RESULTADO DA MODERNIZAÇÃO ================")
    print(resultado)
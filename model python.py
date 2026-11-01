import json
from cb2game import cb2game  # Parser de COPYBOOK COBOL
from crewai import Agent, Crew, Process, Task
from crewai.tools import tool

# =====================================================================
# EXEMPLO DE COPYBOOK COMPLEXO (com REDEFINES e OCCURS)
# =====================================================================
copybook_exemplo = """
       01 CLIENTE-REGISTRO.
          05 CLI-ID                  PIC 9(08).
          05 CLI-NOME                PIC X(30).
          05 CLI-ENDERECOS OCCURS 2 TIMES.
             10 CLI-RUA              PIC X(25).
             10 CLI-CEP              PIC 9(08).
          05 CLI-DOC-TIPO            PIC X(01).
          05 CLI-DOCUMENTO           PIC X(14).
          05 CLI-CPF REDEFINES CLI-DOCUMENTO.
             10 CLI-CPF-NUM          PIC 9(11).
             10 FILLER               PIC X(03).
"""

# Salva o arquivo temporário para demonstração
with open("CLIENTE.cpy", "w") as f:
    f.write(copybook_exemplo)


# =====================================================================
# FERRAMENTA (TOOL) DE PARSING DE COPYBOOK
# =====================================================================
@tool("Parsear COPYBOOK COBOL")
def parsear_copybook(caminho_arquivo: str) -> str:
    """
    Lê um arquivo COPYBOOK COBOL (.cpy) e retorna uma estrutura JSON 
    detalhando o mapa de memória, campos, hierarquia e tipos de dados.
    """
    try:
        # Executa o parseamento da estrutura COBOL
        estrutura = cb2game.process_copybook(caminho_arquivo)
        
        # Converte a árvore de dados em JSON estruturado para o Agente
        return json.dumps(estrutura, indent=2, ensure_ascii=False)
    except Exception as e:
        # Fallback de tratamento caso o parser encontre sintaxe customizada
        return f"Erro ao processar o COPYBOOK: {str(e)}"


# =====================================================================
# INTEGRAÇÃO COM OS AGENTES CREWAI
# =====================================================================
agente_arquiteto = Agent(
    role="Arquiteto de Integração Mainframe",
    goal="Analisar schemas de COPYBOOKs parseados e desenhar a classe de dados equivalente em Python (Pydantic).",
    backstory="Você é um especialista em converter layouts de memória COBOL em modelos de dados modernos e fortemente tipados.",
    tools=[parsear_copybook],
    verbose=True
)

tarefa_mapeamento = Task(
    description=(
        "Execute a ferramenta 'Parsear COPYBOOK COBOL' no arquivo 'CLIENTE.cpy'. "
        "Com base na estrutura JSON retornada, crie um modelo Pydantic em Python "
        "respeitando a hierarquia dos campos, arrays (OCCURS) e variantes (REDEFINES)."
    ),
    expected_output="Código Python contendo os modelos Pydantic equivalentes ao COPYBOOK.",
    agent=agente_arquiteto
)

equipe = Crew(
    agents=[agente_arquiteto],
    tasks=[tarefa_mapeamento],
    process=Process.sequential
)

if __name__ == "__main__":
    resultado = equipe.kickoff()
    print("\n================ MODELO PYDANTIC GERADO ================")
    print(resultado)
from src.agent import Agent
from src.tools import rag_engine

def main():
    print("Iniciando o seu assitente de suporte técnico...")

    rag_engine.load_runbooks()

    try:
        agent = Agent()
    except ValueError as e:
        print(f"Erro ao configurar o agente: {e}")
        return
    
    print("=======================================")
    print("Agente configurado com sucesso!")
    print("Digite 'sair' para encerrar o programa.")
    print("=======================================")

    while True:
        user_input = input("\n Você: ")
        if user_input.lower() == "sair":
            print("Encerrando o programa. Até mais!")
            break

        if not user_input.strip():
            print("Por favor, insira uma mensagem válida.")
            continue

        print("Processando sua mensagem...")

        try:
            resposta = agent.send_message(user_input)
            print(f"Agente: {resposta}")
        except Exception as e:
            print(f"Ocorreu um erro Minha UMED está apresentando erro G999, o que devo fazer?ao processar a mensagem: {e}")

if __name__ == "__main__":
    main()



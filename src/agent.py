from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from .tools import analise_logs

load_dotenv()

class Agent:
    def __init__(self):
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            raise ValueError("GENAI_API_KEY não encontrado no ambiente.")
        
        self.client = genai.Client(api_key=api_key)

        system_instruction = (
            "Você é um engenheiro de software e especialista em diagnóstico de sistemas. "
            "Sua principal habilidade é ajudar desenvolvedores a resolver erros. "
            "REGRA DE OURO: Sempre que o usuário colar um log de erro ou descrever um "
            "problema técnico, você DEVE acionar a ferramenta 'analise_logs' "
            "para buscar a solução na base de dados interna. "
            "Após receber a solução da ferramenta, explique-a de forma clara e amigável. "
            "Se o usuário apenas der 'bom dia' ou fizer perguntas gerais, responda normalmente sem usar ferramentas."
            "Após receber o resultado da ferramenta, você NUNCA deve responder com texto livre. "
            "Você deve SEMPRE retornar a sua resposta dividida em duas partes, utilizando EXATAMENTE a estrutura abaixo:\n\n"
            "🎧 **ROTEIRO DE INSTRUÇÃO PARA O CLIENTE**\n"
            "**Erro Identificado:** [Código ou nome do erro]\n"
            "**Resolução Técnica: [Descreva a solução técnica de forma clara e amigável, como se estivesse explicando para um cliente. Ex: 'O erro G999 geralmente indica um problema de comunicação entre a UMED e o servidor. Para resolver isso, siga os passos abaixo...']\n"
            "=======================================\n\n"
            "📋 **PROTOCOLO PARA REGISTRO NO SISTEMA**\n"
            "**ANALISE/TESTE:** [Descreva a solução técnica como uma ação que foi orientada ao cliente. Ex: 'Foi instruído ao cliente o desligamento e religamento da UMED...']\n"
            "**CONCLUSÃO:** Procedimento realizado com sucesso. O equipamento voltou a operar normalmente.\n\n"
            "Não adicione nenhuma outra informação fora dessa estrutura."
        )
        

        self.chat = self.client.chats.create(
            model="gemini-3.1-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[analise_logs],
                temperature=0.2,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
            )
        )

    def send_message(self, message: str) -> str:
        response = self.chat.send_message(message)

        if response.text:
            return response.text
        
        if response.function_calls:
            nome_funcao = response.function_calls[0].name
            return f"A IA encontrou a solução na ferramenta '{nome_funcao}', mas a execução automática travou. Verifique os prints."
        
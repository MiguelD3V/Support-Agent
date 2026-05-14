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
            "problema técnico, você DEVE acionar a ferramenta 'analisar_log_do_sistema' "
            "para buscar a solução na base de dados interna. "
            "Após receber a solução da ferramenta, explique-a de forma clara e amigável. "
            "Se o usuário apenas der 'bom dia' ou fizer perguntas gerais, responda normalmente sem usar ferramentas."
            "Caso não encontre a resoluçao do problema, solicite para o usuário entrar em contato com o suporte técnico para uma análise mais aprofundada."
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
        
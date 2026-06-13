from src.rag_engine import RagEngine

rag_engine = RagEngine()

def analise_logs(log_bruto: str) -> str:
    print(f"\n[SISTEMA] ⚙️ Habilidade ativada pela IA! Buscando RAG para: '{log_bruto[:40]}...'")
    
    solucao = rag_engine.buscar_solucao(log_bruto)
    return f"Solução histórica encontrada na base: {solucao}"
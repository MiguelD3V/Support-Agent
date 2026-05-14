import chromadb
import os
import PyPDF2 
import glob

class RagEngine:
    def __init__(self):
        os.makedirs("./vector_db", exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(path="./vector_db")
        self.collection = self.chroma_client.get_or_create_collection(
            name="log_solutions",
            metadata={"hnsw:space": "cosine"},
            embedding_function=chromadb.utils.embedding_functions.DefaultEmbeddingFunction()
        )

    def load_pdf(self, caminho_pdf: str):
        if not os.path.exists(caminho_pdf):
            print(f"[RAG] Erro: Arquivo {caminho_pdf} não encontrado.")
            return

        print(f"[RAG] Extraindo texto do PDF: {caminho_pdf}...")
        with open(caminho_pdf, 'rb') as arquivo:
            pdf_reader = PyPDF2.PdfReader(arquivo)
            
            page_texts = []
            metadados = []
            ids = []
            
            for num_pagina, pagina in enumerate(pdf_reader.pages):
                texto = pagina.extract_text()
                if texto.strip(): 
                    page_texts.append(texto)
                    
                    metadados.append({"fonte": caminho_pdf, "pagina": str(num_pagina + 1)})
                    ids.append(f"doc_{os.path.basename(caminho_pdf)}_pag_{num_pagina}")

            if page_texts:
                self.collection.add(
                    documents=page_texts,
                    metadatas=metadados,
                    ids=ids
                )
                print(f"[RAG] Sucesso! {len(page_texts)} páginas indexadas no banco.")

    def load_runbooks(self, path="data/runbooks"):
        pdf_archives = glob.glob(f"{path}/*.pdf")
        txt_archives = glob.glob(f"{path}/*.txt")
        all_archives = pdf_archives + txt_archives

        if not all_archives:
            print("Nenhum arquivo encontrado no diretório especificado.")
            return

        for archive in all_archives:
            if archive.endswith('.pdf'):
                self.load_pdf(archive)
            elif archive.endswith('.txt'):
                with open(archive, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                self.collection.upsert(
                    documents=[conteudo],
                    metadatas=[{"fonte": archive}],
                    ids=[f"doc_{os.path.basename(archive)}"]
                )
                print(f"[RAG] Arquivo TXT {archive} indexado com sucesso!")

    def buscar_solucao(self, query_log: str) -> str:
        if self.collection.count() == 0:
            return "O banco de conhecimento RAG está vazio."
                
        results = self.collection.query(
            query_texts=[query_log],
            n_results=2
        )
            
        if results['documents'] and len(results['documents'][0]) > 0:
            contexto_final = ""
            
            for texto, meta in zip(results['documents'][0], results['metadatas'][0]):
                pagina_info = f" (Página {meta['pagina']})" if 'pagina' in meta else ""
                contexto_final += f"--- Fato retirado de: {meta['fonte']}{pagina_info} ---\n"
                contexto_final += f"{texto}\n\n"
                
            return contexto_final
                
        return "Nenhuma solução exata encontrada nos runbooks para este erro."
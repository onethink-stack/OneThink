import customtkinter as ctk
from main import analisar_unidade, VICIOS, SINERGIAS
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ONETHINK - Módulo de Diagnóstico")
        self.geometry("600x800")

        self.label_titulo = ctk.CTkLabel(self, text="SISTEMA ONETHINK", font=("Roboto", 24, "bold"))
        self.label_titulo.pack(pady=20)

        self.entry_id = ctk.CTkEntry(self, placeholder_text="ID da Unidade (ex: Alvo-01)", width=350)
        self.entry_id.pack(pady=10)

        # Filtro de exibição por Elo (Opcional, mas ajuda a organizar)
        self.scroll_vicios = ctk.CTkScrollableFrame(self, width=500, height=350, label_text="MAPA DE 28 VÍCIOS")
        self.scroll_vicios.pack(pady=10, padx=10)

        self.check_vars = {}
        # Ordenando para facilitar a leitura
        for codigo, info in VICIOS.items():
            var = ctk.BooleanVar()
            texto_exibicao = f"[{codigo}] {info['nome']} ({info['elo']})"
            cb = ctk.CTkCheckBox(self.scroll_vicios, text=texto_exibicao, variable=var)
            cb.pack(pady=4, padx=15, anchor="w")
            self.check_vars[codigo] = var

        self.btn_gerar = ctk.CTkButton(self, text="EXECUTAR DIAGNÓSTICO", 
                                       command=self.executar, 
                                       fg_color="#1f538d", font=("Roboto", 14, "bold"))
        self.btn_gerar.pack(pady=20)

        # Caixa de Resultado Maior
        self.txt_resultado = ctk.CTkTextbox(self, width=500, height=200, font=("Consolas", 13))
        self.txt_resultado.pack(pady=10)

    def executar(self):
        id_unidade = self.entry_id.get()
        vicios_selecionados = [cod for cod, var in self.check_vars.items() if var.get()]
        
        if not id_unidade or not vicios_selecionados:
            self.atualizar_resultado("⚠️ ERRO: Preencha o ID e selecione os vícios.")
            return

        # Capturamos o que o main.py processa
        # Note: vamos rodar e ler o que foi salvo
        from main import SINERGIAS as sinergias_dict
        
        soma_base = sum(VICIOS[v]['peso'] for v in vicios_selecionados)
        sinergias_nomes = []
        vicios_set = set(vicios_selecionados)
        dano_final = soma_base

        for v_comb, info in sinergias_dict.items():
            if set(v_comb).issubset(vicios_set):
                sinergias_nomes.append(info['nome'])
                dano_final *= info['mult']

        score = round(min(dano_final, 10.0), 2)
        
        # Chama a função original para salvar no banco
        analisar_unidade(id_unidade, vicios_selecionados)
        
        # Monta o relatório visual
        relatorio =  f"📊 RELATÓRIO DE ATROFIA\n"
        relatorio += f"------------------------------\n"
        relatorio += f"UNIDADE: {id_unidade}\n"
        relatorio += f"SCORE FINAL: {score}/10.0\n"
        relatorio += f"------------------------------\n"
        
        if sinergias_nomes:
            relatorio += "⚠️ SINERGIAS DETECTADAS:\n"
            for s in sinergias_nomes:
                relatorio += f" -> {s}\n"
        else:
            relatorio += "Nenhuma sinergia crítica detectada.\n"
            
        relatorio += f"\n[SISTEMA]: Gravado em database.json"
        
        self.atualizar_resultado(relatorio)

    def atualizar_resultado(self, texto):
        self.txt_resultado.delete("0.0", "end")
        self.txt_resultado.insert("0.0", texto)

if __name__ == "__main__":
    app = App()
    app.mainloop()
    
# %%
import pandas as pd
from datetime import datetime
from time import sleep
import os
import customtkinter as ctk
df_alimentos = pd.read_csv('alimentos.csv')
df_eletronicos= pd.read_csv('eletronicos.csv')
df_transporte = pd.read_csv('transporte.csv')

# %%
#Customizações visuais do custom tkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# %%
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Base de Dados Pro")
        self.geometry("600x500")

        # Configuração de Grid para centralizar
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Título
        self.titulo = ctk.CTkLabel(self, text="SISTEMA DE INVENTÁRIO", font=("Roboto", 24, "bold"))
        self.titulo.grid(row=0, column=0, pady=20)

        # 2. Criação das Abas (Tabview)
        self.tabview = ctk.CTkTabview(self, width=500)
        self.tabview.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        self.tab_food = self.tabview.add("Alimentos")
        self.tab_elet = self.tabview.add("Eletrônicos")
        self.tab_transp = self.tabview.add("Transporte")

        self.setup_aba_alimentos()
        self.setup_aba_eletronicos()
        self.setup_aba_transporte()

    # --- ABA ALIMENTOS ---
    def setup_aba_alimentos(self):
        ctk.CTkLabel(self.tab_food, text="Cadastrar Novo Alimento", font=("Arial", 16)).pack(pady=10)
        
        self.food_name = ctk.CTkEntry(self.tab_food, placeholder_text="Nome da Comida", width=300)
        self.food_name.pack(pady=5)
        
        self.food_price = ctk.CTkEntry(self.tab_food, placeholder_text="Preço (Ex: 15.99)", width=300)
        self.food_price.pack(pady=5)
        
        btn = ctk.CTkButton(self.tab_food, text="Salvar Alimento", fg_color="green", hover_color="#014d01",
                            command=self.save_food)
        btn.pack(pady=20)

    # --- ABA ELETRÔNICOS ---
    def setup_aba_eletronicos(self):
        ctk.CTkLabel(self.tab_elet, text="Cadastrar Eletrônico", font=("Arial", 16)).pack(pady=10)
        
        self.elet_brand = ctk.CTkEntry(self.tab_elet, placeholder_text="Marca", width=300)
        self.elet_brand.pack(pady=5)
        
        self.elet_item = ctk.CTkEntry(self.tab_elet, placeholder_text="Aparelho", width=300)
        self.elet_item.pack(pady=5)
        
        self.elet_price = ctk.CTkEntry(self.tab_elet, placeholder_text="Preço", width=300)
        self.elet_price.pack(pady=5)
        
        btn = ctk.CTkButton(self.tab_elet, text="Salvar Eletrônico", command=self.save_elet)
        btn.pack(pady=20)

    # --- ABA TRANSPORTE ---
    def setup_aba_transporte(self):
        ctk.CTkLabel(self.tab_transp, text="Cadastrar Meio de Transporte", font=("Arial", 16)).pack(pady=10)
        
        self.trans_name = ctk.CTkEntry(self.tab_transp, placeholder_text="Transporte", width=300)
        self.trans_name.pack(pady=5)
        
        # Usando um Segmented Button para popularidade (fica mais bonito que digitar 0, 1 ou 2)
        ctk.CTkLabel(self.tab_transp, text="Popularidade:").pack()
        self.trans_pop = ctk.CTkSegmentedButton(self.tab_transp, values=["0 (Baixa)", "1 (Média)", "2 (Alta)"])
        self.trans_pop.pack(pady=5)
        self.trans_pop.set("1 (Média)")
        
        btn = ctk.CTkButton(self.tab_transp, text="Salvar Transporte", command=self.save_trans)
        btn.pack(pady=20)

    # --- LÓGICA DE SALVAMENTO ---
    def salvar_no_csv(self, arquivo, novos_dados):
        df_novo = pd.DataFrame(novos_dados)
        if os.path.exists(arquivo):
            df_novo.to_csv(arquivo, mode='a', index=False, header=False, sep=',')
        else:
            df_novo.to_csv(arquivo, index=False, sep=',')
        
        # Pequeno alerta de sucesso (via terminal ou você pode criar um label)
        print(f"Dados salvos com sucesso em {arquivo}!")

    def save_food(self):
        dados = {
            'Comida': [self.food_name.get()],
            'Preco': [self.food_price.get()],
            'Data': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        }
        self.salvar_no_csv('alimentos.csv', dados)
        self.food_name.delete(0, 'end') # Limpa o campo
        self.food_price.delete(0, 'end')

    def save_elet(self):
        dados = {
            'Marca': [self.elet_brand.get()],
            'Eletronico': [self.elet_item.get()],
            'Preco': [self.elet_price.get()],
            'Data': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        }
        self.salvar_no_csv('eletronicos.csv', dados)
        self.elet_brand.delete(0, 'end')
        self.elet_item.delete(0, 'end')

    def save_trans(self):
        # Pega apenas o primeiro caractere do botão segmentado (o número)
        pop_valor = self.trans_pop.get()[0]
        dados = {
            'Transporte': [self.trans_name.get()],
            'Popularidade': [pop_valor],
            'Data': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        }
        self.salvar_no_csv('transporte.csv', dados)
        self.trans_name.delete(0, 'end')

if __name__ == "__main__":
    app = App()
    app.mainloop()



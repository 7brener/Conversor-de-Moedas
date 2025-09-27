import customtkinter as ctk
import tkinter.messagebox as messagebox
from pegar_moedas import nome_moedas, conversoes_disponiveis
from pegar_cotacao import pegar_cotacao_moeda, cotacoes_coingecko

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Conversor de Moedas & Criptomoedas')
        self.geometry('500x430')
        self.theme = ctk.set_default_color_theme('green')
        self.dict_conversoes_disponiveis = conversoes_disponiveis() # Chave->Moeda, valor->Lista de trocas disponíveis

        ## Criando tabs
        self.tabview = ctk.CTkTabview(self, width=480, height=410)
        self.tabview.pack(padx=10, pady=10, expand=True, fill='both')
        self.tab1 = self.tabview.add('Conversor de Moedas')
        self.tab2 = self.tabview.add('Cotação de Criptomoedas')

        #TAB 1 -> Moedas
        ctk.CTkLabel(self.tab1, text='Moeda de Origem', font=("Arial", 14, "bold")).pack() # Moeda origem
        self.selecionar_moeda_origem = ctk.CTkOptionMenu(self.tab1, 
                                                    values=list(self.dict_conversoes_disponiveis.keys()), command=self.carregar_moeda_destino)
        self.selecionar_moeda_origem.pack()
        self.selecionar_moeda_origem.set('')

        ctk.CTkLabel(self.tab1, text='Moeda de Destino', font=("Arial", 14, "bold")).pack() # Moeda Destino
        self.selecionar_moeda_destino = ctk.CTkComboBox(self.tab1, values=[''])  
        self.selecionar_moeda_destino.pack()

        self.qtd_moeda = ctk.CTkEntry(self.tab1, placeholder_text='Quantidade', width=100) # qtd
        self.qtd_moeda.pack(pady=10)
        self.converter = ctk.CTkButton(self.tab1, text='Converter', width=80, command=self.exibir_cotacao)  # Cotação
        self.converter.pack(pady=(0, 5))

        #Linha separadora e Novo Label
        ctk.CTkFrame(self.tab1, height=1, fg_color="gray", bg_color="transparent").pack(fill="x", padx=10, pady=5) # linha horizontal
        ctk.CTkLabel(self.tab1, text='Procurar Simbolo', font=('Arial', 16, 'bold')).pack(pady=(0, 5))
        self.pesquisa = ctk.CTkEntry(self.tab1, placeholder_text='Simbolo', width=110)
        self.pesquisa.pack(pady=5)
        self.botao_procurar = ctk.CTkButton(self.tab1, text='Procurar', width=80, command=self.buscar_simbolo)
        self.botao_procurar.pack()
        self.bind("<Return>", lambda event: self.botao_procurar.invoke())

        #TAB 2 -> Criptomoedas
        ctk.CTkLabel(self.tab2, text="Cryptos Populares", font=("Arial", 14, "bold")).pack()
        self.moedas = ['Bitcoin', 'Ethereum', 'Litecoin', 'Cardano', 'Solana', 'Tron', 'Dogecoin', 'Ripple', 'BinanceCoin', 'Monero']
        self.crypto_menu = ctk.CTkOptionMenu(self.tab2, values=self.moedas, command=self.atualizar_entry)
        self.crypto_menu.set('')
        self.crypto_menu.pack(pady=5)
        
        ctk.CTkLabel(self.tab2, text="Digitar Manualmente", font=("Arial", 14, "bold")).pack() #Campos de busca e botão
        self.campo_busca = ctk.CTkEntry(self.tab2, placeholder_text='Pesquisar moeda...')
        self.campo_busca.pack(pady=5)
        self.qtd_cripto = ctk.CTkEntry(self.tab2, placeholder_text='Quantidade...', width=100)
        self.qtd_cripto.pack(pady=5)

        ctk.CTkButton(self.tab2, text="Converter para Dólar", command=self.exibir_cotacao_cripto).pack(pady=5)  #Texto cotação
        self.texto_cripto = ctk.CTkLabel(self.tab2, text='', font=('Arial', 16, 'bold'))
        self.texto_cripto.pack(pady=10)

    #Comando Tab1
    def carregar_moeda_destino(self, moeda_selecionada):
        lista_moedas_destino = self.dict_conversoes_disponiveis[moeda_selecionada]
        self.selecionar_moeda_destino.configure(values=lista_moedas_destino)
        self.selecionar_moeda_destino.set(lista_moedas_destino[0])

    # Comando Tab1
    def exibir_cotacao(self):
        moeda_origem = self.selecionar_moeda_origem.get()
        moeda_destino = self.selecionar_moeda_destino.get()
        qtd = self.qtd_moeda.get()
        if qtd:
            qtd = float(qtd)
            cotacao = pegar_cotacao_moeda(moeda_origem, moeda_destino)
            if cotacao is not None: # para o caso de exceder o limite mensal e retornar None
                cotacao *= qtd
        else:
            cotacao = pegar_cotacao_moeda(moeda_origem, moeda_destino)
        if cotacao is not None: # para o caso de exceder o limite mensal e retonar None
            if cotacao>=100:
                messagebox.showinfo(message=f'{qtd} {moeda_origem} = {cotacao:,.2f} {moeda_destino}')
            else:
                messagebox.showinfo(message=f'{qtd} {moeda_origem} = {cotacao:.4f} {moeda_destino}')

    # Comando Tab1
    def buscar_simbolo(self):
        dict_nome_moedas = nome_moedas() 
        simbolo_procurado = self.pesquisa.get().upper()
        if simbolo_procurado in dict_nome_moedas:
            nome = dict_nome_moedas[simbolo_procurado]
            messagebox.showinfo(title='INFO', message=f'{simbolo_procurado} -> {nome}')
        else:
            messagebox.showwarning(title='AVISO', message='Simbolo não corresponde a nenhuma moeda!')

    # Comando Tab2
    def atualizar_entry(self, valor_selecionado):
        '''Valor Selecionado é o valor retornado ao selecionar algo no OptionMenu'''
        self.campo_busca.delete(0, ctk.END)
        self.campo_busca.insert(0, valor_selecionado)

    # Comando Tab2
    def exibir_cotacao_cripto(self):
        cripto_escolhida = self.campo_busca.get().lower()
        try:
            cotacao = cotacoes_coingecko(cripto_escolhida)
        except Exception:
            messagebox.showerror(title='ERRO', message='Moeda informada não existe!')
        else:
            qtd = self.qtd_cripto.get()
            if qtd:
                qtd = int(qtd) if qtd.isnumeric() else float(qtd)
                total = cotacao * qtd
                if total >=100:
                    self.texto_cripto.configure(text=f'{qtd} {cripto_escolhida.capitalize()}(s) = ${cotacao*qtd:,.2f}',
                                    text_color='black', 
                                    bg_color='lightgray')
                else:
                    self.texto_cripto.configure(text=f'{qtd} {cripto_escolhida.capitalize()}(s) = ${cotacao*qtd:.4f}',
                                    text_color='black', 
                                    bg_color='lightgray')
            else:
                if cotacao >=100:
                    self.texto_cripto.configure(text=f'{qtd} {cripto_escolhida.capitalize()} = ${cotacao:,.2f}', 
                                    text_color='black', 
                                    bg_color='lightgray')
                else:
                    self.texto_cripto.configure(text=f'{qtd} {cripto_escolhida.capitalize()} = ${cotacao:.4f}', 
                                    text_color='black', 
                                    bg_color='lightgray')

#### Programa principal:
app = App()
app.mainloop()

from tkinter import filedialog
from tkinter import messagebox
import xml_thread
from tkinter import (Frame, Label, Entry, Button, END, Tk)
import requests


class Application:
    def __init__(self, master=None):
        self.fonte = ('Arial', '10')
        self.fonte_maior = ('Arial', '15')
        self.a_container = Frame(master)
        self.a_container['padx'] = 30
        self.a_container.pack()

        self.b_container = Frame(master)
        self.b_container['padx'] = -10
        self.b_container.pack()

        self.c_container = Frame(master)
        self.c_container['padx'] = 30
        self.c_container.pack()

        self.d_container = Frame(master)
        self.d_container['pady'] = 5
        self.d_container.pack()

        self.e_container = Frame(master)
        self.e_container['pady'] = 10
        self.e_container.pack()

        self.label_titulo = Label(self.a_container, text='Login no sistema')
        self.label_titulo['font'] = ('Arial', '10', 'bold')
        self.label_titulo['pady'] = 30
        self.label_titulo.pack()

        self.label_nome = Label(self.b_container, text='Login/Username: ',
                                font=self.fonte)
        self.label_nome.grid(row=1, column=0, padx=1, pady=10)

        self.input_nome = Entry(self.b_container)
        self.input_nome['width'] = 25
        self.input_nome['font'] = self.fonte
        self.input_nome.grid(row=1, column=1, padx=1, pady=10)

        self.label_senha = Label(self.b_container, text='Senha/Password: ',
                                 font=self.fonte)
        self.label_senha.grid(row=2, column=0, padx=1, pady=10)

        self.input_senha = Entry(self.b_container)
        self.input_senha['width'] = 25
        self.input_senha['font'] = self.fonte
        self.input_senha['show'] = '*'
        self.input_senha.grid(row=2, column=1, padx=1, pady=10)

        self.label_product = Label(self.b_container, text='Código Produto: ',
                                   font=self.fonte)
        self.input_product = Entry(self.b_container)
        self.input_product['width'] = 25
        self.input_product['font'] = self.fonte

        self.btn_autenticar = Button(self.c_container)
        self.btn_autenticar['text'] = 'Realizar Autenticação'
        self.btn_autenticar['font'] = self.fonte
        self.btn_autenticar['width'] = 25
        self.btn_autenticar['command'] = self.login_api
        self.btn_autenticar.grid(row=3, column=0, padx=10, pady=10)

        self.brn_consultar_prod = Button(self.b_container)
        self.brn_consultar_prod['text'] = 'Consultar Produto'
        self.brn_consultar_prod['font'] = self.fonte
        self.brn_consultar_prod['width'] = 15
        self.brn_consultar_prod['command'] = self.get_input_products

        self.btn_limpar_prod = Button(self.b_container)
        self.btn_limpar_prod['text'] = 'Limpar'
        self.btn_limpar_prod['font'] = self.fonte
        self.btn_limpar_prod['width'] = 15
        self.btn_limpar_prod['command'] = self.limpar_campos

        self.label_diretorio = Label(self.c_container,
                                     text='Selecione o diretório dos .XML.')
        self.label_diretorio['font'] = self.fonte

        self.brn_cadastrar_prod = Button(self.c_container)
        self.brn_cadastrar_prod['text'] = 'Cadastrar Produto'
        self.brn_cadastrar_prod['font'] = self.fonte
        self.brn_cadastrar_prod['width'] = 25
        self.brn_cadastrar_prod['command'] = self.cadastrar_produto
        self.label_consulta = Label(self.a_container, text='Consultar Produto')
        self.label_consulta['font'] = self.fonte_maior



    # Método verificar input_senha
    def login_api(self):
        username = self.input_nome.get()
        password = self.input_senha.get()
        url = 'https://app-apisystem.herokuapp.com/login'
        payload = {'username': f'{username}', 'password': f'{password}'}

        req = requests.post(url, data=payload)
        json_login = req.json()
        global token

        if ('token' in json_login.keys()):
            token = json_login['token']
            self.btn_autenticar.destroy()
            self.label_nome.destroy()
            self.label_senha.destroy()
            self.input_nome.destroy()
            self.input_senha.destroy()
            self.label_titulo['text'] = 'Bem vindo ao sistema!'
            self.label_titulo['fg'] = '#ff0000'
            self.label_consulta.pack()
            self.label_product.grid(row=1, column=0, padx=1, pady=10)
            self.input_product.grid(row=1, column=1, padx=1, pady=10)
            self.brn_consultar_prod.grid(row=1, column=2, padx=1, pady=10)
            self.btn_limpar_prod.grid(row=1, column=3, padx=1, pady=10)
            self.label_diretorio.grid(row=3, column=0, padx=10, pady=10)
            self.brn_cadastrar_prod.grid(row=3, column=1, padx=10, pady=10)
        elif (not self.input_nome.get() or self.input_senha.get() == ''):
            messagebox.showwarning('Erro no login',
                                   'Campos login/senha vazios.')
        else:
            messagebox.showerror('Error no login',
                                 'Verfique suas credenciais.')

    def get_input_products(self):
        code = self.input_product.get()
        url = f'https://app-apisystem.herokuapp.com/produtos/{code}'
        headers = {'Authorization': f'Bearer {token}'}
        req = requests.get(url, headers=headers)
        if req.status_code == 404:
            messagebox.showerror('Consulta Produto',
                                 'Insira o código do produto.')
        elif ('Product not found' in req.json().values()):
            messagebox.showinfo('Consulta de Produtos',
                                'Produto não encontrado.')
        else:
            produc = req.json()
            msg_cod = "Código do produto {}".format(produc['product_code'])
            msg_prod = "Descrição do produto: {}"\
                .format(produc['product_name'])
            msg_ncm = "NCM do produto: {}".format(produc['product_ncm'])
            msg_unid = "Unidade do produto: {}"\
                .format(produc['product_metric'])
            msg_quant = "Quantidade do produto: {}"\
                .format(produc['product_quant'])
            msg_preco = "Valor do produto {}".format(produc['product_price'])

            msg1 = f'{msg_cod}\n{msg_prod}\n{msg_ncm}'
            msg2 = f'{msg_unid}\n{msg_quant}\n{msg_preco}'

            messagebox.showinfo('Consulta Produto', f'{msg1}\n{msg2}')


    def cadastrar_produto(self):
        filename = filedialog.askdirectory()
        if (filename):
            self.label_diretorio['text'] = filename
            path = {'dir': f'{filename}', 'xml_dir': f'{filename}/'}
            if (xml_thread.extract_products_xml(path, token)):
                messagebox.showinfo('Cadastro de produtos', 'NFe cadastradas')
                self.label_diretorio['text'] = \
                    'Selecione o diretório dos .XML.'
            else:
                messagebox.showinfo('Cadastro de produtos',
                                    'Nenhum arquivo .XML encontrado.')
                self.label_diretorio['text'] = \
                    'Selecione o diretório dos .XML.'
        else:
            messagebox.showinfo('Cadastro de produtos',
                                'Nenhum arquivo .XML encontrado.')
            self.label_diretorio['text'] = 'Selecione o diretório dos .XML.'

    def limpar_campos(self):
        self.input_product.delete(0, END)
        self.label_diretorio['text'] = 'Selecione o diretório dos .XML.'


root = Tk()
root.geometry('600x300')
Application(root)
root.mainloop()

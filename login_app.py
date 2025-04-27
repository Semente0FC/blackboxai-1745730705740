import tkinter as tk
from tkinter import messagebox
from utils import conectar_mt5, salvar_login, carregar_login, verificar_conta_real
from painel import PainelApp

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Future MT5 Trading")
        
        # Modern color scheme
        self.colors = {
            'bg_dark': '#1a1a1a',
            'bg_medium': '#2d2d2d',
            'bg_light': '#363636',
            'accent': '#3498db',
            'accent_hover': '#2980b9',
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'text': '#ffffff',
            'text_secondary': '#b3b3b3'
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        self.root.resizable(False, False)
        self.centralizar_janela(500, 600)
        self.setup_ui()
        self.carregar_login_salvo()
        
        # Bind hover events for buttons
        self.setup_hover_events()

    def centralizar_janela(self, largura, altura):
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

    def create_gradient_frame(self, parent, color1, color2):
        frame = tk.Frame(parent, bg=color1, height=2)
        return frame

    def setup_ui(self):
        # Main container with modern shadow effect
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'], padx=20, pady=20)
        main_container.place(relx=0.5, rely=0.5, anchor="center", width=450, height=500)

        # Header with gradient
        header_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        header_frame.pack(fill="x", pady=(0, 20))

        gradient = self.create_gradient_frame(header_frame, self.colors['accent'], self.colors['bg_dark'])
        gradient.pack(fill="x", pady=(0, 15))

        # Logo and title
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_dark'])
        title_frame.pack(fill="x")

        logo_label = tk.Label(
            title_frame,
            text="🌟",  # Modern star emoji as logo
            font=("Helvetica", 32),
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        )
        logo_label.pack()

        title_label = tk.Label(
            title_frame,
            text="Future MT5",
            font=("Helvetica", 24, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_dark']
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="Trading Platform",
            font=("Helvetica", 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_dark']
        )
        subtitle_label.pack()

        # Login form container
        self.card = tk.Frame(main_container, bg=self.colors['bg_medium'], padx=30, pady=30)
        self.card.pack(fill="both", expand=True)

        # Input fields
        self.entry_server = self.criar_linha_input("🌐 Servidor MT5")
        self.entry_login = self.criar_linha_input("👤 Login")
        self.entry_password = self.criar_linha_input("🔒 Senha", show="•")

        # Checkboxes container
        check_container = tk.Frame(self.card, bg=self.colors['bg_medium'])
        check_container.pack(fill="x", pady=15)

        self.check_real = tk.BooleanVar()
        self.check_save = tk.BooleanVar()

        # Modern styled checkboxes
        self.create_modern_checkbox(check_container, "Conta Real", self.check_real, side=tk.LEFT)
        self.create_modern_checkbox(check_container, "Salvar Dados", self.check_save, side=tk.RIGHT)

        # Login button with modern styling and more prominent appearance
        button_frame = tk.Frame(self.card, bg=self.colors['bg_medium'])
        button_frame.pack(fill="x", pady=(20, 10))

        self.btn_login = tk.Button(
            button_frame,
            text="CONECTAR AO MT5",
            command=self.login,
            font=("Helvetica", 14, "bold"),
            bg=self.colors['success'],
            fg=self.colors['text'],
            activebackground=self.colors['accent_hover'],
            activeforeground=self.colors['text'],
            relief="flat",
            cursor="hand2",
            pady=15,
            padx=30,
            width=25
        )
        self.btn_login.pack(expand=True, pady=10)

        # Footer with gradient
        footer_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        footer_frame.pack(fill="x", pady=(20, 0))

        gradient = self.create_gradient_frame(footer_frame, self.colors['bg_dark'], self.colors['accent'])
        gradient.pack(fill="x")

    def criar_linha_input(self, placeholder, show=None):
        container = tk.Frame(self.card, bg=self.colors['bg_medium'])
        container.pack(fill="x", pady=10)

        entry = tk.Entry(
            container,
            font=("Helvetica", 11),
            show=show,
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief="flat",
            justify="center"
        )
        entry.pack(fill="x", ipady=8)
        
        # Add placeholder
        entry.insert(0, placeholder)
        entry.config(fg=self.colors['text_secondary'])
        
        # Bind focus events for placeholder behavior
        entry.bind("<FocusIn>", lambda e: self.on_entry_focus_in(e, placeholder))
        entry.bind("<FocusOut>", lambda e: self.on_entry_focus_out(e, placeholder))
        
        return entry

    def create_modern_checkbox(self, parent, text, variable, side=tk.LEFT):
        frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        frame.pack(side=side, padx=5)
        
        cb = tk.Checkbutton(
            frame,
            text=text,
            variable=variable,
            fg=self.colors['text'],
            bg=self.colors['bg_medium'],
            selectcolor=self.colors['bg_dark'],
            activebackground=self.colors['bg_medium'],
            activeforeground=self.colors['accent'],
            font=("Helvetica", 10)
        )
        cb.pack()

    def setup_hover_events(self):
        def on_enter(e):
            self.btn_login.config(
                bg=self.colors['accent_hover'],
                relief="flat"
            )

        def on_leave(e):
            self.btn_login.config(
                bg=self.colors['success'],
                relief="flat"
            )

        self.btn_login.bind("<Enter>", on_enter)
        self.btn_login.bind("<Leave>", on_leave)

    def on_entry_focus_in(self, event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            event.widget.config(fg=self.colors['text'])
            if placeholder == "🔒 Senha":
                event.widget.config(show="•")

    def on_entry_focus_out(self, event, placeholder):
        if event.widget.get() == "":
            event.widget.insert(0, placeholder)
            event.widget.config(fg=self.colors['text_secondary'])
            if placeholder == "🔒 Senha":
                event.widget.config(show="")

    def carregar_login_salvo(self):
        dados = carregar_login()
        if dados:
            self.entry_server.delete(0, tk.END)
            self.entry_server.insert(0, dados.get("server", ""))
            self.entry_server.config(fg=self.colors['text'])
            
            self.entry_login.delete(0, tk.END)
            self.entry_login.insert(0, dados.get("login", ""))
            self.entry_login.config(fg=self.colors['text'])
            
            self.entry_password.delete(0, tk.END)
            self.entry_password.insert(0, dados.get("password", ""))
            self.entry_password.config(fg=self.colors['text'], show="•")
            
            self.check_save.set(True)

    def show_error_message(self, title, message):
        # Custom styled error message
        messagebox.showerror(title, message)

    def login(self):
        # Get values, removing placeholder if present
        server = self.entry_server.get().strip()
        if server == "🌐 Servidor MT5":
            server = ""
            
        login = self.entry_login.get().strip()
        if login == "👤 Login":
            login = ""
            
        password = self.entry_password.get().strip()
        if password == "🔒 Senha":
            password = ""

        if not server or not login or not password:
            self.show_error_message("Erro de Login", "Por favor, preencha todos os campos.")
            return

        # Update button state with loading animation
        self.btn_login.config(
            state="disabled",
            text="CONECTANDO...",
            bg=self.colors['bg_light'],
            cursor="wait"
        )
        self.root.update()

        if conectar_mt5(server, login, password):
            if self.check_real.get() and not verificar_conta_real():
                self.show_error_message(
                    "Conta Inválida",
                    "Por favor, conecte-se com uma CONTA REAL para operar."
                )
                self.btn_login.config(
                    state="normal",
                    text="CONECTAR AO MT5",
                    bg=self.colors['success'],
                    cursor="hand2"
                )
                return

            if self.check_save.get():
                salvar_login(server, login, password)

            self.root.destroy()
            painel_root = tk.Tk()
            app = PainelApp(painel_root)
            painel_root.mainloop()
        else:
            self.show_error_message(
                "Erro de Conexão",
                "Não foi possível conectar ao MetaTrader 5.\nVerifique suas credenciais."
            )
            self.entry_password.delete(0, tk.END)
            self.entry_password.insert(0, "🔒 Senha")
            self.entry_password.config(fg=self.colors['text_secondary'], show="")
            self.btn_login.config(
                state="normal",
                text="CONECTAR AO MT5",
                bg=self.colors['success'],
                cursor="hand2"
            )

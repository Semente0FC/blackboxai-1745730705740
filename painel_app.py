import tkinter as tk
from tkinter import ttk, messagebox
import MetaTrader5 as mt5
from utils import obter_saldo
from estrategia import EstrategiaTrading
from log_system import LogSystem
import threading
import time
import random
import math

class PainelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Future MT5 Trading Panel")
        
        # Spotify-like color scheme
        self.colors = {
            'bg_dark': '#121212',      # Main background
            'bg_medium': '#181818',     # Card background
            'bg_light': '#282828',      # Hover state
            'sidebar_bg': '#000000',    # Sidebar background
            'accent': '#1DB954',        # Spotify green
            'accent_hover': '#1ed760',  # Lighter green
            'success': '#1DB954',
            'danger': '#E74C3C',
            'text': '#FFFFFF',
            'text_secondary': '#B3B3B3',
            'divider': '#282828'
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        self.root.resizable(False, False)
        self.centralizar_janela(900, 650)  # Slightly larger for better spacing

        # Create main container for all widgets
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)

        # Canvas for dollar animation (place it behind all widgets)
        self.canvas = tk.Canvas(
            self.main_container,
            bg=self.colors['bg_dark'],
            highlightthickness=0,
            width=900,
            height=650
        )
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create content frame that will be above canvas
        self.content_frame = tk.Frame(
            self.main_container,
            bg=self.colors['bg_dark']
        )
        self.content_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Dollar symbols for animation
        self.dollar_symbols = []
        self.start_dollar_animation()

        self.ativo_selecionado = tk.StringVar()
        self.timeframe_selecionado = tk.StringVar()
        self.lote_selecionado = tk.StringVar(value="0.10")
        self.operando = False

        self.log_system = LogSystem()

        self.setup_styles()
        self.setup_ui()

    def centralizar_janela(self, largura, altura):
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Configure Spotify-like Combobox
        style.configure("TCombobox",
            fieldbackground=self.colors['bg_light'],
            background=self.colors['bg_light'],
            foreground=self.colors['text'],
            arrowcolor=self.colors['accent'],
            selectbackground=self.colors['accent'],
            selectforeground=self.colors['text'])
        
        style.map('TCombobox',
            fieldbackground=[('readonly', self.colors['bg_light'])],
            selectbackground=[('readonly', self.colors['accent'])],
            background=[('readonly', self.colors['bg_light'])])

        # Configure Spotify-like Entry
        style.configure("TEntry",
            fieldbackground=self.colors['bg_light'],
            foreground=self.colors['text'],
            borderwidth=0)
        
        style.map('TEntry',
            fieldbackground=[('focus', self.colors['bg_light'])],
            bordercolor=[('focus', self.colors['accent'])])

    def create_gradient_frame(self, parent, color1, color2):
        frame = tk.Frame(parent, bg=color1, height=2)
        return frame

    def create_dollar_symbol(self):
        x = random.randint(0, self.root.winfo_width())
        # More varied symbols with money theme (focusing on the most visible ones)
        symbol = random.choice(['💰', '💵', '💸', '$'])
        
        # Use a single semi-transparent color for better performance
        color = '#1DB95430'  # Spotify green with 19% opacity
        
        # Random size but keep it subtle
        size = random.randint(12, 20)
        
        # Create the symbol with random rotation
        text_id = self.canvas.create_text(
            x, -30,
            text=symbol,
            font=('Helvetica', size),
            fill=color,
            angle=random.randint(-20, 20)  # Slightly reduced rotation range
        )
        
        # Slower falling speed for better effect
        speed = random.uniform(0.5, 1.2)
        
        self.dollar_symbols.append({
            'id': text_id,
            'speed': speed,
            'angle': random.uniform(-0.5, 0.5)  # Slight rotation during fall
        })

    def animate_dollars(self):
        if not hasattr(self, 'canvas'):
            return
            
        for dollar in self.dollar_symbols[:]:
            # Move dollar symbol down with slight side movement
            self.canvas.move(
                dollar['id'],
                math.sin(time.time() * dollar['speed']) * 0.2,  # More subtle side-to-side movement
                dollar['speed']
            )
            
            # Rotate symbol slightly
            self.canvas.itemconfig(
                dollar['id'],
                angle=self.canvas.itemcget(dollar['id'], 'angle') + dollar['angle']
            )
            
            # Get position
            pos = self.canvas.coords(dollar['id'])
            
            # Remove if it's off screen
            if pos[1] > self.root.winfo_height():
                self.canvas.delete(dollar['id'])
                self.dollar_symbols.remove(dollar)
        
        # Add new dollar symbols randomly (reduced frequency)
        if random.random() < 0.015:  # 1.5% chance each frame for even fewer symbols
            self.create_dollar_symbol()
        
        # Schedule next animation frame
        self.root.after(60, self.animate_dollars)  # Slightly slower update for better performance

    def start_dollar_animation(self):
        # Create initial dollar symbols
        for _ in range(5):
            self.create_dollar_symbol()
        
        # Start animation
        self.animate_dollars()

    def setup_ui(self):
        # Create sidebar
        sidebar = tk.Frame(self.content_frame, bg=self.colors['sidebar_bg'], width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)  # Maintain width

        # Logo section
        logo_frame = tk.Frame(sidebar, bg=self.colors['sidebar_bg'], pady=20)
        logo_frame.pack(fill="x")

        logo_label = tk.Label(
            logo_frame,
            text="🚀 Future MT5",
            font=("Helvetica", 20, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['sidebar_bg']
        )
        logo_label.pack(pady=10)

        # Balance display in sidebar
        self.saldo_label = tk.Label(
            sidebar,
            text="Saldo: ---",
            font=("Helvetica", 14),
            fg=self.colors['success'],
            bg=self.colors['sidebar_bg']
        )
        self.saldo_label.pack(pady=10)

        # Navigation menu with hover effects
        menu_items = [
            ("📊 Trading", self.colors['accent'], True),
            ("📈 Análise", self.colors['text_secondary'], False),
            ("⚙️ Configurações", self.colors['text_secondary'], False)
        ]

        self.menu_buttons = []
        for text, color, active in menu_items:
            btn = tk.Button(
                sidebar,
                text=text,
                font=("Helvetica", 12),
                fg=color,
                bg=self.colors['sidebar_bg'],
                bd=0,
                relief="flat",
                activebackground=self.colors['bg_light'],
                activeforeground=self.colors['text'],
                cursor="hand2",
                anchor="w",
                padx=20,
                pady=12,
                width=25
            )
            if active:
                btn.configure(bg=self.colors['bg_light'])
            
            # Bind hover events
            btn.bind('<Enter>', lambda e, b=btn: self.on_menu_hover(b, True))
            btn.bind('<Leave>', lambda e, b=btn: self.on_menu_hover(b, False))
            
            btn.pack(fill="x", pady=1)
            self.menu_buttons.append(btn)

        # Main content area
        main_content = tk.Frame(self.content_frame, bg=self.colors['bg_dark'])
        main_content.pack(side="left", fill="both", expand=True)

        # Header in main content
        header = tk.Frame(main_content, bg=self.colors['bg_dark'], pady=20)
        header.pack(fill="x", padx=30)

        tk.Label(
            header,
            text="Trading Panel",
            font=("Helvetica", 24, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_dark']
        ).pack(anchor="w")

        # Trading options card
        options_card = tk.Frame(
            main_content,
            bg=self.colors['bg_medium'],
            padx=25,
            pady=25,
            highlightthickness=1,
            highlightbackground=self.colors['divider']
        )
        options_card.pack(fill="x", padx=30, pady=20)

        # Trading options grid
        options_grid = tk.Frame(options_card, bg=self.colors['bg_medium'])
        options_grid.pack(fill="x")

        # Asset selection with update button in one row
        asset_frame = tk.Frame(options_grid, bg=self.colors['bg_medium'])
        asset_frame.pack(fill="x", pady=5)

        tk.Label(
            asset_frame,
            text="Ativo Trading",
            font=("Helvetica", 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_medium']
        ).pack(side="left")

        self.combo_ativo = self.create_combobox(asset_frame, self.ativo_selecionado)
        self.combo_ativo.pack(side="left", padx=20)

        self.btn_atualizar_ativos = tk.Button(
            asset_frame,
            text="🔄 Atualizar",
            command=self.carregar_ativos,
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            font=("Helvetica", 10),
            activebackground=self.colors['accent'],
            activeforeground=self.colors['text'],
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        self.btn_atualizar_ativos.pack(side="left")

        # Timeframe selection
        timeframe_frame = tk.Frame(options_grid, bg=self.colors['bg_medium'])
        timeframe_frame.pack(fill="x", pady=15)

        tk.Label(
            timeframe_frame,
            text="Timeframe",
            font=("Helvetica", 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_medium']
        ).pack(side="left")

        self.combo_timeframe = self.create_combobox(
            timeframe_frame,
            self.timeframe_selecionado,
            ["M1", "M5", "M15", "M30", "H1", "H4", "D1"]
        )
        self.combo_timeframe.pack(side="left", padx=20)

        # Lot size input
        lot_frame = tk.Frame(options_grid, bg=self.colors['bg_medium'])
        lot_frame.pack(fill="x", pady=5)

        tk.Label(
            lot_frame,
            text="Tamanho do Lote",
            font=("Helvetica", 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_medium']
        ).pack(side="left")

        self.entry_lote = self.create_entry(lot_frame, self.lote_selecionado)
        self.entry_lote.pack(side="left", padx=20)

        # Control buttons in a card
        control_card = tk.Frame(
            main_content,
            bg=self.colors['bg_medium'],
            padx=25,
            pady=25,
            highlightthickness=1,
            highlightbackground=self.colors['divider']
        )
        control_card.pack(fill="x", padx=30, pady=20)

        button_frame = tk.Frame(control_card, bg=self.colors['bg_medium'])
        button_frame.pack(fill="x")

        self.btn_iniciar = tk.Button(
            button_frame,
            text="▶ Iniciar Análise com o Robô",
            command=self.iniciar_robô,
            bg=self.colors['accent'],
            fg=self.colors['text'],
            font=("Helvetica", 14, "bold"),
            activebackground=self.colors['accent_hover'],
            relief="flat",
            width=30,
            state="disabled",
            cursor="hand2",
            pady=12,
            borderwidth=0,
            highlightthickness=0
        )
        self.btn_iniciar.grid(row=0, column=0, padx=10)

        self.btn_parar = tk.Button(
            button_frame,
            text="⏹ Parar Análise",
            command=self.parar_robô,
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            font=("Helvetica", 14, "bold"),
            activebackground=self.colors['bg_dark'],
            relief="flat",
            width=25,
            cursor="hand2",
            pady=12,
            borderwidth=0,
            highlightthickness=0
        )
        self.btn_parar.grid(row=0, column=1, padx=10)

        # Logs card
        logs_card = tk.Frame(
            main_content,
            bg=self.colors['bg_medium'],
            padx=25,
            pady=25,
            highlightthickness=1,
            highlightbackground=self.colors['divider']
        )
        logs_card.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(
            logs_card,
            text="📋 Logs do Sistema",
            font=("Helvetica", 14, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_medium']
        ).pack(anchor="w", pady=(0, 10))

        text_frame = tk.Frame(logs_card, bg=self.colors['bg_light'])
        text_frame.pack(fill="both", expand=True)

        self.text_log = tk.Text(
            text_frame,
            height=15,
            width=90,
            bg=self.colors['bg_medium'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief="flat",
            font=("Consolas", 11),
            padx=15,
            pady=15,
            selectbackground=self.colors['accent'],
            selectforeground=self.colors['text']
        )
        self.text_log.pack(side="left", fill="both", expand=True)

        # Spotify-style scrollbar
        self.scrollbar = tk.Scrollbar(
            text_frame,
            command=self.text_log.yview,
            width=10,
            relief="flat",
            troughcolor=self.colors['bg_medium'],
            bg=self.colors['bg_light']
        )
        self.scrollbar.pack(side="right", fill="y", padx=2)

        self.text_log.config(yscrollcommand=self.scrollbar.set)
        self.log_system.conectar_interface(self.text_log)

        # Status bar (like Spotify's player bar)
        status_bar = tk.Frame(
            self.content_frame,
            bg=self.colors['bg_light'],
            height=30
        )
        status_bar.pack(side="bottom", fill="x")
        
        # Add status text to status bar
        status_text = tk.Label(
            status_bar,
            text="Connected to MT5",
            font=("Helvetica", 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_light']
        )
        status_text.pack(side="left", padx=10)

        self.carregar_ativos()

        # Setup variable traces
        self.ativo_selecionado.trace_add("write", self.verificar_campos)
        self.timeframe_selecionado.trace_add("write", self.verificar_campos)
        self.lote_selecionado.trace_add("write", self.verificar_campos)

        # Start balance update thread
        threading.Thread(target=self.atualizar_saldo_loop, daemon=True).start()

    def add_labeled_widget(self, parent, label_text, row, widget):
        tk.Label(
            parent,
            text=label_text,
            font=("Helvetica", 12),
            fg=self.colors['text'],
            bg=self.colors['bg_medium']
        ).grid(row=row, column=0, padx=10, pady=10, sticky="e")
        widget.grid(row=row, column=1, pady=10, sticky="w")

    def create_combobox(self, parent, variable, values=None):
        combo = ttk.Combobox(
            parent,
            textvariable=variable,
            width=30,
            values=values or [],
            style="TCombobox"
        )
        combo.configure(background=self.colors['bg_light'])
        if values:
            combo.current(1)
        return combo

    def on_menu_hover(self, button, entering):
        """Handle menu button hover effects"""
        if button not in self.menu_buttons or button == self.menu_buttons[0]:
            return
        if entering:
            button.configure(bg=self.colors['bg_light'])
        else:
            button.configure(bg=self.colors['sidebar_bg'])

    def create_entry(self, parent, variable):
        entry = tk.Entry(
            parent,
            textvariable=variable,
            font=("Helvetica", 12),
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            relief="flat",
            width=25,
            insertbackground=self.colors['text']  # Cursor color
        )
        # Add focus events for highlight effect
        entry.bind("<FocusIn>", lambda e: entry.configure(bg=self.colors['bg_dark']))
        entry.bind("<FocusOut>", lambda e: entry.configure(bg=self.colors['bg_light']))
        return entry

    def carregar_ativos(self):
        try:
            symbols = mt5.symbols_get()
            lista_ativos = [symbol.name for symbol in symbols if symbol.visible]
            self.combo_ativo['values'] = lista_ativos
            if lista_ativos:
                self.combo_ativo.current(0)
            self.log_system.logar("✅ Ativos atualizados com sucesso!")
        except Exception as e:
            self.log_system.logar(f"❌ Erro ao carregar ativos: {e}")

    def atualizar_saldo_loop(self):
        while True:
            saldo = obter_saldo()
            self.saldo_label.config(text=f"Saldo: R$ {saldo:.2f}")
            time.sleep(5)

    def verificar_campos(self, *args):
        ativo = self.ativo_selecionado.get().strip()
        timeframe = self.timeframe_selecionado.get().strip()
        lote = self.lote_selecionado.get().strip()
        if ativo and timeframe and lote:
            self.btn_iniciar.config(state="normal")
        else:
            self.btn_iniciar.config(state="disabled")

    def iniciar_robô(self):
        ativo = self.ativo_selecionado.get().strip()
        timeframe = self.timeframe_selecionado.get().strip()
        lote = self.lote_selecionado.get().strip()

        if not ativo:
            self.log_system.logar("⚠️ Selecione um ativo para operar!")
            return
        if not timeframe:
            self.log_system.logar("⚠️ Selecione um timeframe para operar!")
            return
        if not lote:
            self.lote_selecionado.set("0.10")
            lote = "0.10"
            self.log_system.logar("⚠️ Lote vazio. Valor padrão 0.10 atribuído.")

        try:
            lote_float = round(float(lote), 2)
            if lote_float <= 0:
                self.log_system.logar("⚠️ O lote deve ser maior que zero.")
                return
        except ValueError:
            messagebox.showerror("Erro de Lote", "Valor de lote inválido! Informe um número válido como 0.10")
            self.log_system.logar("❌ Erro: Lote inválido informado.")
            return

        info = mt5.symbol_info(ativo)
        if info is None:
            self.log_system.logar(f"❌ Ativo {ativo} não encontrado no MetaTrader 5.")
            return
        if not info.visible:
            self.log_system.logar(f"⚠️ Ativo {ativo} não está visível no MT5. Abra o ativo no terminal!")
            return
        if info.trade_mode != mt5.SYMBOL_TRADE_MODE_FULL:
            self.log_system.logar(f"❌ Ativo {ativo} não está liberado para operar (modo inválido)!")
            return

        tick = mt5.symbol_info_tick(ativo)
        if tick is None:
            self.log_system.logar(f"❌ Não foi possível obter preços do ativo {ativo}.")
            return

        spread = (tick.ask - tick.bid) / info.point
        spread_maximo_aceito = 50

        if spread > spread_maximo_aceito:
            self.log_system.logar(
                f"⚠️ Spread do ativo {ativo} está muito alto ({spread:.1f} pontos). Análise bloqueada.")
            return

        if tick.bid == 0 or tick.ask == 0:
            self.log_system.logar(f"⚠️ Mercado para o ativo {ativo} está FECHADO. Análise bloqueada.")
            return
        else:
            self.log_system.logar(f"✅ Mercado para o ativo {ativo} está ABERTO.")

        self.operando = True
        self.log_system.logar(
            f"✅ Ambiente OK. Iniciando análise no ativo {ativo}, timeframe {timeframe}, lote {lote_float}. Spread atual: {spread:.1f} pontos.")
        self.estrategia = EstrategiaTrading(ativo, timeframe, lote_float, self.log_system)
        threading.Thread(target=self.estrategia.executar, daemon=True).start()

    def parar_robô(self):
        self.operando = False
        if hasattr(self, 'estrategia'):
            self.estrategia.parar()
        self.log_system.logar("🛑 Análise parada.")

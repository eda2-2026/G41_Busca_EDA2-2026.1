import os
import json
import sys
from pathlib import Path
import qdarktheme
from datetime import datetime
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import (
    QMainWindow, QCalendarWidget, QVBoxLayout,
    QGridLayout, QFormLayout, QWidget, QFrame,
    QApplication, QPushButton, QLabel, QDialog,
    QLineEdit, QSpinBox, QDateEdit, QListWidget,
    QDialogButtonBox, QMessageBox, QSplitter,
    QStackedWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QHBoxLayout, QAbstractItemView
)

CAMINHO_DB_FILES = Path(__file__).parent / "db_files"
IDS_ALUNOS = os.path.join(CAMINHO_DB_FILES, "id_alunos.json")
INFO_ALUNOS = os.path.join(CAMINHO_DB_FILES, "info_alunos.json")
IDS_LIVROS = os.path.join(CAMINHO_DB_FILES, "id_livros.json")
INFO_LIVROS = os.path.join(CAMINHO_DB_FILES, "info_livros.json")
EMPRESTIMOS = os.path.join(CAMINHO_DB_FILES, "emprestimos.json")
ID_EMPRESTIMO = os.path.join(CAMINHO_DB_FILES, "id_emprestimo.json")
HISTORICO_DEVOLUCOES = os.path.join(CAMINHO_DB_FILES, "historico_devolucoes.json")

class Aluno:
    def __init__(self, id, nome, idade, serie, turno, contato, endereco):
        self.id = id
        self.nome = nome.title()
        self.idade = idade
        self.serie = serie
        self.turno = turno.title()
        self.contato = contato
        self.endereco = endereco.title()

class Livro:
    def __init__(self, numeracao, titulo, genero, autor, editora, quantidade):
        self.numeracao = numeracao
        self.titulo = titulo.capitalize()
        self.genero = genero.capitalize()
        self.autor = autor.capitalize()
        self.editora = editora.capitalize()
        self.quantidade = quantidade

class Biblioteca:
    def __init__(self):
        self.id_alunos = self.importacao(IDS_ALUNOS)
        self.info_alunos = self.importacao(INFO_ALUNOS)
        self.id_livros = self.importacao(IDS_LIVROS)
        self.info_livros = self.importacao(INFO_LIVROS)
        self.emprestimos = self.importacao(EMPRESTIMOS)
        self.id_emprestimo = self.importacao(ID_EMPRESTIMO)
        self.historico_devolucoes = self.importacao(HISTORICO_DEVOLUCOES)
        
        # Hooks de índice para implementação futura
        self.bst = None
        self.indice_invertido = None
        self.buscador_fuzzy = None
        self.motor = None
        
        self.inicializar_indices()

    def importacao(self, caminho: str):
        with open(caminho, "r", encoding="utf-8-sig") as arq:
            return json.load(arq)

    def exportacao(self, caminho: str, dados: dict):
        with open(caminho, "w", encoding="utf-8") as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=2)

    def inicializar_indices(self):
        from indices.bst_livros import BSTBiblioteca
        from indices.indice_invertido import IndiceInvertido
        from indices.busca_aproximada import BuscaAproximada
        from indices.motor_busca import MotorBusca

        livros_lista = list(self.info_livros.values())
        
        self.bst = BSTBiblioteca()
        self.bst.construir_de_lista(livros_lista)
        print(f"[BST] {len(livros_lista)} livros indexados.")

        self.indice_invertido = IndiceInvertido()
        self.indice_invertido.construir(livros_lista)
        print(f"[Invertido] {len(self.indice_invertido.vocabulario())} tokens.")

        self.buscador_fuzzy = BuscaAproximada(self.indice_invertido)
        print("[Fuzzy] Pronto.")

        self.motor = MotorBusca(self)
        print("[Motor] Todos os indices inicializados.")

    def cadastra_aluno(self, nome, idade, serie, turno, contato, endereco):
        _id = str(len(self.id_alunos))
        if _id in self.id_alunos:
            return False
        aluno = Aluno(_id, nome, idade, serie, turno, contato, endereco)
        self.id_alunos.append(_id)
        self.info_alunos[_id] = aluno.__dict__
        self.exportacao(IDS_ALUNOS, self.id_alunos)
        self.exportacao(INFO_ALUNOS, self.info_alunos)
        return self.info_alunos[_id]

    def cadastra_livro(self, numeracao, titulo, genero, autor, editora, qtd):
        livro = Livro(numeracao, titulo, genero, autor, editora, int(qtd) if isinstance(qtd, str) else qtd)
        self.info_livros[numeracao] = livro.__dict__
        self.id_livros.append(numeracao)
        self.exportacao(IDS_LIVROS, self.id_livros)
        self.exportacao(INFO_LIVROS, self.info_livros)
        if self.bst:
            self.bst.inserir(self.info_livros[numeracao])
        if self.indice_invertido:
            self.indice_invertido.atualizar(self.info_livros[numeracao])
        return self.info_livros[numeracao]

    def altera_aluno(self, _id, nome, idade, serie, turno, contato, endereco):
        if _id not in self.id_alunos:
            return None
        aluno = Aluno(_id, nome, idade, serie, turno, contato, endereco)
        self.info_alunos[_id] = aluno.__dict__
        self.exportacao(INFO_ALUNOS, self.info_alunos)
        return self.info_alunos[_id]

    def altera_livro(self, numeracao, titulo, genero, autor, editora, qtd):
        if numeracao not in self.id_livros:
            return None
        livro = Livro(numeracao, titulo, genero, autor, editora, qtd)
        self.info_livros[numeracao] = livro.__dict__
        self.exportacao(INFO_LIVROS, self.info_livros)
        if self.bst:
            self.bst.inserir(self.info_livros[numeracao])
        if self.indice_invertido:
            self.indice_invertido.atualizar(self.info_livros[numeracao])
        return self.info_livros[numeracao]

    def fazer_emprestimo(self, _id, livro, devo):
        chave = str(datetime.now().microsecond)
        self.emprestimos[chave] = {
            "aluno": self.info_alunos[_id],
            "livro": livro.title(),
            "devolucao": devo
        }
        self.id_emprestimo[chave] = _id
        self.exportacao(EMPRESTIMOS, self.emprestimos)
        self.exportacao(ID_EMPRESTIMO, self.id_emprestimo)
        return chave, self.emprestimos[chave]

    def fazer_devolucao(self, chave):
        emprestimo = self.emprestimos.get(chave)
        if not emprestimo:
            return

        # Busca nome do aluno
        aluno_info = emprestimo.get("aluno", {})
        if isinstance(aluno_info, dict):
            nome_aluno = aluno_info.get("nome", "Desconhecido")
        else:
            nome_aluno = str(aluno_info)

        # Salva no histórico de devoluções
        chave_devolucao = f"DEV-{chave}"
        self.historico_devolucoes[chave_devolucao] = {
            "chave_emprestimo": chave,
            "livro": emprestimo.get("livro", ""),
            "aluno": nome_aluno,
            "data_devolucao": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        self.exportacao(HISTORICO_DEVOLUCOES, self.historico_devolucoes)

        # Remove o empréstimo ativo
        self.emprestimos.pop(chave)
        self.id_emprestimo.pop(chave)
        self.exportacao(EMPRESTIMOS, self.emprestimos)
        self.exportacao(ID_EMPRESTIMO, self.id_emprestimo)
 
class JanelaPrincipal(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Sistema de Biblioteca")
        
        # Instancia biblioteca
        self.b1 = Biblioteca()
        
        # Cria janelas secundárias
        self.janelaCA = JanelaCadastraAluno(self.b1)
        self.janelaCL = JanelaCadastroLivro(self.b1)
        self.janelaAA = JanelaAteraAluno(self.b1)
        self.janelaAL = JanelaAlteraLivro(self.b1)
        self.janelaEP = JanelaEmprestimo(self.b1)
        self.janelaDV = JanelaDevolucao(self.b1)
        
        # Cria layout principal com splitter
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Cria sidebar (painel esquerdo)
        self.sidebar = self._criar_sidebar()
        
        # Cria stacked widget para os painéis (painel direito)
        self.stacked = QStackedWidget()
        self.painel_acervo = self._criar_painel_acervo()
        self.painel_alunos = self._criar_painel_alunos()
        self.painel_emprestimos = self._criar_painel_emprestimos()
        self.painel_devolucoes = self._criar_painel_devolucoes()
        
        self.stacked.addWidget(self.painel_acervo)        # 0
        self.stacked.addWidget(self.painel_alunos)        # 1
        self.stacked.addWidget(self.painel_emprestimos)   # 2
        self.stacked.addWidget(self.painel_devolucoes)    # 3
        
        # Adiciona sidebar e stacked ao splitter
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.stacked)
        self.splitter.setSizes([220, 1280])
        
        self.setCentralWidget(self.splitter)
        self.config_style()
        self._conectar_atualizacao_dialogos()
        self._atualizar_tabela_acervo()
        self._atualizar_tabela_alunos()
        self._atualizar_tabela_emprestimos()
        self._atualizar_cards()
    
    def _criar_sidebar(self) -> QFrame:
        """Cria sidebar com navegação"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo real do sistema
        logo_label = QLabel()
        pixmap = QPixmap("img/logo.png")
        pixmap = pixmap.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        # Texto abaixo da logo
        
        separador1 = QFrame()
        separador1.setFrameShape(QFrame.HLine)
        separador1.setStyleSheet("background: rgba(173, 73, 225, 0.2);")
        layout.addWidget(separador1)
        
        # Seção ACERVO
        secao_acervo = QLabel("ACERVO")
        secao_acervo.setObjectName("section-label")
        secao_acervo.setStyleSheet(
            "color: rgba(173, 73, 225, 0.45); font-size: 10px; "
            "letter-spacing: 2px; padding: 12px 16px 4px; font-weight: bold;"
        )
        layout.addWidget(secao_acervo)
        
        # Botões de navegação ACERVO
        self.btn_acervo = self._criar_botao_nav("📚 Acervo de Livros", True)
        self.btn_acervo.clicked.connect(lambda: self._switch_panel(0, self.btn_acervo))
        layout.addWidget(self.btn_acervo)
        
        self.btn_alunos = self._criar_botao_nav("👥 Alunos")
        self.btn_alunos.clicked.connect(lambda: self._switch_panel(1, self.btn_alunos))
        layout.addWidget(self.btn_alunos)
        
        self.btn_emprestimos = self._criar_botao_nav("📤 Empréstimos")
        self.btn_emprestimos.clicked.connect(lambda: self._switch_panel(2, self.btn_emprestimos))
        layout.addWidget(self.btn_emprestimos)
        
        self.btn_devolucoes = self._criar_botao_nav("📥 Devoluções")
        self.btn_devolucoes.clicked.connect(lambda: self._switch_panel(3, self.btn_devolucoes))
        layout.addWidget(self.btn_devolucoes)
        
        self.nav_buttons = [self.btn_acervo, self.btn_alunos, self.btn_emprestimos, self.btn_devolucoes]
        
        separador2 = QFrame()
        separador2.setFrameShape(QFrame.HLine)
        separador2.setStyleSheet("background: rgba(173, 73, 225, 0.2); margin: 8px 0;")
        layout.addWidget(separador2)
        
        # Seção CADASTRO
        secao_cadastro = QLabel("CADASTRO")
        secao_cadastro.setObjectName("section-label")
        secao_cadastro.setStyleSheet(
            "color: rgba(173, 73, 225, 0.45); font-size: 10px; "
            "letter-spacing: 2px; padding: 12px 16px 4px; font-weight: bold;"
        )
        layout.addWidget(secao_cadastro)
        
        btn_novo_livro = self._criar_botao_nav("➕ Novo Livro")
        btn_novo_livro.clicked.connect(self.janelaCL.show)
        layout.addWidget(btn_novo_livro)
        
        btn_novo_aluno = self._criar_botao_nav("➕ Novo Aluno")
        btn_novo_aluno.clicked.connect(self.janelaCA.show)
        layout.addWidget(btn_novo_aluno)
        
        layout.addStretch()
        
        return sidebar
    
    def _criar_botao_nav(self, texto: str, ativo: bool = False) -> QPushButton:
        """Cria um botão de navegação da sidebar"""
        btn = QPushButton(texto)
        btn.setObjectName("nav-btn")
        btn.setProperty("active", ativo)
        btn.setFlat(True)
        btn.setStyleSheet(
            """
            QPushButton#nav-btn {
                background: transparent;
                border: none;
                border-left: 2px solid transparent;
                padding: 9px 16px 9px 14px;
                text-align: left;
                color: rgba(255,255,255,0.55);
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton#nav-btn:hover {
                background: rgba(173, 73, 225, 0.08);
                color: rgba(255,255,255,0.85);
            }
            QPushButton#nav-btn[active="true"] {
                background: rgba(173, 73, 225, 0.12);
                border-left: 2px solid #AD49E1;
                color: #c97ff0;
            }
            """
        )
        return btn
    
    def _switch_panel(self, index: int, btn: QPushButton):
        """Troca entre painéis e atualiza estilo do botão"""
        # Desativa todos os botões
        for b in self.nav_buttons:
            b.setProperty("active", False)
            b.style().unpolish(b)
            b.style().polish(b)
        
        # Ativa botão clicado
        btn.setProperty("active", True)
        btn.style().unpolish(btn)
        btn.style().polish(btn)
        
        # Troca painel
        self.stacked.setCurrentIndex(index)
        
        # Recarrega dados se necessário
        if index == 0:
            self._atualizar_tabela_acervo()
        elif index == 1:
            self._atualizar_tabela_alunos()
        elif index == 2:
            self._atualizar_tabela_emprestimos()
        elif index == 3:
            self._atualizar_tabela_devolucoes()
        self._atualizar_cards()
        

        self.botoes_box.rejected.connect(self.reject)

    def faz_slot(self, func, *args):
        def slot():
            n, i, s, t, c, e = args
            if self.verifica_campos(n, i, s, t, c, e):
                msg = func(n.text(), str(i.value()), s.text(), t.text(), c.text(), e.text())
                for b in args:
                    b.clear()
                faz_msg_box("Cadastro realizado!", str(msg), False)
            else:
                faz_msg_box("Erro", "Preencha todos os campos corretamente.", True)

        return slot

    def verifica_campos(self, nome, idade, serie, turno, contato, endereco):
        if not nome.text() or not serie.text() or not turno.text() or not contato.text() or not endereco.text():
            return False
        if idade.value() <= 0:
            return False
        return True


#Configurações da janela de cadastro dos livros 
class JanelaCadastroLivro(QDialog):
    def __init__(self, biblioteca: Biblioteca, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Cadastro de Livro")
        self.setMinimumSize(900, 350)
        layoutcl = QFormLayout()
        self.setLayout(layoutcl)

        layoutcl.addRow("Numeração:", numeracao := QSpinBox())
        numeracao.setRange(0, 9999999)

        layoutcl.addRow("Titulo Livro:", titulo := QLineEdit())
        layoutcl.addRow("Genero:", genero := QLineEdit())
        layoutcl.addRow("Autor:", autor := QLineEdit())
        layoutcl.addRow("Editora:", editora := QLineEdit())
        layoutcl.addRow("Quantidade:", qtd := QSpinBox())
        qtd.setRange(0, 9999)

        b_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layoutcl.addWidget(b_box)

        b_box.accepted.connect(
            self.faz_slot(
                biblioteca.cadastra_livro,
                numeracao, titulo, genero, autor, editora, qtd
            )
        )
        b_box.rejected.connect(self.reject)

    def faz_slot(self, func, *args):
        def slot():
            n, t, g, a, e, q = args
            if self.verifica_campos(*args):  
                msg = func(
                    n.text(), t.text(), g.text(), a.text(), e.text(), q.value()
                )
                for b in args:
                    b.clear()
                faz_msg_box(
                    "Cadastro Realizado!", str(msg), False
                )
        return slot

    def verifica_campos(self, *args):
        n, t, g, a, e, q = args
        if not n.text() or not t.text() or not g.text() or not a.text() or not e.text():
            faz_msg_box("Erro", "Todos os campos precisam ser preenchidos.", True)
            return False
        if q.value() <= 0:
            faz_msg_box("Erro", "A quantidade deve ser maior que zero.", True)
            return False
        return True

def faz_msg_box(titulo, mensagem, erro=False):
    msg = QMessageBox()
    msg.setWindowTitle(titulo)
    msg.setText(mensagem)
    if erro:
        msg.setIcon(QMessageBox.Critical)  
    else:
        msg.setIcon(QMessageBox.Information)  
    msg.exec()

class JanelaAteraAluno(QDialog):
    def __init__(self, biblioteca: Biblioteca, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Altera Cadastro - Aluno")
        self.setMinimumSize(900, 350)
        layoutaa = QFormLayout()
        self.setLayout(layoutaa)

        campo_texto = [_id := QSpinBox(), nome := QLineEdit(),
                       idade := QSpinBox(), serie := QLineEdit(),
                       turno := QLineEdit(), contato := QLineEdit(),
                       endereco := QLineEdit()]

        _id.setRange(0, 999999)
        titulos = ["ID", "Nome Aluno", "Idade", "Série", "Turno", "Contato", "Endereço"]

        for titulo, campo in zip(titulos, campo_texto):
            layoutaa.addRow(str(titulo), campo)

        self.botoes_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layoutaa.addWidget(self.botoes_box)

        self.botoes_box.accepted.connect(self.faz_slot(
            biblioteca.altera_aluno,
            _id, nome, idade, serie, turno, contato, endereco
        ))

        self.botoes_box.rejected.connect(self.reject)

    def faz_slot(self, func, *args: Botao):
        def slot():
            __id, n, i, s, t, c, e = args
            if self.verifica_campos(*args):
                aluno_id = str(__id.value())
                msg = func(aluno_id, n.text(), i.text(), s.text(), t.text(), c.text(), e.text())

                if msg is None:
                    faz_msg_box("ERRO!", "O ID digitado não existe.", True)
                else:
                    for b in args:
                        b.clear()
                    faz_msg_box("Cadastro atualizado!", str(msg), False)

        return slot

    def verifica_campos(self, *args):
        nome, idade, serie, turno, contato, endereco = args[1:]

        if not nome.text() or not serie.text() or not turno.text() or not contato.text() or not endereco.text():
            return False
        if idade.value() <= 0:
            return False
        return True


#Configurações da janela de alteção dos livros 
class JanelaAlteraLivro(QDialog):
    def __init__(self, biblioteca: Biblioteca, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Altera Cadastro - Livro")
        self.setMinimumSize(900, 350)
        layoutcl = QFormLayout()
        self.setLayout(layoutcl)

        layoutcl.addRow("Numeração:", numeracao := QSpinBox())
        numeracao.setRange(0, 9999999)

        layoutcl.addRow("Titulo Livro:", titulo := QLineEdit())
        layoutcl.addRow("Genero:", genero := QLineEdit())
        layoutcl.addRow("Autor:", autor := QLineEdit())
        layoutcl.addRow("Editora:", editora := QLineEdit())
        layoutcl.addRow("Quantidade:", qtd := QSpinBox())
        qtd.setRange(0, 999)

        b_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layoutcl.addWidget(b_box)

        b_box.accepted.connect(
            self.faz_slot(
                biblioteca.altera_livro,
                numeracao, titulo, genero, autor, editora, qtd
            )
        )
        b_box.rejected.connect(self.reject)

    def faz_slot(self, func, *args):
        def slot():
            n, t, g, a, e, q = args
            if self.verifica_campos(*args): 
                msg = func(
                    n.text(), t.text(), g.text(), a.text(), e.text(), q.value()
                )
                for b in args:
                    b.clear()
                if msg is None:
                    faz_msg_box("ERRO!", "ID não encontrado.", True)
                    return
                # Exibe a mensagem de sucesso após a alteração
                faz_msg_box("Cadastro Alterado!", "O livro foi alterado com sucesso.", False) 

        return slot

    def verifica_campos(self, *args):
        n, t, g, a, e, q = args
        if not n.text() or not t.text() or not g.text() or not a.text() or not e.text():
            faz_msg_box("Erro", "Todos os campos precisam ser preenchidos.", True)
            return False
        if q.value() <= 0:
            faz_msg_box("Erro", "A quantidade deve ser maior que zero.", True)
            return False
        return True

def faz_msg_box(titulo, mensagem, erro=False):
    msg = QMessageBox()
    msg.setWindowTitle(titulo)
    msg.setText(mensagem)  
    if erro:
        msg.setIcon(QMessageBox.Critical)  
    else:
        msg.setIcon(QMessageBox.Information)  
    msg.exec()


#Configurações da janela de Emprestimo
class JanelaEmprestimo(QDialog):
    def __init__(self, biblioteca: Biblioteca, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.biblioteca = biblioteca  
        self.setWindowTitle("Empréstimo de Livro")
        self.setMinimumSize(500, 200)

        # Adicionando os campos necessários
        self._id = QLineEdit() 
        self.livro = QLineEdit()  
        self.data = QDateEdit() 
        self.data.setCalendarPopup(True)

        # Layout
        layout = QFormLayout()
        layout.addRow("ID do Aluno:", self._id)
        layout.addRow("Título do Livro:", self.livro)
        layout.addRow("Data de Devolução:", self.data)
        self.setLayout(layout)

        # Botões
        b_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        b_box.accepted.connect(self.realiza_emprestimo)
        b_box.rejected.connect(self.reject)
        layout.addWidget(b_box)

    def verifica_campos(self, _id, livro, data):
        """Verificar se todos os campos foram preenchidos."""
        if not _id or not livro or not data:
            return False
        return True

    def realiza_emprestimo(self):
        """Processa o empréstimo após a verificação dos campos."""
        _id = self._id.text()  # Obtendo o valor do campo de ID
        livro = self.livro.text()  
        data = self.data.date().toString('yyyy-MM-dd')  

        # Verifica se os campos estão preenchidos corretamente
        if self.verifica_campos(_id, livro, data):
            try:
                chave, msg = self.biblioteca.fazer_emprestimo(_id, livro, data)
                faz_msg_box("Empréstimo realizado!", f"Chave do empréstimo: {chave}", False)
            except KeyError as e:
                faz_msg_box("Erro", f"ID de aluno não encontrado: {e}", True)
            except ValueError as e:
                faz_msg_box("Erro", str(e), True)
        else:
            faz_msg_box("Erro", "Todos os campos precisam ser preenchidos!", True)

class JanelaDevolucao(QDialog):
    def __init__(self, biblioteca: Biblioteca, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Devolução")
        self.setMinimumSize(600, 350)

        layoutdv = QFormLayout()
        self.setLayout(layoutdv)

        self.chave = QSpinBox()
        self.chave.setRange(0, 9999999)
        layoutdv.addRow("Chave da Devolução:", self.chave)

        b_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layoutdv.addWidget(b_box)

        b_box.accepted.connect(lambda: self.faz_slot(biblioteca.fazer_devolucao)())
        b_box.rejected.connect(self.reject)

    def faz_slot(self, func):
        def slot():
            chave_value = self.chave.value()  
            try:
                func(str(chave_value))  
                self.chave.clear()  
                faz_msg_box("Devolução Realizada!", "Devolução bem sucedida.", False)
            except KeyError:
                faz_msg_box("Falha!", "Devolução mal sucedida.\nERRO: CHAVE NÃO ENCONTRADA", True)
        return slot

if __name__ == "__main__":
    app = QApplication(sys.argv)

    janelaCentral = JanelaPrincipal()

    janelaCentral.show()
    sys.exit(app.exec())  
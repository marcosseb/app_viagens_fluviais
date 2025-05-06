import sqlite3
from datetime import datetime

class GerenciadorPassagensBarco:
    def __init__(self, db_name='passagens_barco.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()
    
    def criar_tabelas(self):
        """Cria todas as tabelas necessárias no banco de dados"""
        
        # Tabela de Localizações (Portos)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS localizacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL,
            pais TEXT NOT NULL,
            codigo_porto TEXT UNIQUE
        )
        ''')
        
        # Tabela de Embarcações
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS embarcacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            capacidade INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            registro TEXT UNIQUE NOT NULL
        )
        ''')
        
        # Tabela de Passageiros
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS passageiros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            data_nascimento DATE,
            telefone TEXT,
            email TEXT,
            endereco TEXT
        )
        ''')
        
        # Tabela de Rotas
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS rotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origem_id INTEGER NOT NULL,
            destino_id INTEGER NOT NULL,
            distancia_km REAL,
            duracao_estimada_minutos INTEGER,
            FOREIGN KEY (origem_id) REFERENCES localizacoes(id),
            FOREIGN KEY (destino_id) REFERENCES localizacoes(id),
            CHECK (origem_id != destino_id)
        )
        ''')
        
        # Tabela de Horários
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rota_id INTEGER NOT NULL,
            embarcacao_id INTEGER NOT NULL,
            data_partida DATETIME NOT NULL,
            data_chegada_estimada DATETIME NOT NULL,
            status TEXT DEFAULT 'programado',
            FOREIGN KEY (rota_id) REFERENCES rotas(id),
            FOREIGN KEY (embarcacao_id) REFERENCES embarcacoes(id)
        )
        ''')
        
        # Tabela de Passagens
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS passagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            horario_id INTEGER NOT NULL,
            passageiro_id INTEGER NOT NULL,
            data_compra DATETIME DEFAULT CURRENT_TIMESTAMP,
            preco REAL NOT NULL,
            assento TEXT,
            status TEXT DEFAULT 'confirmado',
            codigo_bilhete TEXT UNIQUE NOT NULL,
            FOREIGN KEY (horario_id) REFERENCES horarios(id),
            FOREIGN KEY (passageiro_id) REFERENCES passageiros(id)
        )
        ''')
        
        # Tabela de Tripulação (opcional)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tripulacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cargo TEXT NOT NULL,
            embarcacao_id INTEGER,
            horario_id INTEGER,
            FOREIGN KEY (embarcacao_id) REFERENCES embarcacoes(id),
            FOREIGN KEY (horario_id) REFERENCES horarios(id)
        )
        ''')
        
        self.conn.commit()
    
    # Métodos CRUD para Localizações
    def adicionar_localizacao(self, nome, cidade, estado, pais, codigo_porto):
        self.cursor.execute('''
        INSERT INTO localizacoes (nome, cidade, estado, pais, codigo_porto)
        VALUES (?, ?, ?, ?, ?)
        ''', (nome, cidade, estado, pais, codigo_porto))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def listar_localizacoes(self):
        self.cursor.execute('SELECT * FROM localizacoes')
        return self.cursor.fetchall()
    
    # Métodos CRUD para Embarcações
    def adicionar_embarcacao(self, nome, capacidade, tipo, registro):
        self.cursor.execute('''
        INSERT INTO embarcacoes (nome, capacidade, tipo, registro)
        VALUES (?, ?, ?, ?)
        ''', (nome, capacidade, tipo, registro))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def listar_embarcacoes(self):
        self.cursor.execute('SELECT * FROM embarcacoes')
        return self.cursor.fetchall()
    
    # Métodos CRUD para Passageiros
    def adicionar_passageiro(self, nome, cpf, data_nascimento=None, telefone=None, email=None, endereco=None):
        self.cursor.execute('''
        INSERT INTO passageiros (nome, cpf, data_nascimento, telefone, email, endereco)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, cpf, data_nascimento, telefone, email, endereco))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def buscar_passageiro_por_cpf(self, cpf):
        self.cursor.execute('SELECT * FROM passageiros WHERE cpf = ?', (cpf,))
        return self.cursor.fetchone()
    
    # Métodos CRUD para Rotas
    def adicionar_rota(self, origem_id, destino_id, distancia_km=None, duracao_estimada_minutos=None):
        self.cursor.execute('''
        INSERT INTO rotas (origem_id, destino_id, distancia_km, duracao_estimada_minutos)
        VALUES (?, ?, ?, ?)
        ''', (origem_id, destino_id, distancia_km, duracao_estimada_minutos))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def listar_rotas(self):
        self.cursor.execute('''
        SELECT r.id, o.nome, d.nome, r.distancia_km, r.duracao_estimada_minutos 
        FROM rotas r
        JOIN localizacoes o ON r.origem_id = o.id
        JOIN localizacoes d ON r.destino_id = d.id
        ''')
        return self.cursor.fetchall()
    
    # Métodos CRUD para Horários
    def adicionar_horario(self, rota_id, embarcacao_id, data_partida, data_chegada_estimada, status='programado'):
        self.cursor.execute('''
        INSERT INTO horarios (rota_id, embarcacao_id, data_partida, data_chegada_estimada, status)
        VALUES (?, ?, ?, ?, ?)
        ''', (rota_id, embarcacao_id, data_partida, data_chegada_estimada, status))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def listar_horarios(self):
        self.cursor.execute('''
        SELECT h.id, o.nome, d.nome, e.nome, h.data_partida, h.data_chegada_estimada, h.status
        FROM horarios h
        JOIN rotas r ON h.rota_id = r.id
        JOIN localizacoes o ON r.origem_id = o.id
        JOIN localizacoes d ON r.destino_id = d.id
        JOIN embarcacoes e ON h.embarcacao_id = e.id
        ''')
        return self.cursor.fetchall()
    
    # Métodos CRUD para Passagens
    def vender_passagem(self, horario_id, passageiro_id, preco, assento=None, status='confirmado'):
        codigo_bilhete = f"BILH{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.cursor.execute('''
        INSERT INTO passagens (horario_id, passageiro_id, preco, assento, status, codigo_bilhete)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (horario_id, passageiro_id, preco, assento, status, codigo_bilhete))
        self.conn.commit()
        return codigo_bilhete
    
    def listar_passagens(self):
        self.cursor.execute('''
        SELECT p.codigo_bilhete, ps.nome, o.nome, d.nome, h.data_partida, e.nome, p.preco, p.status
        FROM passagens p
        JOIN horarios h ON p.horario_id = h.id
        JOIN passageiros ps ON p.passageiro_id = ps.id
        JOIN rotas r ON h.rota_id = r.id
        JOIN localizacoes o ON r.origem_id = o.id
        JOIN localizacoes d ON r.destino_id = d.id
        JOIN embarcacoes e ON h.embarcacao_id = e.id
        ''')
        return self.cursor.fetchall()
    
    def fechar_conexao(self):
        self.conn.close()

# Exemplo de uso do sistema
if __name__ == "__main__":
    gerenciador = GerenciadorPassagensBarco()
    
    # Adicionando dados de exemplo
    print("Populando banco de dados com dados de exemplo...")
    
    # Localizações
    porto_santos = gerenciador.adicionar_localizacao("Porto de Santos", "Santos", "SP", "Brasil", "BRSTS")
    porto_rio = gerenciador.adicionar_localizacao("Porto do Rio de Janeiro", "Rio de Janeiro", "RJ", "Brasil", "BRRIO")
    porto_angra = gerenciador.adicionar_localizacao("Porto de Angra dos Reis", "Angra dos Reis", "RJ", "Brasil", "BRANG")
    porto_ilhabela = gerenciador.adicionar_localizacao("Porto de Ilhabela", "Ilhabela", "SP", "Brasil", "BRILH")
    
    # Embarcações
    balsa = gerenciador.adicionar_embarcacao("Balsa Atlântico", 200, "Balsa", "BR123456")
    lancha = gerenciador.adicionar_embarcacao("Lancha Veloz", 50, "Lancha", "BR654321")
    catamara = gerenciador.adicionar_embarcacao("Catamarã Estrela", 150, "Catamarã", "BR987654")
    
    # Passageiros
    gerenciador.adicionar_passageiro("João Silva", "12345678901", "1980-05-15", "(11)9999-8888", "joao@email.com")
    gerenciador.adicionar_passageiro("Maria Souza", "98765432109", "1992-08-20", "(21)7777-6666", "maria@email.com")
    gerenciador.adicionar_passageiro("Carlos Oliveira", "45678912304", "1975-11-30", "(13)5555-4444", "carlos@email.com")
    
    # Rotas
    rota_santos_rio = gerenciador.adicionar_rota(porto_santos, porto_rio, 350, 480)
    rota_rio_angra = gerenciador.adicionar_rota(porto_rio, porto_angra, 150, 120)
    rota_santos_ilha = gerenciador.adicionar_rota(porto_santos, porto_ilhabela, 200, 180)
    
    # Horários
    partida_santos_rio = datetime(2023, 12, 1, 8, 0, 0)
    chegada_santos_rio = datetime(2023, 12, 1, 16, 0, 0)
    horario1 = gerenciador.adicionar_horario(rota_santos_rio, balsa, partida_santos_rio, chegada_santos_rio)
    
    partida_rio_angra = datetime(2023, 12, 2, 9, 30, 0)
    chegada_rio_angra = datetime(2023, 12, 2, 11, 30, 0)
    horario2 = gerenciador.adicionar_horario(rota_rio_angra, lancha, partida_rio_angra, chegada_rio_angra)
    
    partida_santos_ilha = datetime(2023, 12, 3, 10, 0, 0)
    chegada_santos_ilha = datetime(2023, 12, 3, 13, 0, 0)
    horario3 = gerenciador.adicionar_horario(rota_santos_ilha, catamara, partida_santos_ilha, chegada_santos_ilha)
    
    # Passagens
    bilhete1 = gerenciador.vender_passagem(horario1, 1, 150.00, "A12")
    bilhete2 = gerenciador.vender_passagem(horario2, 2, 80.00, "B05")
    bilhete3 = gerenciador.vender_passagem(horario3, 3, 120.00, "C08")
    
    # Consultando dados
    print("\nLocalizações cadastradas:")
    for loc in gerenciador.listar_localizacoes():
        print(loc)
    
    print("\nEmbarcações cadastradas:")
    for emb in gerenciador.listar_embarcacoes():
        print(emb)
    
    print("\nRotas disponíveis:")
    for rota in gerenciador.listar_rotas():
        print(rota)
    
    print("\nHorários programados:")
    for horario in gerenciador.listar_horarios():
        print(horario)
    
    print("\nPassagens vendidas:")
    for passagem in gerenciador.listar_passagens():
        print(passagem)
    
    gerenciador.fechar_conexao()
import sqlite3

class DbConnection:
    def __init__(self, db_name='./storage/data/passagens_barco.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def listar_cidades(self):
        self.cursor.execute('SELECT DISTINCT cidade FROM portos')
        return [row[0] for row in self.cursor.fetchall()]

    def listar_viagens(self):
        self.cursor.execute('''
            SELECT v.id, p1.nome, p2.nome, v.data_partida
            FROM viagens v
            JOIN portos p1 ON v.id_porto_origem = p1.id
            JOIN portos p2 ON v.id_porto_destino = p2.id
        ''')
        return self.cursor.fetchall()
    
    def listar_passagens(self):
        self.cursor.execute('''
            SELECT p1.nome, p2.nome, v.data_partida, a.numero_assento, pa.nome
            FROM passagens ps
            JOIN viagens v ON ps.id_viagem = v.id
            JOIN portos p1 ON v.id_porto_origem = p1.id
            JOIN portos p2 ON v.id_porto_destino = p2.id
            JOIN assentos a ON ps.id_assento = a.id
            JOIN passageiros pa ON ps.id_passageiro = pa.id
        ''')
        return self.cursor.fetchall()

    def search_travels(self, origem, destino, embarque):
        self.cursor.execute('''
            SELECT p1.nome, p2.nome, v.data_partida
            FROM viagens v
            JOIN portos p1 ON v.id_porto_origem = p1.id
            JOIN portos p2 ON v.id_porto_destino = p2.id
            WHERE p1.nome = ? AND p2.nome = ? AND v.data_partida = ?
        ''', (origem, destino, embarque))
        return self.cursor.fetchall()
    

    def close(self):
        self.conn.close()
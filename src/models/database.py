import sqlite3


class GerenciadorPassagensBarco:
    def __init__(self, db_name='passagens_barco.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS portos (
                id INTEGER PRIMARY KEY NOT NULL,
                nome TEXT NOT NULL,
                cidade TEXT NOT NULL,
                estado TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS embarcacoes (
                id INTEGER PRIMARY KEY NOT NULL,
                nome TEXT NOT NULL,
                capacidade INTEGER NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS assentos (
                            id INTEGER PRIMARY KEY NOT NULL,
                            id_embarcacao INTEGER NOT NULL,
                            numero_assento INTEGER NOT NULL,
                            tipo TEXT NOT NULL,
                            FOREIGN KEY (id_embarcacao) REFERENCES embarcacoes(id)
                            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passageiros (
                id INTEGER PRIMARY KEY NOT NULL,
                nome TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS viagens(
                            id INTEGER PRIMARY KEY NOT NULL,
                            id_embarcacao INTEGER NOT NULL,
                            id_porto_origem INTEGER NOT NULL,
                            id_porto_destino INTEGER NOT NULL,
                            data_partida TEXT NOT NULL,
                            FOREIGN KEY (id_embarcacao) REFERENCES embarcacoes(id),
                            FOREIGN KEY (id_porto_origem) REFERENCES portos(id),
                            FOREIGN KEY (id_porto_destino) REFERENCES portos(id)
                            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passagens(
                            id INTEGER PRIMARY KEY NOT NULL,
                            id_viagem INTEGER NOT NULL,
                            id_assento INTEGER NOT NULL,
                            id_passageiro INTEGER NOT NULL,
                            FOREIGN KEY (id_viagem) REFERENCES viagens(id),
                            FOREIGN KEY (id_assento) REFERENCES assentos(id),
                            FOREIGN KEY (id_passageiro) REFERENCES passageiros(id)
                            )
        ''')
        self.conn.commit()


if __name__ == "__main__":
    db = GerenciadorPassagensBarco()
    
    
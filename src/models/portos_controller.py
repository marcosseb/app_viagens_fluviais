import sqlite3


class PortosController:
    def __init__(self, db_name='./storage/data/passagens_barco.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()


    def cadastrar_porto(self, cliente_data):
        """
        Cadastra um novo porto no banco de dados
        
        Args:
            cliente_data (dict): Dicionário contendo os dados do porto:
                {
                    'nome': str,
                    'cidade': str,
                    'estado': str
                }
        
        Returns:
            int: ID do cliente cadastrado ou None em caso de erro
        """
        sql = """INSERT INTO portos (
                    nome, 
                    cidade, 
                    estado
                ) VALUES (?, ?, ?)"""
        
        try:
            self.cursor.execute(sql, (
                cliente_data['nome'],
                cliente_data['cidade'],
                cliente_data.get('estado')
            ))
            self.conn.commit()
            print(f"Cliente {cliente_data['nome']} cadastrado com sucesso!")
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Erro inesperado ao cadastrar porto: {e}")
            self.conn.rollback()
            return None
        
    def listar_portos(self):
        """
        Lista todos os portos cadastrados no banco de dados
        
        Returns:
            list: Lista de dicionários com os dados dos portos
        """
        sql = "SELECT * FROM portos"
        try:
            self.cursor.execute(sql)
            clientes = self.cursor.fetchall()
            return [dict(zip([column[0] for column in self.cursor.description], row)) for row in clientes]
        except Exception as e:
            print(f"Erro ao listar portos: {e}")
            self.conn.rollback()
            return []

    def excluir_porto(self):
        ...

    def atualizar_porto(self):
        pass
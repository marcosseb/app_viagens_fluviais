import sqlite3

class PassageirosController:
    def __init__(self, db_name='./storage/data/passagens_barco.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def cadastrar_passageiro(self, passageiro_data):
        """
        Cadastra um novo passageiro no banco de dados
        
        Args:
            passageiro_data (dict): Dados do passageiro:
                {
                    'nome': str
                }
        
        Returns:
            int: ID do passageiro cadastrado ou None em caso de erro
        """
        sql = """INSERT INTO passageiros (
                    nome
                ) VALUES (?)"""
        
        try:
            self.cursor.execute(sql, (
                passageiro_data['nome'],
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Erro ao cadastrar passageiro: {e}")
            self.conn.rollback()
            return None
        
    def listar_passageiros(self):
        """
        Lista todos os passageiros cadastrados
        
        Returns:
            list: Lista de dicionários com os dados dos passageiros
        """
        sql = "SELECT * FROM passageiros"
        try:
            self.cursor.execute(sql)
            passageiros = self.cursor.fetchall()
            return [dict(zip([column[0] for column in self.cursor.description], row)) for row in passageiros]
        except Exception as e:
            print(f"Erro ao listar passageiros: {e}")
            self.conn.rollback()
            return []

    def excluir_passageiro(self, id_passageiro):
        """
        Exclui um passageiro do banco de dados
        
        Args:
            id_passageiro (int): ID do passageiro a ser excluído
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário
        """
        sql = "DELETE FROM passageiros WHERE id = ?"
        try:
            self.cursor.execute(sql, (id_passageiro,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir passageiro: {e}")
            self.conn.rollback()
            return False

    def atualizar_passageiro(self, id_passageiro, passageiro_data):
        """
        Atualiza os dados de um passageiro
        
        Args:
            id_passageiro (int): ID do passageiro a ser atualizado
            passageiro_data (dict): Dados atualizados do passageiro
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        sql = """UPDATE passageiros SET
                    nome = ?
                WHERE id = ?"""
        try:
            self.cursor.execute(sql, (
                passageiro_data['nome'],
                id_passageiro
            ))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar passageiro: {e}")
            self.conn.rollback()
            return False
import sqlite3

class PassagensController:
    def __init__(self, db_name='./storage/data/passagens_barco.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def cadastrar_passagem(self, passagem_data):
        """
        Cadastra uma nova passagem no banco de dados
        
        Args:
            passagem_data (dict): Dados da passagem:
                {
                    'id_viagem': int,
                    'id_assento': int,
                    'id_passageiro': int
                }
        
        Returns:
            int: ID da passagem cadastrada ou None em caso de erro
        """
        sql = """INSERT INTO passagens (
                    id_viagem,
                    id_assento,
                    id_passageiro
                ) VALUES (?, ?, ?)"""
        
        try:
            self.cursor.execute(sql, (
                passagem_data['id_viagem'],
                passagem_data['id_assento'],
                passagem_data['id_passageiro']
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Erro ao cadastrar passagem: {e}")
            self.conn.rollback()
            return None
        
    def listar_passagens(self):
        """
        Lista todas as passagens cadastradas
        
        Returns:
            list: Lista de dicionários com os dados das passagens
        """
        sql = "SELECT * FROM passagens"
        try:
            self.cursor.execute(sql)
            passagens = self.cursor.fetchall()
            return [dict(zip([column[0] for column in self.cursor.description], row)) for row in passagens]
        except Exception as e:
            print(f"Erro ao listar passagens: {e}")
            self.conn.rollback()
            return []

    def excluir_passagem(self, id_passagem):
        """
        Exclui uma passagem do banco de dados
        
        Args:
            id_passagem (int): ID da passagem a ser excluída
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário
        """
        sql = "DELETE FROM passagens WHERE id = ?"
        try:
            self.cursor.execute(sql, (id_passagem,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir passagem: {e}")
            self.conn.rollback()
            return False

    def atualizar_passagem(self, id_passagem, passagem_data):
        """
        Atualiza os dados de uma passagem
        
        Args:
            id_passagem (int): ID da passagem a ser atualizada
            passagem_data (dict): Dados atualizados da passagem
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        sql = """UPDATE passagens SET
                    id_viagem = ?,
                    id_assento = ?,
                    id_passageiro = ?
                WHERE id = ?"""
        try:
            self.cursor.execute(sql, (
                passagem_data['id_viagem'],
                passagem_data['id_assento'],
                passagem_data['id_passageiro'],
                id_passagem
            ))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar passagem: {e}")
            self.conn.rollback()
            return False
        
    def listar_passagens_por_id(self, id):
        query = 'SELECT * FROM passagens WHERE id = ?'
        try:
            self.cursor.execute(query, id)
            passagem = self.cursor.fetchall()
            return passagem
        except Exception as e:
            print(f"Erro ao buscar passagem: {e}")
            self.conn.rollback()
            return False
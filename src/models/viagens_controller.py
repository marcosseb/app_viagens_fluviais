import sqlite3

class ViagensController:
    def __init__(self, db_name='./storage/data/passagens_barco.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def cadastrar_viagem(self, viagem_data):
        """
        Cadastra uma nova viagem no banco de dados
        
        Args:
            viagem_data (dict): Dados da viagem:
                {
                    'id_embarcacao': int,
                    'id_porto_origem': int,
                    'id_porto_destino': int,
                    'data_partida': str (AAAA-MM-DD)
                }
        
        Returns:
            int: ID da viagem cadastrada ou None em caso de erro
        """
        sql = """INSERT INTO viagens (
                    id_embarcacao,
                    id_porto_origem,
                    id_porto_destino,
                    data_partida
                ) VALUES (?, ?, ?, ?)"""
        
        try:
            self.cursor.execute(sql, (
                viagem_data['id_embarcacao'],
                viagem_data['id_porto_origem'],
                viagem_data['id_porto_destino'],
                viagem_data['data_partida']
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Erro ao cadastrar viagem: {e}")
            self.conn.rollback()
            return None
        
    def listar_viagens(self):
        """
        Lista todas as viagens cadastradas
        
        Returns:
            list: Lista de dicionários com os dados das viagens
        """
        sql = "SELECT * FROM viagens"
        try:
            self.cursor.execute(sql)
            viagens = self.cursor.fetchall()
            return [dict(zip([column[0] for column in self.cursor.description], row)) for row in viagens]
        except Exception as e:
            print(f"Erro ao listar viagens: {e}")
            self.conn.rollback()
            return []

    def excluir_viagem(self, id_viagem):
        """
        Exclui uma viagem do banco de dados
        
        Args:
            id_viagem (int): ID da viagem a ser excluída
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário
        """
        sql = "DELETE FROM viagens WHERE id = ?"
        try:
            self.cursor.execute(sql, (id_viagem,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir viagem: {e}")
            self.conn.rollback()
            return False

    def atualizar_viagem(self, id_viagem, viagem_data):
        """
        Atualiza os dados de uma viagem
        
        Args:
            id_viagem (int): ID da viagem a ser atualizada
            viagem_data (dict): Dados atualizados da viagem
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        sql = """UPDATE viagens SET
                    id_embarcacao = ?,
                    id_porto_origem = ?,
                    id_porto_destino = ?,
                    data_partida = ?
                WHERE id = ?"""
        try:
            self.cursor.execute(sql, (
                viagem_data['id_embarcacao'],
                viagem_data['id_porto_origem'],
                viagem_data['id_porto_destino'],
                viagem_data['data_partida'],
                id_viagem
            ))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar viagem: {e}")
            self.conn.rollback()
            return False
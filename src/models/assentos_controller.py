import sqlite3

class AssentosController:
    def __init__(self, db_name='./storage/data/passagens_barco.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def cadastrar_assento(self, assento_data):
        """
        Cadastra um novo assento no banco de dados
        
        Args:
            assento_data (dict): Dados do assento:
                {
                    'id_embarcacao': int,
                    'numero_assento': int,
                    'tipo': str
                }
        
        Returns:
            int: ID do assento cadastrado ou None em caso de erro
        """
        sql = """INSERT INTO assentos (
                    id_embarcacao,
                    numero_assento,
                    tipo
                ) VALUES (?, ?, ?)"""
        
        try:
            self.cursor.execute(sql, (
                assento_data['id_embarcacao'],
                assento_data['numero_assento'],
                assento_data['tipo']
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Erro ao cadastrar assento: {e}")
            self.conn.rollback()
            return None
        
    def listar_assentos(self):
        """
        Lista todos os assentos cadastrados
        
        Returns:
            list: Lista de dicionários com os dados dos assentos
        """
        sql = "SELECT * FROM assentos"
        try:
            self.cursor.execute(sql)
            assentos = self.cursor.fetchall()
            return [dict(zip([column[0] for column in self.cursor.description], row)) for row in assentos]
        except Exception as e:
            print(f"Erro ao listar assentos: {e}")
            self.conn.rollback()
            return []

    def excluir_assento(self, id_assento):
        """
        Exclui um assento do banco de dados
        
        Args:
            id_assento (int): ID do assento a ser excluído
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário
        """
        sql = "DELETE FROM assentos WHERE id = ?"
        try:
            self.cursor.execute(sql, (id_assento,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir assento: {e}")
            self.conn.rollback()
            return False

    def atualizar_assento(self, id_assento, assento_data):
        """
        Atualiza os dados de um assento
        
        Args:
            id_assento (int): ID do assento a ser atualizado
            assento_data (dict): Dados atualizados do assento
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        sql = """UPDATE assentos SET
                    id_embarcacao = ?,
                    numero_assento = ?,
                    tipo = ?
                WHERE id = ?"""
        try:
            self.cursor.execute(sql, (
                assento_data['id_embarcacao'],
                assento_data['numero_assento'],
                assento_data['tipo'],
                id_assento
            ))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar assento: {e}")
            self.conn.rollback()
            return False
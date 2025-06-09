import sqlite3

class EmbarcacoesController:
    def __init__(self, db_name='./storage/data/passagens_barco.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def cadastrar_embarcacao(self, embarcacao_data):
        """
        Cadastra uma nova embarcação no banco de dados
        
        Args:
            embarcacao_data (dict): Dados da embarcação:
                {
                    'nome': str,
                    'capacidade': int
                }
        
        Returns:
            int: ID da embarcação cadastrada ou None em caso de erro
        """
        sql = """INSERT INTO embarcacoes (
                    nome, 
                    capacidade
                ) VALUES (?, ?)"""
        
        try:
            self.cursor.execute(sql, (
                embarcacao_data['nome'],
                embarcacao_data['capacidade']
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Erro ao cadastrar embarcação: {e}")
            self.conn.rollback()
            return None
        
    def listar_embarcacoes(self):
        """
        Lista todas as embarcações cadastradas
        
        Returns:
            list: Lista de dicionários com os dados das embarcações
        """
        sql = "SELECT * FROM embarcacoes"
        try:
            self.cursor.execute(sql)
            embarcacoes = self.cursor.fetchall()
            return [dict(zip([column[0] for column in self.cursor.description], row)) for row in embarcacoes]
        except Exception as e:
            print(f"Erro ao listar embarcações: {e}")
            self.conn.rollback()
            return []

    def excluir_embarcacao(self, id_embarcacao):
        """
        Exclui uma embarcação do banco de dados
        
        Args:
            id_embarcacao (int): ID da embarcação a ser excluída
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário
        """
        sql = "DELETE FROM embarcacoes WHERE id = ?"
        try:
            self.cursor.execute(sql, (id_embarcacao,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir embarcação: {e}")
            self.conn.rollback()
            return False

    def atualizar_embarcacao(self, id_embarcacao, embarcacao_data):
        """
        Atualiza os dados de uma embarcação
        
        Args:
            id_embarcacao (int): ID da embarcação a ser atualizada
            embarcacao_data (dict): Dados atualizados da embarcação
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
        """
        sql = """UPDATE embarcacoes SET
                    nome = ?,
                    capacidade = ?
                WHERE id = ?"""
        try:
            self.cursor.execute(sql, (
                embarcacao_data['nome'],
                embarcacao_data['capacidade'],
                id_embarcacao
            ))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar embarcação: {e}")
            self.conn.rollback()
            return False
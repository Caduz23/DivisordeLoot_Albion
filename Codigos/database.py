import sqlite3

class Data_base:
    
    def __init__(self, name = 'system.db') -> None: 
        self.name = name
        
    def connect(self):
        self.connection = sqlite3.connect(self.name)
        
    def close_connection(self):
        try:
            self.connection.close()
        except:
            pass
        
    def create_table_membros(self):
        
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE if not exists membros ("
                       "nick text,"
                       "loot integer)")
        
    def registrar_membro(self, fullDataSet):
        campos_tabela = ('nick','loot')
        qntd = ("?,?")
        cursor = self.connection.cursor()
        
        try:
            cursor.execute(f"""INSERT INTO membros {campos_tabela} VALUES ({qntd})""", fullDataSet)
            self.connection.commit()
            return("OK")
        except:
            return "Erro"
        
    def selecionar_membros(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM membros ORDER BY loot DESC")
            membros = cursor.fetchall()
            return membros
        except Exception as e:
            print("Erro ao selecionar membros")
            return []
        
    def loot_total(self, valorTotal, nicks):
        try:
            cursor = self.connection.cursor()
            for nick in nicks:
                cursor.execute("UPDATE membros SET loot = loot + ? WHERE nick = ?", (valorTotal, nick))
                self.connection.commit()
        except Exception as e:
            print(e)
            
        
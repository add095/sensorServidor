import sqlite3;
import time;
import random;
from datetime import datetime;

def init_db():  
    conn = sqlite3.connect('sensores.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS  leituras_sensores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATATIME,
                sensor_id TEXT,
                cpu_usage REAL, 
                ram_usage REAL, 
                cpu_temp REAL
            )
    ''');
    conn.commit();
    conn.close();

def simular_sensores():
    init_db()
    print("Simulador de sensores em execução. Pressione Ctrl+C para encerrar")
    #Valores base dos sensores 
    sensores = {
        'Sensor_A': {'cpu': 70,'ram':55.0,'temp': 67.25},
        'Sensor_B': {'cpu': 67,'ram':48.0,'temp': 40.00},
        'Sensor_C': {'cpu': 93,'ram':62.0,'temp': 53.10}
    }

    while True:
        try:  
            conn = sqlite3.connect('sensores.db', timeout=10)
            cursor = conn.cursor()

            for sensor_id, dados in sensores.items():
                #Simula pequena oscilação contínua nos valores
                cpu = round(max(0, min(100, dados['cpu'])) + random.uniform(-0.8, 0.8), 2)
                ram = round(max(0, min(100, dados['ram'])) + random.uniform(-0.8, 0.8), 2)
                temp = round(dados['temp'] + random.uniform(-0.15, 0.15), 2)

                #Atualiza referência para variação fluida
                dados['cpu'] = cpu 
                dados['ram'] = ram
                dados['temp'] = temp 

                timestamp = datetime.now().strftime('%Y-%m-%d, %H:%M:%S') 

                cursor.execute('''
                    INSERT INTO leituras_sensores(timestamp, sensor_id, cpu_usage ,ram_usage, cpu_temp)
                    VALUES(?,?,?,?,?)
                ''', (timestamp, sensor_id, cpu, ram, temp))

            conn.commit();
            conn.close();

            print(f"[{datetime.now().strftime('%H:%M:%S')}] Novas leituras inseridas")

        except sqlite3.OperationalError as e:
            print(f"Aviso de concorrência:{e}")
            time.sleep(1)
        except KeyboardInterrupt: 
            print("\nSimulação finalizada.")
            break

if __name__ == "__main__":
    simular_sensores()
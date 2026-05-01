import json
import os
from datetime import datetime

DB_PATH = "./data/json/ativos.json"

def init_db():
    os.makedirs("./data", exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({"motores": [], "audit_log": []}, f)

def insere_motor(dados: dict):
    with open(DB_PATH, "r") as f:
        db = json.load(f)
    
    dados["criado_em"] = datetime.utcnow().isoformat()
    db["motores"].append(dados)
    db["audit_log"].append({
        "operacao": "INSERT",
        "motor_id": dados["id"],
        "executado_em": dados["criado_em"]
    })
    
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

def insere_leitura(leitura: dict):
    with open(DB_PATH, "r") as f:
        db = json.load(f)
    
    if "leituras" not in db:
        db["leituras"] = []
    
    db["leituras"].append(leitura)
    
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
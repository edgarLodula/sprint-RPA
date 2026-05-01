import pytest
import os
import json
from src.database import init_db, insere_motor, insere_leitura

DB_TEST = "./data/ativos_test.json"

@pytest.fixture(autouse=True)
def setup_teardown():
    # Cria banco de teste antes de cada teste
    import src.database as db_module
    db_module.DB_PATH = DB_TEST
    init_db()
    yield
    # Apaga após cada teste
    if os.path.exists(DB_TEST):
        os.remove(DB_TEST)

def test_init_db_cria_arquivo():
    assert os.path.exists(DB_TEST)

def test_insere_motor():
    dados = {
        "id": "WEG-TEST-63-II_polos-0.12kw",
        "cv": 0.16,
        "kw": 0.12,
        "carcaca": "63",
        "rpm": 3490,
        "massa_kg": 10.0
    }
    insere_motor(dados)
    with open(DB_TEST) as f:
        db = json.load(f)
    assert len(db["motores"]) == 1
    assert db["motores"][0]["id"] == "WEG-TEST-63-II_polos-0.12kw"

def test_audit_log_registrado():
    dados = {
        "id": "WEG-TEST-80-IV_polos-0.37kw",
        "cv": 0.5, "kw": 0.37,
        "carcaca": "80", "rpm": 1740, "massa_kg": 17.8
    }
    insere_motor(dados)
    with open(DB_TEST) as f:
        db = json.load(f)
    assert len(db["audit_log"]) == 1
    assert db["audit_log"][0]["operacao"] == "INSERT"

def test_insere_leitura_sensor():
    leitura = {
        "motor_id": "WEG-TEST-63-II_polos-0.12kw",
        "timestamp": "2026-04-30T10:00:00",
        "temperatura_c": 75.5,
        "vibração_mm_s": 2.3,
        "corrente_a": 12.1,
        "rpm": 3490,
        "status": "ok"
    }
    insere_leitura(leitura)
    with open(DB_TEST) as f:
        db = json.load(f)
    assert len(db["leituras"]) == 1
    assert db["leituras"][0]["temperatura_c"] == 75.5
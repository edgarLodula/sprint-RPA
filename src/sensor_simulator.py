import random
import time
from datetime import datetime

def gera_leitura_sensor(motor_id: str) -> dict:
    """Simula leitura de sensor de motor elétrico."""
    return {
        "motor_id": motor_id,
        "timestamp": datetime.utcnow().isoformat(),
        "temperatura_c": round(random.uniform(40.0, 95.0), 2),
        "vibração_mm_s": round(random.uniform(0.5, 12.0), 3),
        "corrente_a": round(random.uniform(8.0, 30.0), 2),
        "rpm": random.randint(1450, 1510),
        "status": "ok"
    }

def stream_sensores(motores: list, intervalo_s: int = 5):
    """Gera leituras contínuas para lista de motores."""
    while True:
        for mid in motores:
            yield gera_leitura_sensor(mid)
        time.sleep(intervalo_s)
import pandas as pd

class DataCollector:
    def __init__(self):
        self.records = []

    def record(self, user_id, algorithm, pattern, text_id, is_hit, time_taken):
        """Registra uma única solicitação de arquivo."""
        self.records.append({
            'user_id': user_id,
            'algorithm': algorithm,
            'pattern': pattern,
            'text_id': text_id,
            'is_hit': is_hit,
            'time_taken': time_taken
        })

    def get_dataframe(self):
        """Converte os registros em um DataFrame do Pandas para fácil análise."""
        return pd.DataFrame(self.records)

    def clear(self):
        """Limpa os registros para uma nova simulação."""
        self.records = []
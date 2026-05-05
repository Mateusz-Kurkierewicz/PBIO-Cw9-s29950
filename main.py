import random as rnd

def generate_sequence(length: int) -> str:
    sequence = ""
    for i in range(length):
        sequence += rnd.choice(["A", "C", "T", "G"])
    return sequence

def calculate_stats(sequence: str) -> dict:
    """Zwraca słownik ze statystykami sekwencji.
    Klucze: "A", "C", "G", "T" (wartości float, %),
           "GC" (wartość float, %)."""

def insert_name(sequence: str, name: str) -> str:
    """Wstawia imię w losową pozycję sekwencji.
    Imię zapisane małymi literami."""

def format_fasta(seq_id: str, description: str,
                 sequence: str, line_width: int = 80) -> str:
    """Zwraca sformatowany rekord FASTA jako string."""

def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100_000) -> int:
    """Pobiera od użytkownika liczbę całkowitą z zakresu.
    W przypadku błędu powtarza pytanie."""

def main():
    print(generate_sequence(100))

if __name__ == "__main__":
    main()
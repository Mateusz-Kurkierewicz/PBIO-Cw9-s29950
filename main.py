import random as rnd

def generate_sequence(length: int) -> str:
    sequence = ""
    for i in range(length):
        sequence += rnd.choice(["A", "C", "T", "G"])
    return sequence

def calculate_stats(sequence: str) -> dict:
    counts = {"A": 0, "C": 0, "G": 0, "T": 0}
    total_count = 0
    for n in sequence:
        if counts.get(n) is not None:
            counts[n] += 1
            total_count += 1
    return {"A": counts["A"] / total_count,
            "C": counts["C"] / total_count,
            "G": counts["G"] / total_count,
            "T": counts["T"] / total_count,
            "GC": (counts["G"] + counts["C"]) / total_count}

def insert_name(sequence: str, name: str) -> str:
    index = int(rnd.random() * len(sequence))
    return sequence[:index] + name.lower() + sequence[index:]

def format_fasta(seq_id: str, description: str,
                 sequence: str, line_width: int = 80) -> str:
    formatted = f">{seq_id} {description}"
    lines = [sequence[i:i + line_width] for i in range(0, len(sequence), line_width)]
    for l in lines:
        formatted += f"\n{l}"
    return formatted

def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100_000) -> int:
    """Pobiera od użytkownika liczbę całkowitą z zakresu.
    W przypadku błędu powtarza pytanie."""

def main():
    sequence = insert_name(generate_sequence(100), "Mateusz")
    print(sequence)
    print(calculate_stats(sequence))
    print(format_fasta("Id", "Opis", sequence))

if __name__ == "__main__":
    main()
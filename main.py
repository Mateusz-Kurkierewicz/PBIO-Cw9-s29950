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
            "GC-content": (counts["G"] + counts["C"]) / total_count}

def format_stats(stats: dict) -> str:
    formatted = ""
    for k, v in stats.items():
        formatted += k + ": " + f"{v:.2f}\n"
    return formatted

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

def retry_validation(min_val: int = 1,
                     max_val: int = 100_000):
    print(f"Nieprawidłowa długość sekwencji - podaj liczbę z zakresu [{min_val}, {max_val}]")
    sequence_length_input = input("Podaj długość sekwencji: ")
    return validate_positive_int(sequence_length_input)

def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100_000) -> int:
    try:
        sequence_length = int(prompt)
        if sequence_length > max_val or sequence_length < min_val:
            return retry_validation(min_val, max_val)
        else:
            return sequence_length
    except ValueError:
        return retry_validation(min_val, max_val)

def is_space(c) -> bool:
    return c == " " or c == "\t" or c == "\n" or c == "\r" or c == "\v" or c == "\f"

def validate_sequence_id(prompt: str) -> bool:
    if len(prompt) == 0:
        return False
    has_whitespaces = any(is_space(c) for c in prompt)
    return not has_whitespaces

def save_to_file(sequence: str) -> str:
    file_name = "Sequences.fasta"
    with open(file=file_name, mode="w") as file:
        file.writelines(sequence)
        file.close()
    return file_name

def main():
    sequence_length_input = input("Podaj długość sekwencji: ")
    sequence_length = validate_positive_int(sequence_length_input)
    sequence_id = input("Podaj id sekwencji: ")
    while not validate_sequence_id(sequence_id):
        print("Id sekwencji nie może być puste ani zawierać białych znaków")
        sequence_id = input("Podaj id sekwencji: ")
    sequence_description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")
    sequence = insert_name(generate_sequence(sequence_length), name)
    print(format_stats(calculate_stats(sequence)))
    fasta = format_fasta(sequence_id, sequence_description, sequence)
    file_name = save_to_file(fasta)
    print(f"Zapisano sekwencję do pliku {file_name}")

if __name__ == "__main__":
    main()
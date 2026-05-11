import random as rnd
import os


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

def save_to_file(sequence: str, file_name: str, should_override=True) -> str:
    mode = "w" if should_override else "a"
    is_empty = not os.path.exists(file_name) or os.path.getsize(file_name) == 0
    if not is_empty and not should_override:
        sequence = "\n\n" + sequence
    with open(file=file_name, mode=mode) as file:
        file.writelines(sequence)
    return file_name

def get_sequence_id() -> str:
    sequence_id = input("Podaj id sekwencji: ")
    while not validate_sequence_id(sequence_id):
        print("Id sekwencji nie może być puste ani zawierać białych znaków")
        sequence_id = input("Podaj id sekwencji: ")
    return sequence_id

def create_multiple_sequences():
    try:
        sequence_count = int(input("Podaj ilość sekwencji: "))
    except ValueError:
        print("Nieprawidłowa ilość sekwencji do wygenerowania!")
        create_multiple_sequences()
        return
    for i in range(sequence_count):
        sequence = generate_sequence(2000)
        seq_id = i + 1
        id_str = str(seq_id)
        if seq_id < 10:
            id_str = "0" + id_str
        if seq_id < 100:
            id_str = "0" + id_str
        fasta = format_fasta(f"Seq_{id_str}", "", sequence)
        should_override = True if i == 0 else False
        save_to_file(fasta, "multi_sequences.fasta", should_override)

def replace_all(sequence: str) -> str:
    return sequence.replace('T', 'U')

def create_mRNA():
    sequence_length_input = input("Podaj długość sekwencji: ")
    sequence_length = validate_positive_int(sequence_length_input)
    sequence = generate_sequence(sequence_length)
    sequence = replace_all(sequence)
    formatted = format_fasta("mRNA_seq", "", sequence)
    save_to_file(formatted, "mrna.fasta")

def generate_sequence_with_distribution(length: int, probabilities: dict) -> str:
    sequence = ""
    keys = [k for k in probabilities.keys()]
    values = [v for v in probabilities.values()]
    for i in range(length):
        sequence += rnd.choices(keys, weights=values)[0]
    return sequence

def validate_float(request: str) -> float:
    try:
        return float(input(request))
    except ValueError:
        print("Nieprawidłowa wartość!")
        return validate_float(request)

def create_sequence_with_distribution():
    sequence_length_input = input("Podaj długość sekwencji: ")
    sequence_length = validate_positive_int(sequence_length_input)
    a_prob = validate_float("Podaj prawdopodobieństwo A: ")
    c_prob = validate_float("Podaj prawdopodobieństwo C: ")
    g_prob = validate_float("Podaj prawdopodobieństwo G: ")
    t_prob = validate_float("Podaj prawdopodobieństwo T: ")
    if a_prob + c_prob + g_prob + t_prob != 1:
        print("Suma prawdopodobieństw musi być równa 1!")
        return
    probabilities = {"A": a_prob, "C": c_prob, "G": g_prob, "T": t_prob}
    sequence = generate_sequence_with_distribution(sequence_length, probabilities)
    print(sequence)

def find_all(sequence: str, part: str) -> list:
    part_len = len(part)
    indexes = []
    if len(sequence) < part_len:
        print("Długość motywu jest za duża!")
        return indexes
    for i in range(len(sequence) - part_len + 1):
        fragment = sequence[i:i+part_len]
        if fragment == part:
            indexes.append(i + 1)
    return indexes

def main():
    sequence_length_input = input("Podaj długość sekwencji: ")
    sequence_length = validate_positive_int(sequence_length_input)
    sequence_id = get_sequence_id()
    sequence_description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")
    sequence = insert_name(generate_sequence(sequence_length), name)
    print(format_stats(calculate_stats(sequence)))
    fasta = format_fasta(sequence_id, sequence_description, sequence)
    file_name = save_to_file(fasta, "Sequences.fasta")
    print(f"Zapisano sekwencję do pliku {file_name}")
    # create_multiple_sequences()
    # create_mRNA()
    # create_sequence_with_distribution()
    part = input("Podaj motyw do wyszukania w sekwencji: ")
    indexes = find_all(sequence, part)
    print(f'Podany motyw występuje na następujących indeksach: {indexes}')

if __name__ == "__main__":
    main()
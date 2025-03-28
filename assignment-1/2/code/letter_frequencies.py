from collections import Counter
from tabulate import tabulate

with open("vegenire_cipher.txt", "r") as file:
    cipherfile = file.read().replace("\n", "")

"""
Anlayze letter frequency using tabulate
"""
def analyze_frequency(text: str):
    cleaned_text = [char for char in text if char.isalpha()]

    freq_counter = Counter(cleaned_text)
    total_chars = sum(freq_counter.values())

    result_list = [[char, count, f"{(count / total_chars) * 100:.2f}%"] for char, count in freq_counter.most_common()]
    print(tabulate(result_list, headers=["Character", "Frequency", "Percentage"], tablefmt="github"))

if __name__ == "__main__":
    analyze_frequency(cipherfile)
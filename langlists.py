'''import csv

with open('languages.csv') as f:
    reader = list(csv.reader(f, delimiter=';'))'''

most = '''english
german
french
spanish
japanese
korean
italian
hindi
mandarin
russian
'''.split()

facl = '''french
swedish
Hebrew (Modern)
italian
german
korean
hindi
'''.split('\n')

# print(*(f"(final_merged_df['Name_x'] == '{name.capitalize()}')" for name in facl + most), sep=' | ')
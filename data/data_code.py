import pandas as pd

# путь к нужным исходным табличкам wals (которые я загрузила предварительно)
file_path_language_names = 'https://raw.githubusercontent.com/Spalesta/gramguessr/master/data/language_names.csv'
file_path_parameters = 'https://raw.githubusercontent.com/Spalesta/gramguessr/master/data/parameters.csv'
file_path_values = 'https://raw.githubusercontent.com/Spalesta/gramguessr/master/data/values.csv'
file_path_codes = 'https://raw.githubusercontent.com/Spalesta/gramguessr/master/data/codes.csv'

# читаем файлы с wals, в которых содержатся нужные нам данные
language_names_df = pd.read_csv(file_path_language_names)
parameters_df = pd.read_csv(file_path_parameters)
values_df = pd.read_csv(file_path_values)
codes_df = pd.read_csv(file_path_codes)

# объединяем таблички parameters и values по ID и Parameter_ID, тк они одни и те же. по способу outer, значит ни одна строка не будет потеряна
merged_param_val_df = pd.merge(parameters_df, values_df, left_on='ID', right_on='Parameter_ID', how='outer')
# убираем ненужные столбцы
merged_param_val_df.drop(['Comment', 'Source', 'Example_ID', 'Description', 'ColumnSpec', 'Chapter_ID'], axis=1, inplace=True)

# объединяем merged_param_val_df с language_names по Language_ID
merged_w_lang_names_df = pd.merge(language_names_df, merged_param_val_df, left_on='Language_ID', right_on='Language_ID', how='outer')
# убираем ненужные столбцы
merged_w_lang_names_df.drop(['Provider'], axis=1, inplace=True)

# объединяем merged_w_lang_names_df
final_merged_df = pd.merge(merged_w_lang_names_df, codes_df, left_on='Code_ID', right_on='ID', how='outer', suffixes=('_left', '_right'))
final_merged_df.drop(['ID_x', 'ID_y', 'ID_left', 'Parameter_ID_left', 'Value', 'Code_ID', 'ID_right', 'Parameter_ID_right', 'Number', 'icon'], axis=1, inplace=True)

# фильтруем какие угодно языки
language_filter = (final_merged_df['Language_ID'] == 'rus') | (final_merged_df['Language_ID'] == 'ger') | (final_merged_df['Language_ID'] == 'eng')
selected_languages_df = final_merged_df[language_filter]

# переименуем для удобства
selected_languages_df = selected_languages_df.rename(columns={
    'Name_x': 'Language_name',
    'Name_y': 'Parameter',
    'Name': 'Value',
})

# отсортируем в алфавитном порядке
selected_languages_df = selected_languages_df.sort_values(by='Language_ID')

# сохраним в итоговую табличку
selected_languages_df.to_csv('https://raw.githubusercontent.com/Spalesta/gramguessr/master/data/draft.csv', index=False)


###ниже будет в комментарии пример вывода по параметру number of cases###


# number_of_cases_df = selected_languages_df[selected_languages_df['Parameter'] == 'Number of Cases']

# print("Number of Cases for Russian:", number_of_cases_df[number_of_cases_df['Language_ID'] == 'rus']['Value'].values[0])
# print("Number of Cases for German:", number_of_cases_df[number_of_cases_df['Language_ID'] == 'ger']['Value'].values[0])
# print("Number of Cases for English:", number_of_cases_df[number_of_cases_df['Language_ID'] == 'eng']['Value'].values[0])

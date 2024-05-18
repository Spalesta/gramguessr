import pandas as pd

# путь к нужным исходным табличкам wals (которые я загрузила предварительно)
file_path_language_names = 'language_names.csv'
file_path_parameters = 'parameters.csv'
file_path_values = 'values.csv'
file_path_codes = 'codes.csv'

# читаем файлы с wals, в которых содержатся нужные нам данные
language_names_df = pd.read_csv(file_path_language_names)
parameters_df = pd.read_csv(file_path_parameters)
values_df = pd.read_csv(file_path_values)
codes_df = pd.read_csv(file_path_codes)

# меняем ячейки где несколько языковых кодов на один для корректного склеивания табличек
language_names_df['Language_ID'] = language_names_df['Language_ID'].apply(lambda x: 
    'ger' if isinstance(x, str) and 'ger' in x else 
    ('spa' if isinstance(x, str) and 'spa' in x else 
    ('mnd' if isinstance(x, str) and 'mnd' in x else 
    ('ita' if isinstance(x, str) and 'ita' in x else 
    ('fre' if isinstance(x, str) and 'fre' in x else 
    ('heb' if isinstance(x, str) and 'heb' in x else 
    ('swe' if isinstance(x, str) and 'swe' in x else x)))))))

# сохраняем обновленную табличку language_names
language_names_df.to_csv('/final_language_names.csv', index=False)
file_path_final_language_names = '/content/drive/My Drive/hse_final_project/final_language_names.csv'
final_language_names_df = pd.read_csv(file_path_final_language_names)

# объединяем таблички parameters и values по ID и Parameter_ID, тк они одни и те же. по способу outer, 
# значит ни одна строка не будет потеряна
merged_param_val_df = pd.merge(parameters_df, values_df, left_on='ID', right_on='Parameter_ID', how='outer')
# убираем ненужные столбцы
merged_param_val_df.drop(['Comment', 'Source', 'Example_ID', 'Description', 'ColumnSpec', 'Chapter_ID'], axis=1, inplace=True)

# объединяем merged_param_val_df с final_language_names по Language_ID
merged_w_lang_names_df = pd.merge(final_language_names_df, merged_param_val_df, left_on='Language_ID', \
                                  right_on='Language_ID', how='outer')
# убираем ненужные столбцы
merged_w_lang_names_df.drop(['Provider'], axis=1, inplace=True)

# объединяем merged_w_lang_names_df
final_merged_df = pd.merge(merged_w_lang_names_df, codes_df, left_on='Code_ID', right_on='ID', how='outer', \
                           suffixes=('_left', '_right'))
final_merged_df.drop(['ID_x', 'ID_y', 'ID_left', 'Parameter_ID_left', 'Value', 'Code_ID', 'ID_right', \
                      'Parameter_ID_right', 'Number', 'icon'], axis=1, inplace=True)

# убираем дублирующиеся строки
final_merged_df = final_merged_df.drop_duplicates()

# фильтруем нужные нам языки по language_id и по language_name чтобы нам не попадались диалекты и варианты языков
language_filter = (
    ((final_merged_df['Language_ID'] == 'fre') &
     (final_merged_df['Name_x'] == 'French'))|

    ((final_merged_df['Language_ID'] == 'swe') &
     (final_merged_df['Name_x'] == 'Swedish'))|

    ((final_merged_df['Language_ID'] == 'heb') & 
    (final_merged_df['Name_x'] == 'Hebrew'))|

    ((final_merged_df['Language_ID'] == 'eng') & 
    (final_merged_df['Name_x'] == 'English'))|

    ((final_merged_df['Language_ID'] == 'ger') & 
    (final_merged_df['Name_x'] == 'German'))|

    ((final_merged_df['Language_ID'] == 'spa') & 
    (final_merged_df['Name_x'] == 'Spanish'))|

    ((final_merged_df['Language_ID'] == 'jpn') & 
    (final_merged_df['Name_x'] == 'Japanese'))|

    ((final_merged_df['Language_ID'] == 'kor') & 
    (final_merged_df['Name_x'] == 'Korean'))|

    ((final_merged_df['Language_ID'] == 'ita') & 
    (final_merged_df['Name_x'] == 'Italian'))|

    ((final_merged_df['Language_ID'] == 'hin') & 
    (final_merged_df['Name_x'] == 'Hindi'))|

    ((final_merged_df['Language_ID'] == 'mnd') & 
    (final_merged_df['Name_x'] == 'Mandarin'))|

    ((final_merged_df['Language_ID'] == 'rus') & 
    (final_merged_df['Name_x'] == 'Russian'))
)

selected_languages_df = final_merged_df[language_filter]

# переименуем для удобства
selected_languages_df = selected_languages_df.rename(columns={
    'Name_x': 'Language_name',
    'Name_y': 'Parameter',
    'Name': 'Value',
})

# отсортируем в алфавитном порядке
selected_languages_df = selected_languages_df.sort_values(by='Language_name')

# сохраним в итоговую табличку
selected_languages_df.to_csv('draft.csv', index=False)

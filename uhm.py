from requests import Session
from services.writer import Writer
import pandas as pd

BASE_URL = 'https://www.upphandlingsmyndigheten.se'
URL = '/api/sv/statisticsservice/bridgeapi/statistics/export/{}'

EXT = {
    'csv': 'csv',
    'excel': 'xlsx'
}

def download(params, filepath, format='excel', cleaned=True):
    print('Downloading the data...')
    response = Session().get(BASE_URL + URL.format(format), params=params)

    if response.status_code == 200:
        print('Data downloaded succesfully!')
        print(f'Url: {response.url}')

        if format == 'csv':
            content = __fix_csv(response.content)
        else:
            content = response.content

        Writer.write_file(content, f'{filepath}.{EXT[format]}')

        if cleaned:
            __clean_file(f'{filepath}.{EXT[format]}')

    else:
        print(f'There was an error {response.status_code}.')
        print(response.url)

def __fix_csv(bytes):
    return bytes.decode('utf-8-sig').replace('; ', ',').encode('utf-8')

def __clean_file(filepath):
    print('Opening the file...')
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath, sep=';')
    elif filepath.endswith('.xlsx'):
        df = pd.read_excel(filepath)
    else:
        print('The file does not seem to be a CSV or Excel.')
        return

    print('Cleaning the file to reduce it size...')

    print("- Cleaning all the 'Uppgift saknas'")
    df = df.replace('Uppgift saknas', '')

    columns_to_clean = [
        'Direktivstyrd',
        'Dynamiskt inköpssystem',
        'Elektronisk auktion',
        'Anbudsområden',
        'Samordnad upphandling',
        'Miljömässigt hållbar upphandling',
        'Socialt hållbar upphandling',
        'Innovationsupphandling',
        'Reserverad upphandling',
        'Reserverat genomförande',
        'Överprövad'
    ]

    for column in columns_to_clean:
        if column in df.columns:
            print(f'- Cleaning column {column}')
            df[column] = df[column].apply(lambda x: 'False' if 'Inte' in x or 'Inga' in x else x)
            df[column] = df[column].apply(lambda x: 'True' if x != 'False' and x != '' else x)

    if 'Upphandlings-ID' in df and 'Publiceringsdatum' in df:
        print('- Sorting the file by date then procurement ID')
        df = df.sort_values('Upphandlings-ID').sort_values('Publiceringsdatum')

    print('Saving the file...')
    if filepath.endswith('.csv'):
        df.to_csv(filepath, index=False)
    elif filepath.endswith('.xlsx'):
        sheet_name = f'{df.columns[-1]}'[:31].replace('*', '')
        save_excel_with_adjusted_columns(df, filepath, sheet_name)

def save_excel_with_adjusted_columns(df, filepath, sheet_name):
    writer = pd.ExcelWriter(filepath)

    df.to_excel(writer, sheet_name=sheet_name, index=False, na_rep='')

    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets[sheet_name].set_column(col_idx, col_idx, column_width)

    writer.close()

def big_merge():
    df = pd.read_csv('number_of_procurements.csv')

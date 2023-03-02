import uhm
import parameters
import pandas as pd

for format in ['excel', 'csv']:
    uhm.download(
        parameters.get_request_for('Upphandlingar, Bas.Antal anbud'),
        f'./data/{format}/number_of_tenders',
        format
        )

    uhm.download(
        parameters.get_request_for('Upphandlingar, Bas.Antal kontrakterade anbud*'),
        f'./data/{format}/number_of_contracted_tenders_with_suppliers',
        format
        )

    uhm.download(
        parameters.get_request_for('Upphandlingar, Bas.Antal upphandlingar'),
        f'./data/{format}/number_of_procurements',
        format
        )

    uhm.download(
        parameters.get_request_for('Upphandlingar, Innovationstyp.Antal upphandlingar, Innovationstyp'),
        f'./data/{format}/number_of_innovation_procurements',
        format
        )

    uhm.download(
        parameters.get_request_for('Upphandlingar, Miljötyp.Antal upphandlingar, Miljötyp'),
        f'./data/{format}/number_of_environmental_procurements',
        format
        )

    uhm.download(
        parameters.get_request_for('Upphandlingar, Socialtyp.Antal upphandlingar, Socialtyp'),
        f'./data/{format}/number_of_social_procurements',
        format
        )

    uhm.download(
        parameters.get_request_for('Upphandlingar, Bas.Kontrakterat värde'),
        f'./data/{format}/contracted_value',
        format
        )

    uhm.download(
        parameters.get_request_for('Valfrihetssystem.Antal valfrihetsystem'),
        f'./data/{format}/number_of_valfrihetsystem',
        format
        )

# Fix because one request fails for excel format
filepath = './data/{}/number_of_contracted_tenders_with_suppliers.{}'
df = pd.read_csv(filepath.format('csv', 'csv'))
uhm.save_excel_with_adjusted_columns(
    df,
    filepath.format('excel', 'xlsx'),
    f'{df.columns[-1]}'[:31].replace('*', '')
    )


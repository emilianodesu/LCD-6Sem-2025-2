import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import uuid
from sklearn.pipeline import Pipeline
class CsvReader(BaseEstimator, TransformerMixin):
    def __init__(self, path):
        self.path = path

    def fit(self, X, y=None):
        return self

    def transform(self, _):
        return pd.read_csv(self.path)

class ErrorFingerTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns, p, seed=42):
        self.columns = columns if isinstance(columns, list) else [columns]
        self.p = p
        self.seed = seed

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        new_df = X.copy()
        n_rows = len(new_df)
        m_cols = len(self.columns)
        np.random.seed(self.seed)
        mustBeChange = np.random.binomial(1, self.p, size=(n_rows, m_cols))
        for i in range(n_rows):
            for j in range(m_cols):
                if mustBeChange[i, j]:
                    value = new_df[self.columns[j]].iloc[i]
                    value_str = str(value)
                    value_str += np.random.choice(['1','2','3','4','5','6','7','8','9'])
                    new_val = new_df[self.columns[j]].dtype.type(value_str)
                    new_df.iloc[i, new_df.columns.get_loc(self.columns[j])] = new_val
        return new_df

class DuplicateRecordsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, n_duplicates, columns=None, random_state=42):
        self.n_duplicates = n_duplicates
        self.columns = columns
        self.random_state = random_state

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        new_df = X.copy()
        np.random.seed(self.random_state)
        random_indices = np.random.choice(len(X), self.n_duplicates, replace=False)
        duplicates = X.iloc[random_indices].copy()
        result_df = pd.concat([new_df, duplicates], ignore_index=True)
        return result_df

class MissingValuesTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns, p, seed=42):
        self.columns = columns if isinstance(columns, list) else [columns]
        self.p = p
        self.seed = seed

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        new_df = X.copy()
        i = 0
        for col in self.columns:
            if col in new_df.columns:
                np.random.seed(self.seed+i)
                mask = np.random.rand(len(new_df)) < self.p
                new_df.loc[mask, col] = np.nan
                i += 1
        return new_df

class DeleteRecordsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, p, seed=42):
        self.p = p
        self.seed = seed

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        new_df = X.copy()
        n_rows = len(new_df)
        np.random.seed(self.seed)
        mustBeChange = np.random.binomial(1, self.p, size=n_rows)
        return new_df[~mustBeChange.astype(bool)]

class GenerateRandomUUID(BaseEstimator, TransformerMixin):
    def __init__(self, column, random_state=42):
        self.column = column
        self.n_uuids = None
        self.random_state = random_state

    def fit(self, X, y=None):
        self.n_uuids = len(X)
        return self

    def transform(self, X):
        new_df = X.copy()
        np.random.seed(self.random_state)
        uuids = [uuid.uuid4().hex for _ in range(self.n_uuids)]
        new_df[self.column] = uuids
        return new_df

class CastTypeTransforme(BaseEstimator, TransformerMixin):
    def __init__(self, pairColumnType):
        self.pairColumnType = pairColumnType

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        new_df = X.copy()
        for col, dtype in self.pairColumnType.items():
            if col in new_df.columns:
                new_df[col] = new_df[col].apply(lambda x: dtype(x) if pd.notnull(x) else x)
        return new_df

class AgregarInconsistencia(BaseEstimator, TransformerMixin):
    def __init__(self, id_column, columns, noise_factor=0.05, seed=42,p=0.9,p2=0.8):
        """
        id_column: str
            The column used to identify duplicate groups.
        columns: list of str
            List of columns where variations will be added on duplicate groups.
        noise_factor: float
            Factor to scale the noise for numeric columns.
        seed: int
            Random seed.
        """
        self.id_column = id_column
        self.columns = columns if isinstance(columns, list) else [columns]
        self.noise_factor = noise_factor
        self.p = p
        self.p2 = p2
        self.seed = seed

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        new_df = X.copy()
        np.random.seed(self.seed)
        groups = new_df.groupby(self.id_column)
        for _, group_df in groups:
            if len(group_df) > 1:
                for idx in group_df.index:
                    if np.random.binomial(1,self.p,1)[0] == 0:
                        continue
                    mustBeChange = np.random.binomial(1, self.p2, len(self.columns))
                    for col,bitChange in zip(self.columns,mustBeChange):
                        if not bitChange:
                            continue
                        original_val = new_df.at[idx, col]
                        if pd.api.types.is_numeric_dtype(new_df[col]):
                            noise = original_val * np.random.uniform(-self.noise_factor, self.noise_factor)
                            new_val = original_val + noise
                            new_val = new_df[col].dtype.type(new_val)
                            new_df.at[idx, col] = new_val
        return new_df

class GenerateStartDate(BaseEstimator, TransformerMixin):
    def __init__(self, start_date, end_date, date_column):
        self.start_date = start_date
        self.end_date = end_date
        self.date_column = date_column

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        new_df = X.copy()
        new_df[self.date_column] = pd.date_range(start=self.start_date, end=self.end_date, periods=len(new_df))
        return new_df

class RandomDateOffsetTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, date_column, new_column, max_seconds, seed=42):
        self.date_column = date_column
        self.new_column = new_column
        self.max_seconds = max_seconds
        self.seed = seed

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        new_df = X.copy()
        np.random.seed(self.seed)
        # Convert the specified column to datetime if it isn't already
        new_df[self.date_column] = pd.to_datetime(new_df[self.date_column])
        # Generate a random number of seconds for each row (between 0 and max_seconds inclusive)
        random_seconds = np.random.randint(0, self.max_seconds + 1, size=len(new_df))
        # Create the new column with the offset added
        new_df[self.new_column] = new_df[self.date_column] + pd.to_timedelta(random_seconds, unit='s')
        return new_df
def calculate_and_display_accuracy(bad_dataset, original_dataset):
    # Fusiona los datasets en base a la columna 'UUID'
    merged_df = pd.merge(
        left=bad_dataset,
        right=original_dataset,
        on='UUID',
        how='left',
        suffixes=('_bad', '_original')
    )

    # Calcula la precisión comparando columnas con sufijos '_bad' y '_original'
    result_accuracy = {}
    for col in merged_df.columns:
        if col.endswith('_bad'):
            col_original = col.replace('_bad', '_original')
            col_clean = col.replace('_bad', '')
            result_accuracy[col_clean] = round(
                (merged_df[col] == merged_df[col_original]).mean() * 10,
                1
            )

    # Convierte el diccionario a DataFrame y calcula la precisión final
    result_accuracy_df = pd.DataFrame(result_accuracy, index=[0])
    cal_accuracy = round(result_accuracy_df.mean(axis=1)[0], 2)
    # Muestra los elementos usando las funciones especificadas=
    print("Resultados de Precisión:")
    print(result_accuracy_df)
    return cal_accuracy
def calculate_and_display_consistency(bad_dataset):
    # Filtrar grupos duplicados en base a 'UUID'
    duplicate_groups = bad_dataset.groupby('UUID').filter(lambda x: len(x) >= 2)

    def count_discrepancies(group):
        pivot = group.iloc[0]
        counter = 0
        idx = [pivot['UUID']]
        for _, row in group.iloc[1:].iterrows():
            for col in group.columns:
                if pd.isna(pivot[col]) and pd.isna(row[col]):
                    continue
                if pivot[col] != row[col]:
                    # Si al menos un valor es diferente se considera una discrepancia
                    counter += 1
                    idx.append(row['UUID'])
                    break
        return counter, idx

    count_records_with_discrepancies = 0
    ids = []
    total_records = len(bad_dataset)

    # Agrupar nuevamente por 'UUID' en los grupos filtrados
    for _, group in duplicate_groups.groupby('UUID'):
        c, ids_group = count_discrepancies(group)
        ids += ids_group
        count_records_with_discrepancies += c

    records_with_inconsistencies = bad_dataset[bad_dataset['UUID'].isin(ids)]
    records_with_inconsistencies = records_with_inconsistencies.sort_values('UUID')
    
    cal_consistency = round((1 - count_records_with_discrepancies / total_records) * 10, 2)
    print("Registros con Inconsistencia:")
    print(records_with_inconsistencies)
    return cal_consistency
def calculate_and_display_completeness(bad_dataset):
    
    result_non_null_percent = round((bad_dataset.notnull().sum() / len(bad_dataset)) * 10, 2).to_frame().T
    cal_completeness = round(result_non_null_percent.mean(axis=1)[0], 2)
    print("Porcentaje de Completitud:")
    print(result_non_null_percent)

    return cal_completeness
def calculate_and_display_opportunity(bad_dataset):
    max_date_to_opp = 60 * 60 * 24 * 7  # una semana
    result_opp = (bad_dataset['confirm_date'] - bad_dataset['register_date']).dt.total_seconds()
    result_opp_mean = round(result_opp.mean(), 2)
    result_opp_mean_days = round(result_opp_mean / (60 * 60 * 24), 2)
    days = int(result_opp_mean // (60 * 60 * 24))
    hours = int((result_opp_mean % (60 * 60 * 24)) // (60 * 60))
    result_opp_mean_days_format = f"{days} días con {hours:02d} hrs"
    cal_opportunity = 10 - (result_opp_mean / max_date_to_opp) * 10
    print(f"Tiempo promedio de Espera:{result_opp_mean_days_format}")
    cal_opportunity = round(cal_opportunity, 2)
    return cal_opportunity
cast_transformer =  CastTypeTransforme(pairColumnType={
        'Age' : np.int16,
        'SystolicBP' : np.int16,
        'DiastolicBP' : np.int16,
        'BS' : np.float32,
        'BodyTemp' : np.float32,
        'HeartRate' : np.int16,
    })
pipeline_dataset = Pipeline([
    ('csv_reader', CsvReader(path='Maternal Health Risk Data Set.csv')),
    ('generate_uuid', GenerateRandomUUID(column='UUID')),
    ('cast_type',cast_transformer),
    ('generate_start_date', GenerateStartDate(start_date='2025-01-01', end_date='2025-03-08', date_column='register_date')),
    ('random_date_offset', RandomDateOffsetTransformer(date_column='register_date', new_column='confirm_date', max_seconds=60*60*24*4)),
])
pipeline_bad_dataset = Pipeline([
    ('delete_records', DeleteRecordsTransformer(p=0.05)),
    ('error_finger', ErrorFingerTransformer(columns='Age', p=0.1)),
    ('missing_values', MissingValuesTransformer(columns=['Age','HeartRate','SystolicBP','BodyTemp'], p=0.2)),
    ('duplicate', DuplicateRecordsTransformer(n_duplicates=100)),
    ('c1', cast_transformer),
    (
        'incon',
        AgregarInconsistencia(
            id_column='UUID',
            columns=['Age','SystolicBP','DiastolicBP','BS','BodyTemp','HeartRate'],
            noise_factor=0.2
        )
    ),
    ('c2', cast_transformer),
])
original_dataset = pipeline_dataset.fit_transform(None)
bad_dataset = pipeline_bad_dataset.fit_transform(original_dataset)
def get_datasets():
    return bad_dataset, original_dataset
if __name__ == '__main__':

    accuracy = calculate_and_display_accuracy(bad_dataset, original_dataset)
    print("_______________________________________________________\n\n")
    consistency = calculate_and_display_consistency(bad_dataset)
    print("_______________________________________________________\n\n")

    completeness = calculate_and_display_completeness(bad_dataset)
    print("_______________________________________________________\n\n")

    opportunity = calculate_and_display_opportunity(bad_dataset)
    print("_______________________________________________________\n\n")


    print("Precisión:", accuracy)
    print("Consistencia:", consistency)
    print("Completitud:", completeness)
    print("Oportunidad:", opportunity)
    print("\n")

    calificacion_final = round((
        0.4*accuracy + \
        0.2*consistency + \
        0.1*completeness + \
        0.3*opportunity), 2)
    print("Calificación Final:", calificacion_final)
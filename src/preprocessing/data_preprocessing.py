import pandas as pd
import numpy as np
from pathlib import Path


def load_raw_data(path: str) -> pd.DataFrame:
    """Carga el dataset RAW desde un CSV."""
    return pd.read_csv(path, encoding="latin-1")


def filter_target_classes(df: pd.DataFrame) -> pd.DataFrame:
    """Conserva únicamente las clases 1 y 3 del target DIABETE3."""
    df = df[df["DIABETE3"].isin([1, 3])].copy()
    df.reset_index(drop=True, inplace=True)
    df = df.drop_duplicates()
    return df


def drop_irrelevant_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina las columnas irrelevantes para la detección de diabetes."""
    cols_to_drop = [
    '_STATE', 'FMONTH', 'IDATE', 'IMONTH', 'IDAY', 'IYEAR', 'DISPCODE', 'SEQNO', '_PSU', 'QSTVER', 'QSTLANG', 'MSCODE',
    '_STSTR', '_STRWT', '_RAWRAKE', '_WT2RAKE', '_CLLCPWT', '_DUALUSE', '_DUALCOR', '_LLCPWT', 'CTELENUM', 'CELLFON3',
    'CTELNUM1', 'CELLFON2', 'CADULT', 'CCLGHOUS', 'CSTATE', 'LANDLINE', 'NUMPHON2', 'CPDEMO1', 'INTERNET', 'PVTRESD1',
    'COLGHOUS', 'STATERES', 'LADULT', 'NUMADULT', 'NUMMEN', 'NUMWOMEN', 'PVTRESD2', 'HHADULT', 'HLTHPLN1', 'PERSDOC2',
    'MEDCOST', 'CHECKUP1', 'RENTHOM1', 'NUMHHOL2', 'CHILDREN', 'INCOME2', 'CDHELP', 'CDSOCIAL', '_CHLDCNT', '_INCOMG',
    'DIABAGE2', 'CVDINFR4', 'CVDCRHD4', 'CVDSTRK3', 'CHCKIDNY', 'PDIABTST', 'PREDIAB1', 'INSULIN', 'FEETCHK2',
    'DOCTDIAB', 'CHKHEMO3', 'FEETCHK', 'EYEEXAM', 'DIABEYE', 'DIABEDU', 'MARITAL', 'EDUCA', 'VETERAN3', 'EMPLOY1',
    'SEATBELT', 'CDDISCUS', 'SCNTMNY1', 'SCNTMEL1', 'SCNTPAID', 'SCNTWRK1', 'SCNTLPAD', 'SCNTLWK1', 'SXORIENT',
    'TRNSGNDR', 'RCSGENDR', 'RCSRLTN2', 'EMTSUPRT', 'LSATISFY', 'ADPLEASR', 'ADDOWN', 'MISTMNT', '_EDUCAG', '_RFSEAT2',
    '_RFSEAT3', '_LMTWRK1', '_LMTSCL1', 'CAREGIV1', 'CRGVREL1', 'CRGVLNG1', 'CRGVHRS1', 'CRGVPRB1', 'CRGVPERS',
    'CRGVHOUS', 'CRGVMST2', 'CRGVEXPT', 'CDHOUSE', 'CDASSIST', 'WEIGHT2', 'HEIGHT3', 'HTIN4', 'HTM4', 'WTKG3',
    '_BMI5', '_RFBMI5', 'STOPSMK2', 'LASTSMK2', 'USENOW3', '_SMOKER3', '_RFSMOK3', 'ALCDAY5', 'DRNK3GE5', 'MAXDRNKS',
    'DRNKANY5', 'DROCDY3_', '_RFBING5', '_DRNKWEK', '_RFDRHV5', 'FVGREEN', 'ARTHEXER', 'FVORANG', 'VEGETAB1', 'GRENDAY_',
    'ORNGDAY_', 'VEGEDA1_', '_MISVEGN', '_VEGLT1', '_VEG23', '_VEGETEX', 'FTJUDA1_', 'FRUTDA1_', 'FRUITJU1', 'FRUIT1',
    '_MISFRTN', '_FRTLT1', '_FRT16', '_FRUITEX', 'FVBEANS', 'EXERANY2', 'EXRACT11', 'EXRACT21', 'EXEROFT2', 'EXERHMM2',
    'ADMOVE', 'EXACTOT1', 'EXACTOT2', '_TOTINDA', 'METVL11_', 'METVL21_', 'MAXVO2_', 'FC60_', 'ACTIN11_', 'ACTIN21_',
    'PADUR1_', 'PADUR2_', 'PAFREQ1_', 'PAFREQ2_', '_MINAC11', '_MINAC21', 'STRFREQ_', 'PAMIN11_', 'PAMIN21_', 'PA1MIN_',
    'PAVIG11_', 'PAVIG21_', 'PA1VIGM_', '_PA150R2', '_PA300R2', '_PA30021', '_PASTRNG', '_PAREC1', '_PASTAE1', '_LMTACT1',
    'LMTJOIN3', 'ARTHSOCL', 'JOINPAIN', 'PAINACT2', 'TOLDHI2', 'QLMENTL2', 'QLSTRES2', 'QLHLTH2', '_RFHLTH', 'VIDFCLT2',
    'VIREDIF3', 'VIPRFVS2', 'VINOCRE2', 'VIEYEXM2', 'VIINSUR2', 'VICTRCT4', 'VIGLUMA2', 'VIMACDG2', 'ASTHMAGE', 'ASATTACK',
    'ASERVIST', 'ASDRVIST', 'ASRCHKUP', 'ASACTLIM', 'ASYMPTOM', 'ASNOSLEP', 'ASTHMED3', 'ASINHALR', 'CASTHDX2', 'CASTHNO2',
    '_LTASTH1', '_CASTHM1', '_ASTHMS1', 'HAREHAB1', 'STREHAB1', 'CVDASPRN', 'ASPUNSAF', '_MICHD', 'RLIVPAIN', 'RDUCHART',
    'RDUCSTRK', 'ARTTODAY', 'ARTHWGT', 'ARTHEDU', '_DRDXAR1', '_RFCHOL',  '_CHISPNC', '_CRACE1', '_CPRACE', '_PRACE1',
    '_MRACE1', '_HISPANC', '_RACEG21', '_RACEGR3', '_RACE_G1', '_AGE65YR', '_AGE80', '_AGE_G', '_RFHYPE5', 'CHOLCHK',
    'HIVTST6', 'HIVTSTD3', 'WHRTST10', 'HADMAM', 'HOWLONG', 'HADPAP2', 'LASTPAP2', 'HPVTEST', 'HPLSTTST', 'HADHYST2',
    'PROFEXAM', 'LENGEXAM', 'BLDSTOOL', 'LSTBLDS3', 'HADSIGM3', 'HADSGCO1', 'LASTSIG3', 'PSATEST1', 'PSATIME', 'PCPSARS1',
    'PCPSADE1', 'PCDMDECN', '_AIDTST3', '_CHOLCHK', 'FLUSHOT6', 'FLSHTMY2', 'IMFVPLAC', 'PNEUVAC3', 'TETANUS', 'HPVADVC2',
    'HPVADSHT', 'SHINGLE2', '_FLSHOT6', '_PNEUMO2', 'DRADVISE', 'PREGNANT', 'PCPSAAD2', 'PCPSADI1', 'PCPSARE1', '_HCVU651',
    'STRENGTH', 'PAMISS1_', 'SMOKDAY2', 'EXERHMM1', 'WTCHSALT', 'LONGWTCH', 'BEANDAY_', '_FRTRESP', '_VEGRESP', '_PAINDX1',
    'CIMEMLOS', 'ASTHMA3', 'ASTHNOW', 'CHCSCNCR', 'CHCOCNCR', 'CHCCOPD1', 'BLDSUGAR'
]
    return df.drop(columns=cols_to_drop, errors="ignore").copy()


def drop_high_nan_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina columnas con gran cantidad de valores faltantes o poco valor clínico."""
    cols_to_drop = ['ADSLEEP', 'ADENERGY', 'ADEAT1', 'ADFAIL',
                    'ADTHINK', 'ADANXEV', 'ARTHDIS2', 'POORHLTH', 
                    'AVEDRNK2', 'PHYSHLTH', 'MENTHLTH']
    return df.drop(columns=cols_to_drop, errors="ignore").copy()


def decode_exeroft1(x):
    """Convierte EXEROFT1 a unidades estándar (veces/semana)."""
    if pd.isna(x):
        return np.nan
    if 101 <= x <= 199:
        return x - 100
    if 201 <= x <= 299:
        return (x - 200) / (30.0 / 7.0)
    if x in (777, 999):
        return x
    return np.nan


def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica transformaciones numéricas (EXEROFT1, frutos y vegetales)."""
    df["EXEROFT1"] = df["EXEROFT1"].apply(decode_exeroft1)
    df["_FRUTSUM"] = df["_FRUTSUM"] / 100
    df["_VEGESUM"] = df["_VEGESUM"] / 100
    return df

def impute_bpmeds(df: pd.DataFrame) -> pd.DataFrame:
    df["BPMEDS"] = df["BPMEDS"].fillna(2)
    return df

def replace_invalid_values(df: pd.DataFrame) -> pd.DataFrame:
    """Reemplaza valores que representan 'No sabe/Se negó' por NaN."""
    invalid_values = {
        'GENHLTH': [7, 9],
        'BPHIGH4': [7, 9],
        'BPMEDS': [7, 9],
        'BLOODCHO': [7, 9],
        'HAVARTH3': [7, 9],
        'QLACTLM2': [7, 9],
        'USEEQUIP': [7, 9],
        'BLIND': [7, 9],
        'DECIDE': [7, 9],
        'DIFFWALK': [7, 9],
        'DIFFDRES': [7, 9],
        'DIFFALON': [7, 9],
        'SMOKE100': [7, 9],
        'ADDEPEV2': [7, 9],
        '_PACAT1': [9],
        '_RACE': [9],
        '_AGEG5YR': [14],
        'EXEROFT1': [777, 999]
    }
    for col, vals in invalid_values.items():
        df[col] = df[col].replace(vals, np.nan)
    return df


def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Imputa valores faltantes según tipo de variable."""
    categorical_nominal = ['BPHIGH4', 'BPMEDS', 'BLOODCHO', 'HAVARTH3', 'QLACTLM2',
                           'USEEQUIP', 'BLIND', 'DECIDE', 'DIFFWALK',
                           'DIFFDRES', 'DIFFALON', 'SMOKE100',
                           'ADDEPEV2', '_RACE']

    categorical_ordinal = ['GENHLTH', '_PACAT1', '_AGEG5YR']

    numerical = ['EXEROFT1']

    for col in categorical_nominal + categorical_ordinal:
        df[col] = df[col].fillna(-1)

    for col in numerical:
        df[col] = df[col].fillna(df[col].median())

    df = df.reset_index(drop=True)
    return df


def preprocess_data(input_path: str, output_path: str):
    """Pipeline completo de preprocesamiento."""
    df = load_raw_data(input_path)
    print('Dataset original:')
    print(df.info())
    df = filter_target_classes(df)
    df = drop_irrelevant_columns(df)
    df = drop_high_nan_columns(df)
    df = clean_numeric_columns(df)
    df = impute_bpmeds(df)
    df.dropna(inplace=True)
    df = replace_invalid_values(df)
    df = impute_missing_values(df)
    print('Dataset pretratado:')
    print(df.info())
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    INPUT = Path("data/raw_dataset.csv")
    OUTPUT = Path("data/cleaned_dataset.csv")
    preprocess_data(INPUT, OUTPUT)
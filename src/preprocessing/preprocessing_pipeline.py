import numpy as np

categorical_nominal = ['BPHIGH4', '_RACE']
binary_vars = ['BPMEDS', 'BLOODCHO', 'HAVARTH3', 'QLACTLM2', 'USEEQUIP', 'BLIND', 'DECIDE', 
               'DIFFWALK', 'DIFFALON','DIFFDRES', 'SMOKE100', 'ADDEPEV2', 'SEX']
categorical_ordinal = ['GENHLTH', '_PACAT1', '_AGEG5YR', '_BMI5CAT']
numeric_vars = ['EXEROFT1', '_FRUTSUM', '_VEGESUM']

def boosting_deterministic_preproc(X):
    X = X.copy()
    X = X.replace(-1, np.nan)

    for col in binary_vars:
        X[col] = (X[col]==1).astype(int)

    for col in categorical_nominal:
        X[col] = X[col].astype('category')

    return X

def cap_outliers_numeric(X, numeric_vars):
    X = X.copy()

    for col in numeric_vars:
        low = np.nanpercentile(X[col], 1)
        high = np.nanpercentile(X[col], 99)
        X[col] = X[col].clip(low, high)
        
    return X
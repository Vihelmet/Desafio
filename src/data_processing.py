import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

vino = pd.read_csv(r'.\Analisis_calidad_vino_blanco_ML\data\raw\winequality-white.csv', delimiter= ';')

vino['good quality'] = [1 if x > 5 else 0 for x in vino.quality]
vino.drop(columns=['quality'], inplace=True)

vino.to_csv(r'.\Analisis_calidad_vino_blanco_ML\data\processed.csv')

vino_processed = pd.read_csv(r'.\Analisis_calidad_vino_blanco_ML\data\processed.csv', index_col=0)

train, test = train_test_split(vino_processed)

train.to_csv(r'.\Analisis_calidad_vino_blanco_ML\data\train.csv')
test.to_csv(r'.\Analisis_calidad_vino_blanco_ML\data\test.csv')
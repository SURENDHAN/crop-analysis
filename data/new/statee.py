import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
df = pd.read_csv("C:/Users/nithi/Downloads/Crop_Production_Statistics.csv/Crop_Production_Statistics.csv")
r = df[df['Crop'].isna()]
nv = {}
for dist, yea, Sea in zip(r['District '], r['Crop_Year'], r['Season']):
    t = df[((df['District '] == dist) & (df['Crop_Year'] == yea) & (df['Season'] == Sea))]['Crop'].value_counts().index
    if len(t) == 0:
        nv[dist] = np.nan
    else:
        nv[dist] = t[-1]
df.loc[:, 'Crop'] = df['Crop'].fillna(df['District '].map(nv))
df.dropna(subset=['Crop'], axis=0, inplace=True)
df.dropna(subset=['Production'], axis=0, inplace=True)
def statee(state):
    try:
        y = df[df['State'] == state]['Crop'].value_counts().sort_values()
        plt.figure(figsize=(13,8))
        plt.barh(y.index, y.values)
        plt.xlabel('Count')
        plt.ylabel('Crop')
        plt.title(f'Crop Distribution in {state}')
        plt.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()
        return plot_base64

    except Exception as e:

        print(f"An error occurred: {e}")
        return None
def yeare(year):
    try:
        re = df[df['Crop_Year'] == year]['Crop'].value_counts().sort_values(ascending=False)
        plt.figure(figsize=(13, 8))
        plt.barh(re.index, re.values) 
        plt.xlabel('Count')
        plt.ylabel('Crop')
        plt.title(f'Crop Distribution in {year}') 
        plt.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()
        return plot_base64
    except Exception as e:
        return f"Error: {e}"
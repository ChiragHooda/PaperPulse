import pandas as pd
from PIL import Image

def replace_num(abstract):
    for i in abstract:
        if i.isdigit():
            abstract = abstract.replace(i, "@")
    return abstract

def get_metrics():
    df = pd.read_csv('assets/metrics.csv', index_col=False)
    model_metrics = df.iloc[:4,:]
    baseline_metrics = df.iloc[4:,:]
    image = Image.open('assets/model.png')

    return model_metrics, baseline_metrics, image
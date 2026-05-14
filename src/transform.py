import pandas as pd
import numpy as np

def load_data(path):
    df = pd.read_csv(path)
    return df

def filter_offensive_players(df):
    df = df.copy()
    return df[df['Pos'].str.contains(r'FW', na=False)]

def select_columns(df):
    columns = [
        'Player','Squad', 'Comp', 'Pos',
        'Min', 'Gls', 'Ast', 'Sh', 'SoT'
    ]
    return df[columns]

def clean_data(df):
    df = df.dropna().copy()
    df = df[df['Min'] > 0].copy()
    return df


def add_metrics(df):
    df = df.copy()

    df['goals_per_90'] = (df['Gls'] / df['Min']) * 90
    df['assists_per_90'] = (df['Ast'] / df['Min']) * 90

    df['shots_per_90'] = (df['Sh'] / df['Min']) * 90
    df['sot_per_90'] = (df['SoT'] / df['Min']) * 90
    

    
    df['shot_accuracy'] = np.where(
        df['Sh'] > 0,
        df['SoT'] / df['Sh'],
        0
    )

    df['goal_efficiency'] = np.where(
        df['Sh'] > 0,
        df['Gls'] / df['Sh'],
        0
    )

    df['contribution'] = df['Gls'] + df['Ast']

    return df

def normalize(df, cols):
    result = df[cols].copy()
    for col in cols:
        min_val = df[col].min()
        max_val = df[col].max()
        
        if max_val - min_val == 0:
            result[col] = 0
        else:
            result[col] = (df[col] - min_val) / (max_val - min_val)
    
    return result

def calculate_score(df):
    df = df.copy()
    
    metrics = ['goals_per_90', 'assists_per_90', 'goal_efficiency', 'shots_per_90']
    norm = normalize(df, metrics)

    df['score'] = (
    norm['goals_per_90'] * 0.4 +
    norm['assists_per_90'] * 0.2 +
    norm['goal_efficiency'] * 0.2 +
    norm['shots_per_90'] * 0.2
)
    return df

def top_attackers(df):
    return df.sort_values(by='contribution', ascending=False)


def run_pipeline(path):
    df = load_data(path)
    df = filter_offensive_players(df)
    df = select_columns(df)
    df = clean_data(df)
    df = add_metrics(df)
    df = calculate_score(df)
    return df


if __name__ == "__main__":
    df = run_pipeline("data/players_data_light-2025_2026.csv")
    
    top = top_attackers(df)
    print(top.head(10))

    df.to_csv("data/clean_attackers.csv", index=False)



    


import psycopg2
from psycopg2.extras import execute_batch
import pandas as pd
import os

def connect():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "football_analysis"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "2520")
    )

def insert_data(df):
    conn = None
    cur = None

    try:
        conn = connect()
        cur = conn.cursor()

        query = """
            INSERT INTO attackers (
                player, squad, competition, position,
                minutes, goals, assists, shots, shots_on_target,
                goals_per_90, assists_per_90, shot_accuracy,
                goal_efficiency, contribution, score
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """

        data = [
            (
                row['Player'],
                row['Squad'],
                row['Comp'],
                row['Pos'],
                int(row['Min']),
                int(row['Gls']),
                int(row['Ast']),
                int(row['Sh']),
                int(row['SoT']),
                float(row['goals_per_90']),
                float(row['assists_per_90']),
                float(row['shot_accuracy']),
                float(row['goal_efficiency']),
                int(row['contribution']),
                float(row['score'])
            )
            for _, row in df.iterrows()
        ]

        execute_batch(cur, query, data, page_size=1000)

        conn.commit()

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error inserting data: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    df = pd.read_csv("data/clean_attackers.csv")
    insert_data(df)
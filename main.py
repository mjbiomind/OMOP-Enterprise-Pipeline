import os
import sqlite3
import pandas as pd
from pipeline import run_omop_etl

def run_sql_analysis():
    print("\n📦 Initializing In-Memory SQL Reporting Engine...")
    conn = sqlite3.connect(":memory:")
    
    # Load the processed outputs into SQL
    person_df = pd.read_csv("data_output/omop_person.csv")
    condition_df = pd.read_csv("data_output/omop_condition_occurrence.csv")
    
    person_df.to_sql("omop_person", conn, index=False, if_exists="replace")
    condition_df.to_sql("omop_condition_occurrence", conn, index=False, if_exists="replace")
    
    # Native SQL query built straight into Python!
    sql_query = """
    SELECT 
        p.person_id,
        p.person_source_value AS patient_guid,
        p.year_of_birth,
        p.gender_source_value AS gender,
        co.condition_source_value AS raw_code,
        co.condition_start_date,
        CASE 
            WHEN co.condition_end_date IS NULL OR co.condition_end_date = '' THEN 'Active Surveillance'
            ELSE 'Resolved / Discharged'
        END AS clinical_status
    FROM omop_person p
    INNER JOIN omop_condition_occurrence co ON p.person_id = co.person_id
    WHERE co.condition_concept_id = 436073;
    """
    
    result_df = pd.read_sql_query(sql_query, conn)
    print("\n=== SQL SURVEILLANCE REPORT ===")
    print(result_df.to_string(index=False))
    conn.close()

if __name__ == "__main__":
    # 1. Run the data migration pipeline
    run_omop_etl()
    # 2. Run the SQL analysis report automatically
    run_sql_analysis()

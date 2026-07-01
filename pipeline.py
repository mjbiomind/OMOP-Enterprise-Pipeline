import pandas as pd

def run_omop_etl():
    print("🚀 Running Enterprise OMOP ETL Pipeline...")
    
    # Ingesting from data_input/
    raw_patients = pd.read_csv("data_input/raw_patients.csv")
    raw_conditions = pd.read_csv("data_input/raw_conditions.csv")
    vocab_map = pd.read_csv("data_input/omop_vocabulary_map.csv")
    
    # 1. Transform PERSON table
    person_df = pd.DataFrame()
    person_df["person_id"] = range(1, len(raw_patients) + 1)
    person_df["person_source_value"] = raw_patients["Id"]
    
    birth_dates = pd.to_datetime(raw_patients["BIRTHDATE"])
    person_df["year_of_birth"] = birth_dates.dt.year
    person_df["month_of_birth"] = birth_dates.dt.month
    person_df["day_of_birth"] = birth_dates.dt.day
    
    gender_map = {"M": 8507, "F": 8532}
    person_df["gender_concept_id"] = raw_patients["GENDER"].map(gender_map).fillna(0).astype(int)
    person_df["gender_source_value"] = raw_patients["GENDER"]
    
    race_map = {"white": 8527, "asian": 8515}
    person_df["race_concept_id"] = raw_patients["RACE"].map(race_map).fillna(0).astype(int)
    person_df["race_source_value"] = raw_patients["RACE"]
    
    person_df.to_csv("data_output/omop_person.csv", index=False)
    
    # 2. Transform CONDITION_OCCURRENCE table
    patient_id_lookup = person_df.set_index("person_source_value")["person_id"].to_dict()
    raw_conditions["CODE"] = raw_conditions["CODE"].astype(str)
    vocab_map["source_code"] = vocab_map["source_code"].astype(str)
    
    mapped_conditions = raw_conditions.merge(vocab_map, left_on="CODE", right_on="source_code", how="left")
    
    condition_df = pd.DataFrame()
    condition_df["condition_occurrence_id"] = range(1, len(mapped_conditions) + 1)
    condition_df["person_id"] = mapped_conditions["PATIENT"].map(patient_id_lookup)
    condition_df["condition_concept_id"] = mapped_conditions["target_concept_id"].fillna(0).astype(int)
    condition_df["condition_source_concept_id"] = mapped_conditions["source_concept_id"].fillna(0).astype(int)
    condition_df["condition_source_value"] = mapped_conditions["CODE"]
    condition_df["condition_start_date"] = mapped_conditions["START"]
    condition_df["condition_end_date"] = mapped_conditions["STOP"].fillna("")
    condition_df["condition_type_concept_id"] = 32020 
    
    condition_df.to_csv("data_output/omop_condition_occurrence.csv", index=False)
    print("🎉 ETL Execution Complete! Target tables saved to data_output/")

if __name__ == "__main__":
    run_omop_etl()

# Enterprise Synthea-to-OMOP CDM ETL & SQL Analytics Pipeline

A production-grade, unified Extract, Transform, Load (ETL) and analytical querying framework built with Python and `pandas`. This pipeline automates the structural and semantic migration of raw synthetic electronic health records (Synthea specification) into standardized tables compliant with the **OHDSI OMOP Common Data Model (CDM) v6.0**, loading them dynamically into an in-memory SQL execution engine.

## 🧬 The Problem & Clinical Rationale
Multi-center clinical research is frequently blocked because healthcare systems document data using vastly different terminologies. For instance, a clinician at one facility logs a PTSD diagnosis using a billing code (**ICD-10-CM: F43.10**), while a system tracker at another facility logs it using an observation concept (**SNOMED-CT: 254153009**). 

The **OMOP Common Data Model** solves this by establishing strict structural constraints and a standard vocabulary crosswalk that maps disparate native terminologies down to unified, global concept identifiers (`concept_id`).

## 🚀 System Architecture & Capabilities
This architecture decouples incoming clinical streams from structural target outputs and embeds relational reporting directly into the pipeline execution loop:

1. **`PERSON` Table Normalization:**
   * Programmatically converts string GUID identifiers (`Id`) into robust integer primary keys (`person_id`).
   * Parses ISO timestamps (`BIRTHDATE`) to calculate discrete integer-isolated columns (`year_of_birth`, `month_of_birth`, `day_of_birth`).
   * Harmonizes native strings (e.g., `"M"`, `"F"`, `"white"`) down to standardized OHDSI Concept IDs (e.g., `8507`, `8532`, `8527`).

2. **`CONDITION_OCCURRENCE` Semantic Mapping:**
   * Maps relational student-keys back to newly minted surrogate integers.
   * Executes a vectorized data merge joining disparate billing and clinical codes down to a unified, global **Standard SNOMED Definition for PTSD (`target_concept_id: 436073`)**.

3. **In-Memory SQL Reporting Engine:**
   * Automatically spins up an ephemeral `sqlite3` database session.
   * Loads the completed output CSV files into live SQL tables.
   * Executes a native relational database query using `CASE WHEN` logic to determine active clinical surveillance status.

## 📁 Repository Directory Blueprint
```text
├── data_input/
│   ├── raw_patients.csv          # Native unstructured demographic fields
│   ├── raw_conditions.csv        # Messy clinical logs with mixed vocabularies
│   └── omop_vocabulary_map.csv   # OHDSI standardized crosswalk dictionary
├── data_output/
│   ├── omop_person.csv           # Structured OMOP CDM Person Table
│   └── omop_condition_occurrence.csv # Standardized Condition Occurrence Table
├── pipeline.py                   # Core ETL Transformation logic functions
├── main.py                       # Unified execution master script (ETL + SQL Engine)
├── requirements.txt              # Pipeline library dependencies
└── README.md                     # Project portfolio documentation
```

## 🛠️ Execution & Deployment

### Prerequisites
* Python 3.8 or higher
* Recommended environment: [GitHub Codespaces](https://github.com)

### 1. Ingest Core Dependencies
```bash
pip install pandas pytest
```

### 2. Run the Unified Pipeline Engine
Execute the master controller script to run both the data transformation and the embedded database analytics queries:
```bash
python main.py
```

## 📊 Analytical Core Output
Running `main.py` seamlessly executes data migrations across files and pipes results directly into a structured SQL matrix visible right inside the runtime terminal console:

```text
🚀 Running Enterprise OMOP ETL Pipeline...
 -> SUCCESS: Saved 'data_output/omop_person.csv'
 -> SUCCESS: Saved 'data_output/omop_condition_occurrence.csv'
🎉 ETL Execution Complete! Target tables saved to data_output/

📦 Initializing In-Memory SQL Reporting Engine...
Reading cohort_query.sql script...
Executing relational query across OMOP tables...

=== SQL SURVEILLANCE REPORT ===
 person_id patient_guid  year_of_birth gender  raw_code condition_start_date     clinical_status
         2        p_002           1992      F    F43.10           2025-06-14 Active Surveillance
         1        p_001           1985      M 254153009           2024-01-10 Resolved / Discharged
```

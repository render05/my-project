





from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os

DATA_FILE = "/opt/airflow/data/customers.csv"
OUTPUT_DIR = "/opt/airflow/output"


# -----------------------------
# STEP 1: EXTRACT CUSTOMERS
# -----------------------------
def extract_customers(ti):

    df = pd.read_csv(DATA_FILE)

    print("Customers Extracted")
    print(df)

    ti.xcom_push(
        key="customers",
        value=df.to_dict("records")
    )


# -----------------------------
# STEP 2: VALIDATE CUSTOMERS
# -----------------------------
def validate_customers(ti):

    customers = ti.xcom_pull(
        task_ids="extract_customers",
        key="customers"
    )

    valid = []

    for customer in customers:

        name = str(customer.get("name", "")).strip()
        email = str(customer.get("email", "")).strip()

        if name and "@" in email:
            valid.append(customer)

    print(f"Valid Customers: {len(valid)}")

    pd.DataFrame(valid).to_csv(
        f"{OUTPUT_DIR}/valid_customers.csv",
        index=False
    )

    ti.xcom_push(
        key="valid_customers",
        value=valid
    )


# -----------------------------
# STEP 3: TRANSFORM CUSTOMERS
# -----------------------------
def transform_customers(ti):

    customers = ti.xcom_pull(
        task_ids="validate_customers",
        key="valid_customers"
    )

    df = pd.DataFrame(customers)

    df["name"] = df["name"].str.title()

    df.to_csv(
        f"{OUTPUT_DIR}/transformed_customers.csv",
        index=False
    )

    print("Data Transformed")
    print(df)

    ti.xcom_push(
        key="transformed_customers",
        value=df.to_dict("records")
    )


# -----------------------------
# STEP 4: LOAD DATABASE
# -----------------------------
def load_database(ti):

    customers = ti.xcom_pull(
        task_ids="transform_customers",
        key="transformed_customers"
    )

    df = pd.DataFrame(customers)

    df.to_csv(
        f"{OUTPUT_DIR}/database_table.csv",
        index=False
    )

    print("Database Loaded Successfully")


# -----------------------------
# STEP 5: EXTRACT FROM DATABASE
# -----------------------------
def extract_from_database(ti):

    df = pd.read_csv(
        f"{OUTPUT_DIR}/database_table.csv"
    )

    print("Data Extracted From Database")
    print(df)

    ti.xcom_push(
        key="db_customers",
        value=df.to_dict("records")
    )


# -----------------------------
# STEP 6: SEND EMAILS
# -----------------------------
def send_welcome_email(ti):

    customers = ti.xcom_pull(
        task_ids="extract_from_database",
        key="db_customers"
    )

    email_file = f"{OUTPUT_DIR}/welcome_emails.txt"

    with open(email_file, "w") as f:

        for customer in customers:

            message = (
                f"To: {customer['email']}\n"
                f"Subject: Welcome\n"
                f"Hello {customer['name']},\n"
                f"Welcome to our platform.\n"
                f"---------------------------------\n\n"
            )

            f.write(message)

            print(message)

    print("Welcome Emails Generated")


# -----------------------------
# DAG
# -----------------------------
with DAG(
    dag_id="customer_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_customers",
        python_callable=extract_customers
    )

    validate_task = PythonOperator(
        task_id="validate_customers",
        python_callable=validate_customers
    )

    transform_task = PythonOperator(
        task_id="transform_customers",
        python_callable=transform_customers
    )

    load_task = PythonOperator(
        task_id="load_database",
        python_callable=load_database
    )

    extract_db_task = PythonOperator(
        task_id="extract_from_database",
        python_callable=extract_from_database
    )

    email_task = PythonOperator(
        task_id="send_welcome_email",
        python_callable=send_welcome_email
    )

    (
        extract_task
        >> validate_task
        >> transform_task
        >> load_task
        >> extract_db_task
        >> email_task
    )
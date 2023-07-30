import os

import psycopg2


def save_answer(user_id: str, answer: str) -> None:
    """
    Function to save the chatbot's answer for a specific user in a PostgreSQL database.

    Parameters:
    user_id (str): The user ID for whom to save the answer.
    answer (str): The chatbot's answer to be saved.

    Returns:
    None

    This function establishes a connection to a PostgreSQL database using the environment variables
    PG_DATABASE, PG_HOST, PG_USER, and PG_PASSWORD to connect to the appropriate database.
    It then updates the 'response' column in the 'data' table for the given user ID with the chatbot's answer.
    After updating the database, the connection is closed.

    If any exception occurs during the execution, it is caught and not raised to the calling function.
    """
    try:
        conn = psycopg2.connect(database=os.getenv("PG_DATABASE"),
                                host=os.getenv("PG_HOST"),
                                user=os.getenv("PG_USER"),
                                password=os.getenv("PG_PASSWORD"))

        cursor = conn.cursor()

        # Execute an SQL query to update the 'response' column in the 'data' table
        cursor.execute("UPDATE data SET response = %s WHERE user_id = %s", (answer, user_id))

        conn.commit()

    except Exception as err:
        # If any exception occurs during the execution, it is caught and not raised to the calling function.
        pass

    finally:
        # Close the connection to the database, whether the operation is successful or not.
        conn.close()

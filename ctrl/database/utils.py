from typing import Any, Callable
import ctrl.config as config


# Database Configuration
DATABASE_PARAMS = {
    'dbname': config.DB_NAME,
    'user': config.DB_USER,
    'password': 'postgres',
    'host': 'localhost'
}


def perform_db_op(operation_func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """
    Performs a database operation within a transaction.
    The operation is a function that gets passed a cursor and any other arguments.
    """
    import psycopg2

    with _get_db_connection() as conn:
        try:
            with conn.cursor() as cur:
                result = operation_func(cur, *args, **kwargs)
            return result
        except psycopg2.DatabaseError as e:
            conn.rollback()
            raise e


def _get_db_connection():
    import psycopg2

    try:
        return psycopg2.connect(**DATABASE_PARAMS)
    except psycopg2.OperationalError as e:
        print(f"Cannot connect to the database: {e}")
        raise e


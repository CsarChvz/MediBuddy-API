import pytest
from sqlalchemy import text

def test_database_connection(db_session): 
    # Ejecutamos directamente, sin 'await'
    result = db_session.execute(text("SELECT current_database()")) 
    
    db_name = result.scalar()
    
    # Según tu docker_utils.py, el nombre es 'test_db'
    assert db_name == "medibuddy"
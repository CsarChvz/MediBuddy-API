import pytest
from sqlalchemy import text

@pytest.mark.asyncio
async def test_database_connection(db_session):
    # Verificar que estamos en la base de datos de test
    result = await db_session.execute(text("SELECT current_database()"))
    db_name = result.scalar()
    
    # Según tu docker_utils.py, el nombre es 'test_db'
    assert db_name == "test_db" 
    assert True
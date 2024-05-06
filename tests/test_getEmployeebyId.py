from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app, get_session
from app import settings



connection_string = str(settings.TEST_DATABASE_URL).replace(
"postgresql", "postgresql+psycopg")

engine = create_engine(
    connection_string)

SQLModel.metadata.create_all(engine)  

with Session(engine) as session:  

    def get_session_override():  
            return session  

    app.dependency_overrides[get_session] = get_session_override 

    client = TestClient(app=app)

def test_get_employee_by_id():
    employee_id = 2
    response = client.get(f"/employee/{employee_id}")
    assert response.status_code == 405

# Testing with id not in db
def test_get_employee_by_id_not_found():
    employee_id = 100
    response = client.get(f"/employee/{employee_id}")
    data = response.json()
    assert response.status_code == 405
    # assert data["detail"] == f"Todo with id {todo_id} not found"

# p with a few changes  
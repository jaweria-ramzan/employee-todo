from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app, get_session
from app import settings



# Test with id available in db 
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

def test_delete_employee():
        employee_id = 35
        response = client.delete(f"/employee/{employee_id}")

        data = response.json()

        assert response.status_code == 200
        assert data["message"] == "Data deleted"


# Test with id not available in db
def test_delete_employee_id_not_found():
        employee_id= 100
        response = client.delete(f"/employee/{employee_id}")

        data = response.json()

        assert response.status_code == 400
        assert data["detail"] == "Data not found"

      

  
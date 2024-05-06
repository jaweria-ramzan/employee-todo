from fastapi.testclient import TestClient
from sqlmodel import Field, Session, SQLModel, create_engine
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

def test_update_employee():
        employee_id = 2
        employee_name = "Updated  content"

        response = client.put(f"/employee/{employee_id}",
            json={"name": employee_name}
        )

        assert response.status_code == 200



def test_update_employee_not_found():
        employee_id = 100
        employee_name = "Updated  content"

        response = client.put(f"/employee/{employee_id}",
            json={"name": employee_name}
        )

        data = response.json()

        assert response.status_code == 400
        assert data["detail"] == "Data not found"

  
# p

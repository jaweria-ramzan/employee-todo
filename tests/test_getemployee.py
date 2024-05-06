from fastapi.testclient import TestClient
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.main import app, get_session
from app import settings




def test_get_employee():

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

        response = client.get("/employee/")
        
        assert response.status_code == 200

#  p 


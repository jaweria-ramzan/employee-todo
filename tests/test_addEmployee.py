from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from httpx._transports.wsgi import WSGITransport
from app.main import app, get_session
from app import settings


connection_string=str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine=create_engine(
    connection_string ,connect_args={"sslmode": "require"}, pool_recycle=300
)

SQLModel.metadata.create_all(engine)
with Session(engine) as session:  

    def get_session_override():  
            return session  

    app.dependency_overrides[get_session] = get_session_override 

    client = TestClient(app=app)

def test_add_employee():


        response = client.post("/employee/",
            json={
                 "id": 35,
                 "name": "test todo name",
                 "age": 4,
                 "gmail": "jj",
                 "address": "mmm",
                 "cnum": 3,
                 }
        )

        data = response.json()

        assert response.status_code == 200
        # assert data["name"] == "test todo name"
        # assert data["id"] == 34

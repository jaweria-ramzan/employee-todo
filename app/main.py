from fastapi import Depends, FastAPI, HTTPException
from typing import Annotated, Optional
from sqlmodel import SQLModel,Field,create_engine,Session, select
from app import settings
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Hello World API", 
    version="0.0.1",
    servers=[
        {
            "url": "http://0.0.0.0:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

class Employee(SQLModel,table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int = Field(index=True)
    gmail: str = Field(index=True)
    address: str = Field(index=True)
    cnum: int = Field(index=True)
    done: Optional[bool] = Field(default=False)

 
connection_string=str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine=create_engine(
    connection_string ,connect_args={"sslmode": "require"}, pool_recycle=300
)

def create_table():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def tb(app:FastAPI):
    print("printing table")
    create_table()
    yield



app = FastAPI(lifespan=tb)


app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    return {"message": "hello World"}


@app.post("/employee/", response_model=Employee)
def create_data(employee: Employee, session: Annotated[Session, Depends(get_session)]):
    if employee.name.strip():
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee
    else:
        raise HTTPException(status_code=400, detail="Title cannot be empty")


@app.delete("/employee/{employee_id}")
async def delete_data(employee_id: int, session: Annotated[Session, Depends(get_session)]):
  employee = session.get(Employee, employee_id)
  if not employee:
    raise HTTPException(status_code=400, detail="Data not found")
  
  session.delete(employee)
  session.commit()
  return {"message": "Data deleted"}


@app.get("/employee/", response_model=list[Employee])
def read_data(session: Annotated[Session, Depends(get_session)]):
    datas = session.exec(select(Employee)).all()
    return datas

@app.put("/employee/{employee_id}")
async def update_data(employee_id: int, employee: Employee, session: Annotated[Session, Depends(get_session)]):
  data_to_update = session.get(Employee, employee_id)
  if not data_to_update:
    raise HTTPException(status_code=400, detail="Data not found")
 
  if employee.name:
    if employee.name.strip():
      data_to_update.name = employee.name
    if employee.done is not None:
        data_to_update.done = employee.done
  
    session.commit()
    session.refresh(data_to_update)
    return data_to_update
  


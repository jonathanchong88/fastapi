import uvicorn
from fastapi import FastAPI, Path, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel, Field
from typing import Tuple
from fastapi.middleware.cors import CORSMiddleware

print ('hello')
# origins = [
#    "http://192.168.211.:8000",
#    "http://localhost",
#    "http://localhost:8080",
# ]
app = FastAPI()
# app.add_middleware(
#    CORSMiddleware,
#    allow_origins=origins,
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
# )
@app.get("/")
async def index():
   return {"message": "Hello World"}
# @app.get("/hello/{name}")
# async def hello(name):
#    return {"name": name}
@app.get("/hello/{name}/{age}")
async def hello(name:str,age:int):
   return {"name": name, "age":age} 
@app.get("/hello")
async def hello(name:str,age:int):
   return {"name": name, "age":age}
@app.get("/hello/{name}")
async def hello(name:str=Path(...,min_length=3,
max_length=10)):
   return {"name": name}
class Student(BaseModel):
   id: int
   name :str = Field(None, title="name of student", max_length=10)
   subjects: List[str] = []
class student(BaseModel):
   id: int
   name :str = Field(None, title="name of student", max_length=10)
   marks: List[int] = []
   percent_marks: float
class percent(BaseModel):
   id:int
   name :str = Field(None, title="name of student", max_length=10)
   percent_marks: float
@app.post("/students/")
async def student_data(s1: Student):
   return s1
@app.post("/students")
async def student_data(name:str=Body(...),
marks:int=Body(...)):
   return {"name":name,"marks": marks}
@app.post("/students")
async def student_data(name:str=Body(...),
marks:int=Body(...)):
   return {"name":name,"marks": marks}
@app.post("/students/{college}")
async def student_data(college:str, age:int, student:Student):
   retval={"college":college, "age":age, **student.dict()}
   return retval
@app.get("/rspheader/")
def set_rsp_headers():
   content = {"message": "Hello World"}
   headers = {"X-Web-Framework": "FastAPI", "Content-Language": "en-US"}
   return JSONResponse(content=content, headers=headers)
@app.post("/marks", response_model=percent)
async def get_percent(s1:student):
   s1.percent_marks=sum(s1.marks)/2
   return s1
class supplier(BaseModel):
   supplierID:int
   supplierName:str
class product(BaseModel):
   productID:int
   prodname:str
   price:int
   supp:supplier
class customer(BaseModel):
   custID:int
   custname:str
   prod:Tuple[product]
@app.post('/invoice')
async def getInvoice(c1:customer):
   return c1
class dependency:
   def __init__(self, id: str, name: str, age: int):
      self.id = id
      self.name = name
      self.age = age 
@app.get("/user/")
async def user(dep: dependency = Depends(dependency)):
   return dep
@app.get("/admin/")
async def admin(dep: dependency = Depends(dependency)):
   return dep 
async def validate(dep: dependency = Depends(dependency)):
   if dep.age > 18:
      raise HTTPException(status_code=400, detail="You are not eligible")
@app.get("/users/", dependencies=[Depends(validate)])
async def user():
   return {"message": "You are eligible"}
if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
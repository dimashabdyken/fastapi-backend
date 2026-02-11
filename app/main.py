import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas


app = FastAPI()

models.Base.metadata.create_all(bind=models.engine)


@app.get("/")
def read_root():
    return {"FastApi project!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(models.get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(models.get_db)):
    return crud.create_task(db=db, task=task)


@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(models.get_db)):
    db_task = crud.delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

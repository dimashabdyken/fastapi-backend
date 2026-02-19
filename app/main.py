import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, database, schemas

app = FastAPI(title="DevOps ToDo API")


@app.get("/")
def read_root():
    return {"message": "FastAPI connected to PostgreSQL!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks/", response_model=list[schemas.TaskResponse])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    return crud.create_task(db=db, task=task)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    db_task = crud.delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(database.get_db),
):
    db_task = crud.update_task(db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from schemas import ProjectCreate, ContractCreate, ClauseCreate, ReviewCreate, ProjectResponse, ContractResponse, Clause, Review
from crud import (
    get_projects, create_project, update_project, delete_project,
    get_contracts, create_contract, update_contract, delete_contract,
    get_clauses, create_clause, update_clause, delete_clause,
    get_reviews, create_review
)
from db import SessionLocal

api_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@api_router.get("/projects", response_model=List[ProjectResponse])
def read_projects(db: Session = Depends(get_db)):
    return get_projects(db)


@api_router.post("/projects", response_model=ProjectResponse)
def add_project(project: ProjectCreate, db: Session = Depends(get_db)):
    return create_project(db, project)


@api_router.put("/projects/{project_id}", response_model=ProjectResponse)
def modify_project(project_id: UUID, updated_project: ProjectCreate, db: Session = Depends(get_db)):
    project = update_project(db, project_id, updated_project)
    if project:
        return project
    raise HTTPException(status_code=404, detail="Project not found")


@api_router.delete("/projects/{project_id}")
def remove_project(project_id: UUID, db: Session = Depends(get_db)):
    if delete_project(db, project_id):
        return {"message": "Project deleted"}
    raise HTTPException(status_code=404, detail="Project not found")


@api_router.get("/contracts", response_model=List[ContractResponse])
def read_contracts(db: Session = Depends(get_db)):
    return get_contracts(db)


@api_router.post("/contracts", response_model=ContractResponse)
def add_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    return create_contract(db, contract)


@api_router.put("/contracts/{contract_id}", response_model=ContractResponse)
def modify_contract(contract_id: UUID, updated_contract: ContractCreate, db: Session = Depends(get_db)):
    contract = update_contract(db, contract_id, updated_contract)
    if contract:
        return contract
    raise HTTPException(status_code=404, detail="Contract not found")


@api_router.delete("/contracts/{contract_id}")
def remove_contract(contract_id: UUID, db: Session = Depends(get_db)):
    if delete_contract(db, contract_id):
        return {"message": "Contract deleted"}
    raise HTTPException(status_code=404, detail="Contract not found")


@api_router.get("/clauses", response_model=List[Clause])
def read_clauses(db: Session = Depends(get_db)):
    return get_clauses(db)


@api_router.post("/clauses", response_model=Clause)
def add_clause(clause: ClauseCreate, db: Session = Depends(get_db)):
    return create_clause(db, clause)


@api_router.put("/clauses/{clause_id}", response_model=Clause)
def modify_clause(clause_id: UUID, updated_clause: ClauseCreate, db: Session = Depends(get_db)):
    clause = update_clause(db, clause_id, updated_clause)
    if clause:
        return clause
    raise HTTPException(status_code=404, detail="Clause not found")


@api_router.delete("/clauses/{clause_id}")
def remove_clause(clause_id: UUID, db: Session = Depends(get_db)):
    if delete_clause(db, clause_id):
        return {"message": "Clause deleted"}
    raise HTTPException(status_code=404, detail="Clause not found")


@api_router.get("/reviews", response_model=List[Review])
def read_reviews(db: Session = Depends(get_db)):
    return get_reviews(db)


@api_router.post("/reviews/start", response_model=Review)
def start_review(review: ReviewCreate, db: Session = Depends(get_db)):
    return create_review(db, review)

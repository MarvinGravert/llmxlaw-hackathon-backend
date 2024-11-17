from typing import List
from sqlalchemy.orm import Session
from schemas import ProjectCreate, ContractCreate, ClauseCreate, ReviewCreate, ProjectDB, ContractDB, ClauseDB, ReviewDB
from models import ProjectModel, ContractModel, ClauseModel, ReviewModel
from sqlalchemy import UUID


def get_projects(db: Session) -> List[ProjectDB]:
    projects = db.query(ProjectModel).all()
    project_list = []
    for project in projects:
        contracts = db.query(ContractModel).filter(
            ContractModel.project_id == project.id).all()
        contract_list = []
        for contract in contracts:
            clauses = db.query(ClauseModel).filter(
                ClauseModel.contract_id == contract.id).all()
            clause_list = [ClauseDB(id=clause.id, text=clause.text, title=clause.title,
                                    contract_id=clause.contract_id) for clause in clauses]
            contract_list.append(ContractDB(
                id=contract.id, title=contract.title, project_id=contract.project_id, clauses=clause_list))
        project_list.append(
            ProjectDB(id=project.id, title=project.title, contracts=contract_list))
    return project_list


def create_project(db: Session, project: ProjectCreate) -> ProjectDB:
    db_project = ProjectModel(
        title=project.title
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return ProjectDB(id=db_project.id, title=db_project.title, contracts=[])


def update_project(db: Session, project_id: UUID, updated_project: ProjectCreate) -> ProjectDB | None:
    db_project = db.query(ProjectModel).filter(
        ProjectModel.id == project_id).first()
    if db_project:
        db_project.title = updated_project.title
        db.commit()
        db.refresh(db_project)
        return ProjectDB(id=db_project.id, title=db_project.title, contracts=[])
    return None


def delete_project(db: Session, project_id: UUID) -> bool:
    db_project = db.query(ProjectModel).filter(
        ProjectModel.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
        return True
    return False

# Similar CRUD functions for Contract, Clause, and Review


def get_contracts(db: Session) -> List[ContractDB]:
    contracts = db.query(ContractModel).all()
    contract_list = []
    for contract in contracts:
        clauses = db.query(ClauseModel).filter(
            ClauseModel.contract_id == contract.id).all()
        clause_list = [ClauseDB(id=clause.id, text=clause.text, title=clause.title,
                                contract_id=clause.contract_id) for clause in clauses]
        contract_list.append(ContractDB(id=contract.id, title=contract.title,
                             project_id=contract.project_id, clauses=clause_list))
    return contract_list


def create_contract(db: Session, contract: ContractCreate) -> ContractDB:
    db_contract = ContractModel(
        title=contract.title,
        project_id=contract.project_id,
        metadata_info=contract.metadata_info  # Default empty string
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)

    # Find and associate clauses
    clause_list = []
    for clause in contract.clauses:
        db_clause = db.query(ClauseModel).filter(
            ClauseModel.id == clause.id).first()
        if db_clause:
            db_clause.contract_id = db_contract.id
            db.commit()
            db.refresh(db_clause)
            clause_list.append(ClauseDB(id=db_clause.id, text=db_clause.text,
                               title=db_clause.title, contract_id=db_clause.contract_id))

    return ContractDB(id=db_contract.id, title=db_contract.title, project_id=db_contract.project_id, clauses=clause_list)


def update_contract(db: Session, contract_id: UUID, updated_contract: ContractCreate) -> ContractDB | None:
    db_contract = db.query(ContractModel).filter(
        ContractModel.id == contract_id).first()
    if db_contract:
        db_contract.title = updated_contract.title
        db_contract.project_id = updated_contract.project_id
        db_contract.metadata_info = updated_contract.metadata_info  # Default empty string
        db.commit()
        db.refresh(db_contract)

        # Find and associate clauses
        clause_list = []
        for clause in updated_contract.clauses:
            db_clause = db.query(ClauseModel).filter(
                ClauseModel.id == clause.id).first()
            if db_clause:
                db_clause.contract_id = db_contract.id
                db.commit()
                db.refresh(db_clause)
                clause_list.append(ClauseDB(id=db_clause.id, text=db_clause.text,
                                   title=db_clause.title, contract_id=db_clause.contract_id))

        return ContractDB(id=db_contract.id, title=db_contract.title, project_id=db_contract.project_id, clauses=clause_list)
    return None


def delete_contract(db: Session, contract_id: UUID) -> bool:
    db_contract = db.query(ContractModel).filter(
        ContractModel.id == contract_id).first()
    if db_contract:
        db.delete(db_contract)
        db.commit()
        return True
    return False


def get_clauses(db: Session) -> List[ClauseDB]:
    clauses = db.query(ClauseModel).all()
    return [ClauseDB(id=clause.id, text=clause.text, title=clause.title, contract_id=clause.contract_id) for clause in clauses]


def create_clause(db: Session, clause: ClauseCreate) -> ClauseDB:
    db_clause = ClauseModel(
        text=clause.text,
        title=clause.title,
        contract_id=clause.contract_id
    )
    db.add(db_clause)
    db.commit()
    db.refresh(db_clause)
    return ClauseDB(id=db_clause.id, text=db_clause.text, title=db_clause.title, contract_id=db_clause.contract_id)


def update_clause(db: Session, clause_id: UUID, updated_clause: ClauseCreate) -> ClauseDB | None:
    db_clause = db.query(ClauseModel).filter(
        ClauseModel.id == clause_id).first()
    if db_clause:
        db_clause.text = updated_clause.text
        db_clause.title = updated_clause.title
        db_clause.contract_id = updated_clause.contract_id
        db.commit()
        db.refresh(db_clause)
        return ClauseDB(id=db_clause.id, text=db_clause.text, title=db_clause.title, contract_id=db_clause.contract_id)
    return None


def delete_clause(db: Session, clause_id: UUID) -> bool:
    db_clause = db.query(ClauseModel).filter(
        ClauseModel.id == clause_id).first()
    if db_clause:
        db.delete(db_clause)
        db.commit()
        return True
    return False


def get_reviews(db: Session) -> List[ReviewDB]:
    reviews = db.query(ReviewModel).all()
    return [ReviewDB(id=review.id, clause=review.clause, score=review.score, good=review.good, bad=review.bad) for review in reviews]


def create_review(db: Session, review: ReviewCreate) -> ReviewDB:
    db_review = ReviewModel(
        clause=review.clause,
        score=review.score,
        good=review.good,
        bad=review.bad
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return ReviewDB(id=db_review.id, clause=db_review.clause, score=db_review.score, good=db_review.good, bad=db_review.bad)

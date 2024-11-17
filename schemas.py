from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from uuid import UUID, uuid4
from pydantic import ConfigDict

# Base Schemas


class ClauseBase(BaseModel):
    text: str
    title: str


class ContractBase(BaseModel):
    title: str
    metadata_info: str = ""  # Default empty string


class ProjectBase(BaseModel):
    title: str


class ReviewBase(BaseModel):
    clause: str
    score: float
    good: List[str]
    bad: List[str]

# Request Schemas


class ClauseCreate(ClauseBase):
    contract_id: UUID


class ContractCreate(ContractBase):
    project_id: UUID
    clauses: List[ClauseCreate] = Field(default_factory=list)


class ProjectCreate(ProjectBase):
    pass


class ReviewCreate(ReviewBase):
    pass

# Response Schemas


class Clause(ClauseBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = Field(default_factory=uuid4)
    text: str
    title: str
    contract_id: UUID


class ContractResponse(ContractBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = Field(default_factory=uuid4)
    title: str
    project_id: UUID
    clauses: List[Clause] = Field(default_factory=list)


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = Field(default_factory=uuid4)
    title: str
    contracts: List[ContractResponse] = Field(default_factory=list)


class Review(ReviewBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = Field(default_factory=uuid4)
    clause: str
    score: float
    good: List[str]
    bad: List[str]

# Database Schemas


class ClauseDB(ClauseBase):
    id: UUID
    contract_id: UUID


class ContractDB(ContractBase):
    id: UUID
    project_id: UUID
    clauses: List[ClauseDB]


class ProjectDB(ProjectBase):
    id: UUID
    contracts: List[ContractDB]


class ReviewDB(ReviewBase):
    id: UUID

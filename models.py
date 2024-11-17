from uuid import uuid4
from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
from db import Base


class ProjectModel(Base):
    __tablename__ = "projects"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    title = Column(String, index=True)


class ContractModel(Base):
    __tablename__ = "contracts"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    title = Column(String, index=True)
    project_id = Column(UUID(as_uuid=True))  # Removed ForeignKey
    metadata_info = Column(String, default="")  # Default empty string


class ClauseModel(Base):
    __tablename__ = "clauses"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    text = Column(String)
    title = Column(String)
    contract_id = Column(UUID(as_uuid=True))  # Removed ForeignKey


class ReviewModel(Base):
    __tablename__ = "reviews"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    clause = Column(String)
    score = Column(Float)
    good = Column(String)
    bad = Column(String)

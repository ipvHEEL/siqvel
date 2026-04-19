from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str = ""
    owner_id: int


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    status: str = Field(default="todo", pattern="^(todo|in_progress|done)$")
    project_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int

    class Config:
        from_attributes = True

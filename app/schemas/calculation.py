from enum import Enum
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator


class CalculationType(str, Enum):
    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"


class CalculationBase(BaseModel):
    type: CalculationType = Field(
        ...,
        description="Operation to perform",
        examples=["addition"]
    )
    inputs: List[float] = Field(
        ...,
        description="Numbers used in the calculation",
        examples=[[8, 2, 1]],
        min_length=2
    )

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, value):
        valid_types = {item.value for item in CalculationType}
        if not isinstance(value, str) or value.lower() not in valid_types:
            raise ValueError(
                f"Calculation type must be one of: {', '.join(sorted(valid_types))}"
            )
        return value.lower()

    @field_validator("inputs", mode="before")
    @classmethod
    def validate_inputs_list(cls, value):
        if not isinstance(value, list):
            raise ValueError("Inputs must be provided as a list")
        return value

    @model_validator(mode="after")
    def validate_inputs(self):
        if len(self.inputs) < 2:
            raise ValueError("A calculation requires at least two numbers")
        if self.type == CalculationType.DIVISION and any(num == 0 for num in self.inputs[1:]):
            raise ValueError("Division by zero is not allowed")
        return self

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {"type": "addition", "inputs": [8, 2, 1]},
                {"type": "division", "inputs": [20, 5]}
            ]
        }
    )


class CalculationCreate(CalculationBase):
    user_id: UUID = Field(
        ...,
        description="User ID linked to this calculation",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "multiplication",
                "inputs": [4, 3, 2],
                "user_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
    )


class CalculationUpdate(BaseModel):
    inputs: Optional[List[float]] = Field(
        None,
        description="Revised list of numbers for the calculation",
        examples=[[12, 4]],
        min_length=2
    )

    @model_validator(mode="after")
    def validate_inputs(self):
        if self.inputs is not None and len(self.inputs) < 2:
            raise ValueError("A calculation requires at least two numbers")
        return self

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "inputs": [12, 4]
            }
        }
    )


class CalculationResponse(CalculationBase):
    id: UUID = Field(
        ...,
        description="Unique identifier for the calculation",
        examples=["123e4567-e89b-12d3-a456-426614174999"]
    )
    user_id: UUID = Field(
        ...,
        description="User ID associated with this calculation",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    created_at: datetime = Field(
        ...,
        description="Date and time the calculation was created"
    )
    updated_at: datetime = Field(
        ...,
        description="Date and time the calculation was last updated"
    )
    result: float = Field(
        ...,
        description="Calculated output",
        examples=[24.0]
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174999",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "type": "multiplication",
                "inputs": [4, 3, 2],
                "result": 24.0,
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        }
    )
import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from app.schemas.calculation import (
    CalculationType,
    CalculationBase,
    CalculationCreate,
    CalculationUpdate,
    CalculationResponse,
)


def test_calculation_type_enum_values():
    assert CalculationType.ADDITION.value == "addition"
    assert CalculationType.SUBTRACTION.value == "subtraction"
    assert CalculationType.MULTIPLICATION.value == "multiplication"
    assert CalculationType.DIVISION.value == "division"


def test_calculation_base_valid_addition():
    data = {
        "type": "addition",
        "inputs": [10.5, 3, 2]
    }
    calc = CalculationBase(**data)
    assert calc.type == CalculationType.ADDITION
    assert calc.inputs == [10.5, 3, 2]


def test_calculation_base_valid_subtraction():
    data = {
        "type": "subtraction",
        "inputs": [20, 5.5]
    }
    calc = CalculationBase(**data)
    assert calc.type == CalculationType.SUBTRACTION
    assert calc.inputs == [20, 5.5]


def test_calculation_base_case_insensitive_type():
    for type_variant in ["Addition", "ADDITION", "AdDiTiOn"]:
        data = {"type": type_variant, "inputs": [1, 2]}
        calc = CalculationBase(**data)
        assert calc.type == CalculationType.ADDITION


def test_calculation_base_invalid_type():
    data = {
        "type": "modulus",
        "inputs": [10, 3]
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationBase(**data)

    assert "Calculation type must be one of" in str(exc_info.value)


def test_calculation_base_inputs_not_list():
    data = {
        "type": "addition",
        "inputs": "not a list"
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationBase(**data)

    assert "Inputs must be provided as a list" in str(exc_info.value)


def test_calculation_base_insufficient_inputs():
    data = {
        "type": "addition",
        "inputs": [5]
    }
    with pytest.raises(ValidationError):
        CalculationBase(**data)


def test_calculation_base_empty_inputs():
    data = {
        "type": "multiplication",
        "inputs": []
    }
    with pytest.raises(ValidationError):
        CalculationBase(**data)


def test_calculation_base_division_by_zero():
    data = {
        "type": "division",
        "inputs": [100, 0]
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationBase(**data)

    assert "Division by zero is not allowed" in str(exc_info.value)


def test_calculation_base_division_by_zero_in_middle():
    data = {
        "type": "division",
        "inputs": [100, 5, 0, 2]
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationBase(**data)

    assert "Division by zero is not allowed" in str(exc_info.value)


def test_calculation_base_division_zero_numerator_ok():
    data = {
        "type": "division",
        "inputs": [0, 5, 2]
    }
    calc = CalculationBase(**data)
    assert calc.inputs[0] == 0


def test_calculation_create_valid():
    user_id = uuid4()
    data = {
        "type": "multiplication",
        "inputs": [2, 3, 4],
        "user_id": str(user_id)
    }
    calc = CalculationCreate(**data)
    assert calc.type == CalculationType.MULTIPLICATION
    assert calc.inputs == [2, 3, 4]
    assert calc.user_id == user_id


def test_calculation_create_missing_user_id():
    data = {
        "type": "addition",
        "inputs": [1, 2]
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)

    assert "user_id" in str(exc_info.value)


def test_calculation_create_invalid_user_id():
    data = {
        "type": "subtraction",
        "inputs": [10, 5],
        "user_id": "not-a-valid-uuid"
    }
    with pytest.raises(ValidationError):
        CalculationCreate(**data)


def test_calculation_update_valid():
    data = {
        "inputs": [42, 7]
    }
    calc = CalculationUpdate(**data)
    assert calc.inputs == [42, 7]


def test_calculation_update_all_fields_optional():
    data = {}
    calc = CalculationUpdate(**data)
    assert calc.inputs is None


def test_calculation_update_insufficient_inputs():
    data = {
        "inputs": [5]
    }
    with pytest.raises(ValidationError):
        CalculationUpdate(**data)


def test_calculation_response_valid():
    data = {
        "id": str(uuid4()),
        "user_id": str(uuid4()),
        "type": "addition",
        "inputs": [10, 5],
        "result": 15.0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    calc = CalculationResponse(**data)
    assert calc.result == 15.0
    assert calc.type == CalculationType.ADDITION


def test_calculation_response_missing_result():
    data = {
        "id": str(uuid4()),
        "user_id": str(uuid4()),
        "type": "multiplication",
        "inputs": [2, 3],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationResponse(**data)

    assert "result" in str(exc_info.value)


def test_multiple_calculations_with_different_types():
    user_id = uuid4()

    calcs_data = [
        {"type": "addition", "inputs": [1, 2, 3], "user_id": str(user_id)},
        {"type": "subtraction", "inputs": [10, 3], "user_id": str(user_id)},
        {"type": "multiplication", "inputs": [2, 3, 4], "user_id": str(user_id)},
        {"type": "division", "inputs": [100, 5], "user_id": str(user_id)},
    ]

    calcs = [CalculationCreate(**data) for data in calcs_data]

    assert len(calcs) == 4
    assert calcs[0].type == CalculationType.ADDITION
    assert calcs[1].type == CalculationType.SUBTRACTION
    assert calcs[2].type == CalculationType.MULTIPLICATION
    assert calcs[3].type == CalculationType.DIVISION


def test_schema_with_large_numbers():
    data = {
        "type": "multiplication",
        "inputs": [1e10, 1e10, 1e10]
    }
    calc = CalculationBase(**data)
    assert all(isinstance(x, float) for x in calc.inputs)


def test_schema_with_negative_numbers():
    data = {
        "type": "addition",
        "inputs": [-5, -10, 3.5]
    }
    calc = CalculationBase(**data)
    assert calc.inputs == [-5, -10, 3.5]


def test_schema_with_mixed_int_and_float():
    data = {
        "type": "subtraction",
        "inputs": [100, 23.5, 10, 6.7]
    }
    calc = CalculationBase(**data)
    assert len(calc.inputs) == 4


def test_calculation_base_model_validator_raises_for_short_inputs():
    calc = CalculationBase.model_construct(
        type=CalculationType.ADDITION,
        inputs=[5]
    )

    with pytest.raises(ValueError, match="A calculation requires at least two numbers"):
        calc.validate_inputs()


def test_calculation_update_model_validator_raises_for_short_inputs():
    calc = CalculationUpdate.model_construct(inputs=[5])

    with pytest.raises(ValueError, match="A calculation requires at least two numbers"):
        calc.validate_inputs()
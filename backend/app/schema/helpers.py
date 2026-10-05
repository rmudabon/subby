from pydantic import BaseModel


def find_invalid_null_fields(
    model: BaseModel, nullable_fields: set[str] | None = None
) -> list[str]:
    nullable_fields = nullable_fields or set()
    checkable_fields = model.model_fields_set - nullable_fields
    return [
        field_name
        for field_name in checkable_fields
        if getattr(model, field_name) is None
    ]

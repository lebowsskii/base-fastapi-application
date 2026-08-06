import orjson
import sqlalchemy as sa
from pydantic import TypeAdapter
from pydantic.json import pydantic_encoder
from sqlalchemy.dialects.postgresql import JSONB


class PydanticType(sa.types.TypeDecorator):
    """Pydantic type.
    SAVING:
    - Uses SQLAlchemy JSON type under the hood.
    - Acceps the pydantic model and converts it to a dict on save.
    - SQLAlchemy engine JSON-encodes the dict to a string.
    RETRIEVING:
    - Pulls the string from the database.
    - SQLAlchemy engine JSON-decodes the string to a dict.
    - Uses the dict to create a pydantic model.
    """

    impl = sa.dialects.postgresql.JSONB

    def __init__(self, pydantic_type):
        super().__init__()
        self.pydantic_type = pydantic_type
        self.type_adapter = TypeAdapter(pydantic_type)

    def load_dialect_impl(self, dialect):
        # Use JSONB for PostgreSQL and JSON for other databases.
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        else:
            return dialect.type_descriptor(sa.JSON())

    def process_bind_param(self, value, dialect):
        return self.type_adapter.dump_python(value) if value else None

    def process_result_value(self, value, dialect):
        return self.type_adapter.validate_python(value) if value else None


def json_serializer(obj) -> str:
    return orjson.dumps(obj, default=pydantic_encoder).decode("utf-8")

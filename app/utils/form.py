import orjson
from pydantic import TypeAdapter
from wtforms import fields


class PydanticField(fields.TextAreaField):
    def __init__(self, *args, **kwargs):
        self.pydantic_type = kwargs.pop("pydantic_type")
        self.type_adapter = TypeAdapter(self.pydantic_type)
        super().__init__(*args, **kwargs)

    def _value(self):
        if self.data:
            return self.type_adapter.dump_json(self.data).decode("utf-8")
        return ""

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = self.type_adapter.validate_json(valuelist[0])
            except ValueError:
                raise ValueError("Invalid data")
        else:
            self.data = None


class DictField(fields.TextAreaField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _value(self):
        if self.data:
            return orjson.dumps(self.data).decode("utf-8")
        return ""

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = orjson.loads(valuelist[0])
            except ValueError:
                raise ValueError("Invalid data")
        else:
            self.data = None

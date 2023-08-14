from marshmallow import fields

class EnumToDictionary(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        
        return {
            'key': value.name,
            'value': value.value
        }
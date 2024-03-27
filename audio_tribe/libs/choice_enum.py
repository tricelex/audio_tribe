from enum import Enum

from django.utils.safestring import mark_safe

from audio_tribe.libs.enum import Attribute
from audio_tribe.libs.enum import AttributeSerializer


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.value[0], x.value[1]) for x in cls)

    @classmethod
    def get_all_choice_values(cls):
        return [x.value[0] for x in cls]

    @classmethod
    def get_all_choice_descriptions(cls):
        return [x.value[1] for x in cls]

    @classmethod
    def formatted_choices(cls):
        return tuple(
            (x.value[0], mark_safe("<span>%s</span>" % x.value[1])) for x in cls
        )

    @property
    def display(self):
        return self.value[1]

    @property
    def choice_value(self):
        return self.value[0]

    @classmethod
    def init_from_choice_value(cls, value):
        for x in cls:
            if x.choice_value == value:
                return x

    @property
    def help_text(self):
        if len(self.value) > 2:
            return self.value[2]


class SerializableEnum(ChoiceEnum):
    def selected_choice_to_json(self):
        attribute = Attribute(val=self.value[0], display=self.value[1], code=self.name)
        return AttributeSerializer(attribute).data

    @classmethod
    def to_json(cls, serializer_class=AttributeSerializer):
        attributes = []
        for x in cls:
            attribute = Attribute(val=x.value[0], display=x.value[1], code=x.name)
            attributes.append(attribute)
        return serializer_class(attributes, many=True).data

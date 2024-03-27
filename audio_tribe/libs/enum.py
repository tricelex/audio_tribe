import json

import six
from django.conf import settings
from rest_framework import serializers


class Enumeration:
    """
    A small helper class for more readable enumerations,
    and compatible with Django's choice convention.
    You may just pass the instance of this class as the choices
    argument of model/form fields.

    Example:
            MY_ENUM = Enumeration([
                    (100, 'MY_NAME', 'My verbose name'),
                    (200, 'MY_AGE', 'My verbose age'),
            ])
            assert MY_ENUM.MY_AGE == 200
            assert MY_ENUM[1] == (200, 'My verbose age')
    """

    def __init__(self, enum_list):
        self.enum_list_full = enum_list
        self.enum_list = [(item[0], item[2]) for item in enum_list]
        self.enum_dict = {}
        self.enum_code = {}
        self.languages = {}
        self.enum_display = {}
        for item in enum_list:
            self.enum_dict[item[1]] = item[0]
            self.enum_display[item[0]] = item[2]
            self.enum_code[item[0]] = item[1]
            i = 0
            for language_code, language in settings.LANGUAGES:
                try:
                    translation = item[2 + i]
                except IndexError:
                    translation = item[2]
                self.languages[str(item[0]) + language_code] = translation
                i += 1

    def __contains__(self, v):
        return v in self.enum_list

    def __len__(self):
        return len(self.enum_list)

    def __getitem__(self, v):
        if isinstance(v, six.string_types):
            return self.enum_dict[v]
        elif isinstance(v, int):
            return self.enum_list[v]

    def __getattr__(self, name):
        try:
            return self.enum_dict[name]
        except KeyError:
            raise AttributeError

    def __iter__(self):
        return self.enum_list.__iter__()

    def __repr__(self):
        return "Enum(%s)" % self.enum_list_full.__repr__()

    def get_display_name(self, v):
        return self.enum_display[v]

    def get_display_code(self, v):
        return self.enum_code[v]

    def get_language_name(self, v, language_code):
        return self.languages[str(v[0]) + language_code]


class Attribute:
    def __init__(self, val, display, code):
        self.val = val
        self.display = display
        self.code = code


class HelpTextAttribute:
    def __init__(self, val, display, code, help_text):
        self.val = val
        self.display = display
        self.code = code
        self.help_text = help_text


class GroupAttribute:
    def __init__(self, val, display, code, group, help_text):
        self.val = val
        self.display = display
        self.code = code
        self.group = group
        self.help_text = help_text


class AttributeSerializer(serializers.Serializer):
    val = serializers.IntegerField()
    display = serializers.CharField()
    code = serializers.CharField()


class CharAttributeSerializer(serializers.Serializer):
    val = serializers.CharField()
    display = serializers.CharField()
    code = serializers.CharField()


class GroupCharAttributeSerializer(serializers.Serializer):
    val = serializers.CharField()
    display = serializers.CharField()
    code = serializers.CharField()
    group = serializers.CharField()
    help_text = serializers.CharField()


class HelpTextAttributeSerializer(serializers.Serializer):
    val = serializers.CharField()
    display = serializers.CharField()
    code = serializers.CharField()
    help_text = serializers.CharField()


class SerializableEnumeration(Enumeration):
    def get_display_json(self, v):
        return json.dumbs({self.enum_code[v]: self.enum_display[v]})

    # def to_json(self):
    #     return [{'val': key, 'display': name, 'code': self.get_display_code(key)} for key, name in self.enum_list]

    def to_json(self, serializer_class=AttributeSerializer):
        attributes = []
        for key, name in self.enum_list:
            attribute = Attribute(
                val=key, display=name, code=self.get_display_code(key)
            )
            attributes.append(attribute)
        return serializer_class(attributes, many=True).data

from dataclasses import dataclass
from datetime import datetime
from os import path
from typing import Any, cast, TypeVar, Generic

from jsons import (
    dump,
    dumps,
    NoneType,
    load,
    loads,
    JsonsError,
    set_deserializer,
    set_serializer,
    set_validator,
    suppress_warnings,
    default_nonetype_deserializer,
)

T = TypeVar("T")

JSON_FILE_EXTENSION: str = ".json"
WRITE: str = "w"
READ: str = "r"
JSON_PARSE_ERROR = '{"error": "Object could not be parsed due to json issue"}'
# TODO Issue #??: Jsons library incorrectly dumps class method
KEYS_TO_REMOVE = ["from_json", "from_json_file", "from_json_object"]


@dataclass
class Serializable(Generic[T]):
    """
    Serializable class with methods to convert to json
    """

    def to_json(self, strip_privates: bool = True) -> str:
        """
        Serialize to json string
        :param strip_privates: strip private variables
        :return: the json string representation of this object
        """
        return write_json(self, strip_privates)

    def to_json_object(self, strip_privates: bool = True) -> Any:
        """
        Serialize to json object
        :param strip_privates: strip private variables
        :return: the json representation of this object
        """
        return write_json_object(self, strip_privates)

    def to_json_file(
        self, file_name: str, file_path: str = "", strip_privates: bool = True
    ) -> None:
        """
        Serialize an object to a json file
        :param file_name: File name
        :param file_path: File path
        :param strip_privates: Strip private variables
        """
        write_json_file(self, file_name, file_path, strip_privates)

    @classmethod
    def from_json(cls, data: str) -> T:
        """
        Deserialize the provided data string into the specified instance
        :param data: JSON string
        """
        set_deserializers()
        return cast(T, loads(data, cls))

    @classmethod
    def from_json_object(cls, data: object) -> T:
        """
        Deserialize the provided data object into the specified instance
        :param data: JSON object
        """
        set_deserializers()
        return cast(T, load(data, cls))

    @classmethod
    def from_json_file(cls, file_name: str, file_path: str = "") -> T:
        """
        Deserialize the provided file into the specified instance
        :param file_name: File name
        :param file_path: File path
        """
        json_file_path: str = path.join(file_path, file_name + JSON_FILE_EXTENSION)
        with open(json_file_path, READ) as json_file:
            data = json_file.read()
            target = cls.from_json(data)
        return target


def _remove_key(obj: Any, key_to_remove: str) -> Any:
    """
    Remove key from object recursively
    :param obj: Any object
    :param key_to_remove: key to remove
    """
    if isinstance(obj, dict):
        for key in list(obj.keys()):
            if key == key_to_remove:
                del obj[key]
            else:
                _remove_key(obj[key], key_to_remove)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            if obj[i] == key_to_remove:
                del obj[i]
            else:
                _remove_key(obj[i], key_to_remove)


def write_json(object_to_write: object, strip_privates: bool = True) -> str:
    """
    Serialize to json string
    :param object_to_write: object to write to json
    :param strip_privates: strip private variables
    :return: the json string representation of this object
    """
    set_serializers()
    suppress_warnings()
    try:
        json_object = write_json_object(object_to_write, strip_privates)
        json_string = cast(
            str, dumps(json_object, strip_privates=strip_privates, strip_nulls=True)
        )
        return json_string
    except JsonsError:
        return JSON_PARSE_ERROR


def write_json_object(object_to_write: object, strip_privates: bool = True) -> object:
    """
    Serialize to json object
    :param object_to_write: object to write to json
    :param strip_privates: strip private variables
    :return: the json representation of this object
    """
    set_serializers()
    suppress_warnings()
    try:
        json_object = dump(
            object_to_write, strip_privates=strip_privates, strip_nulls=True
        )
        for key in KEYS_TO_REMOVE:
            _remove_key(json_object, key)
        return json_object
    except JsonsError:
        return JSON_PARSE_ERROR


def write_json_file(
    object_to_write: object,
    file_name: str,
    file_path: str = "",
    strip_privates: bool = True,
) -> None:
    """
    Serialize json data string to json file
    :param object_to_write: object to write to json
    :param file_name: File name
    :param file_path: File path
    :param strip_privates: strip private variables
    """
    json_file_path: str = path.join(file_path, file_name + JSON_FILE_EXTENSION)
    with open(json_file_path, WRITE) as json_file:
        json_file.write(write_json(object_to_write, strip_privates))


def set_serializers() -> None:
    """Set serializers for jsons to use to cast specific classes"""

    # Local import to minimize jsons usage across files
    from .group import ElementModP, ElementModQ

    set_serializer(lambda p, **_: str(p), ElementModP)
    set_serializer(lambda q, **_: str(q), ElementModQ)
    set_serializer(lambda dt, **_: dt.isoformat(), datetime)


def set_deserializers() -> None:
    """Set deserializers and validators for json to use to cast specific classes"""

    # Local import to minimize jsons usage across files
    from .group import ElementModP, ElementModQ, int_to_p_unchecked, int_to_q_unchecked

    set_deserializer(
        lambda p_as_int, cls, **_: int_to_p_unchecked(p_as_int), ElementModP
    )
    set_validator(lambda p: p.is_in_bounds(), ElementModP)

    set_deserializer(
        lambda q_as_int, cls, **_: int_to_q_unchecked(q_as_int), ElementModQ
    )
    set_validator(lambda q: q.is_in_bounds(), ElementModQ)

    set_deserializer(
        lambda none, cls, **_: None
        if none == "None"
        else default_nonetype_deserializer(none),
        NoneType,
    )

    set_deserializer(lambda dt, cls, **_: datetime.fromisoformat(dt), datetime)

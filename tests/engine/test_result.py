import pytest

from prefect.engine.result import Result, NoResult
from prefect.engine.result_handlers import ResultHandler, JSONResultHandler


class TestInitialization:
    def test_noresult_inits_with_no_args(self):
        n = NoResult()

    def test_result_requires_value(self):
        with pytest.raises(TypeError) as exc:
            r = Result()
        assert "value" in str(exc.value)

    def test_result_inits_with_value(self):
        r = Result(3)
        assert r.value == 3

        s = Result(value=5)
        assert s.value == 5

    def test_result_inits_with_serialized_and_serializer(self):
        handler = ResultHandler()
        r = Result(value=3, serialized=False, serializer=handler)
        assert r.value == 3
        assert r.serialized is False
        assert r.serializer == handler

    def test_result_does_allow_serialized_false_without_serializer(self):
        r = Result(value=2, serialized=False)
        assert r.value == 2
        assert r.serialized is False

    def test_result_doesnt_allow_serialized_without_serializer(self):
        with pytest.raises(ValueError):
            r = Result(value=3, serialized=True)

    def test_result_assumes_nonserialized_at_init(self):
        r = Result(10)
        assert r.serialized is False
        assert r.serializer is None


@pytest.mark.parametrize("attr", ["value", "serialized", "serializer"])
def test_noresult_has_no_result_attrs(attr):
    n = NoResult()
    with pytest.raises(AttributeError):
        getattr(n, attr)


class TestSerialization:
    def test_serialize_serializes(self):
        r = Result(value=4, serializer=JSONResultHandler())
        assert r.serialized is False
        s = r.serialize()
        assert s.serialized is True
        assert s.value == "4"
        assert s.serializer is r.serializer

    def test_serialize_doesnt_serialize(self):
        r = Result(value=4, serialized=True, serializer=JSONResultHandler())
        assert r.serialized is True
        s = r.serialize()
        assert s is r

    def test_serialize_deserializes(self):
        r = Result(value="4", serialized=True, serializer=JSONResultHandler())
        assert r.serialized is True
        s = r.deserialize()
        assert s.serialized is False
        assert s.value == 4
        assert s.serializer is r.serializer

    def test_serialize_doesnt_deserialize(self):
        r = Result(value="4", serialized=False, serializer=JSONResultHandler())
        assert r.serialized is False
        s = r.deserialize()
        assert s is r

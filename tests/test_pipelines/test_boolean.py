import pytest

from kim.field import FieldInvalid, Boolean
from kim.pipelines.boolean import is_allowed_value


def test_is_allowed_value():

    field = Boolean(name='test')

    with pytest.raises(FieldInvalid):
        is_allowed_value(field, 'test')

    assert is_allowed_value(field, True) is True
    assert is_allowed_value(field, 'true') == 'true'
    assert is_allowed_value(field, '1') == '1'
    assert is_allowed_value(field, 'True') == 'True'
    assert is_allowed_value(field, False) is False
    assert is_allowed_value(field, 'false') == 'false'
    assert is_allowed_value(field, '0') == '0'
    assert is_allowed_value(field, 0) == 0
    assert is_allowed_value(field, 'False') == 'False'


def test_is_allowed_value_with_custom_values():

    field = Boolean(name='test', true_boolean_values=['foo'],
                    false_boolean_values=['bar'])

    with pytest.raises(FieldInvalid):
        is_allowed_value(field, True)
    with pytest.raises(FieldInvalid):
        is_allowed_value(field, False)

    assert is_allowed_value(field, 'foo') == 'foo'
    assert is_allowed_value(field, 'bar') == 'bar'


def test_boolean_input():

    field = Boolean(name='is_active', required=True)

    output = {}
    field.marshal({'is_active': False, 'email': 'mike@mike.com'}, output)
    assert output == {'is_active': False}

    field.marshal({'is_active': 'false', 'email': 'mike@mike.com'}, output)
    assert output == {'is_active': False}

    field.marshal({'is_active': True, 'email': 'mike@mike.com'}, output)
    assert output == {'is_active': True}

    field.marshal({'is_active': 'true', 'email': 'mike@mike.com'}, output)
    assert output == {'is_active': True}


def test_boolean_input_with_allow_none():

    field = Boolean(name='is_active', required=False, allow_none=True)

    output = {}
    field.marshal({'is_active': None, 'email': 'mike@mike.com'}, output)
    assert output == {'is_active': None}


def test_boolean_output():

    class Foo(object):
        is_active = True

    field = Boolean(name='is_active', required=True)

    output = {}
    field.serialize(Foo(), output)
    assert output == {'is_active': True}

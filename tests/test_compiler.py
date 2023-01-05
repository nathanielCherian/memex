import pytest

from memex.compiler import Compiler
from memex.errors import InvalidQueryException


def test_id_basic():
    compiler = Compiler("id=100")
    assert compiler.to_sql() == "(id = 100)"
    assert compiler.rebuild_query() == "id=100"


def test_keywords_basic():
    compiler = Compiler("keywords='.test\d+'")
    assert compiler.to_sql() == "(keywords regexp '.test\d+')"
    assert compiler.rebuild_query() == "keywords='.test\d+'"


def test_url_basic():
    compiler = Compiler("url = '.test(\d+)'")
    assert compiler.to_sql() == "(url regexp '.test(\d+)')"
    assert compiler.rebuild_query() == "url = '.test(\d+)'"


def test_id_operators():
    compiler = Compiler("id<100")
    assert compiler.to_sql() == "(id < 100)"
    assert compiler.rebuild_query() == "id<100"

    compiler = Compiler("id>100")
    assert compiler.to_sql() == "(id > 100)"
    assert compiler.rebuild_query() == "id>100"

    compiler = Compiler("id<=100")
    assert compiler.to_sql() == "(id <= 100)"
    assert compiler.rebuild_query() == "id<=100"

    compiler = Compiler("id>=100")
    assert compiler.to_sql() == "(id >= 100)"
    assert compiler.rebuild_query() == "id>=100"

    compiler = Compiler("id!=100")
    assert compiler.to_sql() == "(id != 100)"
    assert compiler.rebuild_query() == "id!=100"


def test_chaining():
    compiler = Compiler("id>=100&&url='.tory.'||keywords='.test.'")
    assert (
        compiler.to_sql()
        == "((id >= 100) AND ((url regexp '.tory.') OR (keywords regexp '.test.')))"
    )
    assert compiler.rebuild_query() == "(id>=100&&(url='.tory.'||keywords='.test.'))"


def test_parentheticals():
    compiler = Compiler("(id>=100&&url='.tory.')||keywords='.test.'")
    assert (
        compiler.to_sql()
        == "(((id >= 100) AND (url regexp '.tory.')) OR (keywords regexp '.test.'))"
    )
    assert compiler.rebuild_query() == "((id>=100&&url='.tory.')||keywords='.test.')"


def test_nested():
    compiler = Compiler("id>=100&&(url='.tory.'||(keywords='.test.'&&id<200))")
    assert (
        compiler.to_sql()
        == "((id >= 100) AND ((url regexp '.tory.') OR ((keywords regexp '.test.') AND (id < 200))))"
    )
    assert (
        compiler.rebuild_query()
        == "(id>=100&&(url='.tory.'||(keywords='.test.'&&id<200)))"
    )


def test_unknown_operator():
    with pytest.raises(InvalidQueryException):
        compiler = Compiler("id ?? 5")


def test_mismatched_datatypes():
    with pytest.raises(InvalidQueryException):
        compiler = Compiler("id = wrong")

from frosted import messages as m
from frosted.api import _noqa_lines, _re_noqa, check
from frosted.reporter import Reporter

from .utils import flakes


def test_regex():
    # simple format
    assert _re_noqa.search('#noqa')
    assert _re_noqa.search('# noqa')
    # simple format is strict, must be at start of comment
    assert not _re_noqa.search('# foo noqa')

    # verbose format (not strict like simple format)
    assert _re_noqa.search('#frosted:noqa')
    assert _re_noqa.search('# frosted: noqa')
    assert _re_noqa.search('# foo frosted: noqa')


def test_checker_ignore_lines():
    # ignore same line
    flakes('from fu import *', ignore_lines=[1])
    # don't ignore different line
    flakes('from fu import *', m.ImportStarUsed, ignore_lines=[2])


def test_noqa_lines():
    assert _noqa_lines('from fu import bar; bar') == []
    assert _noqa_lines('from fu import * # noqa; bar') == [1]
    assert _noqa_lines('from fu import * #noqa\nbar\nfoo # frosted: noqa') == [1, 3]


def test_check_integration():
    """ make sure all the above logic comes together correctly in the check() function """
    reporter = Reporter(ListWriter(), ListWriter())

    result = check('from fu import *', 'test', reporter)

    # errors reported
    assert result == 1
    assert reporter._stdout.pop(0) == "test:1: 'from fu import *' used;"

    # same test, but with ignore set
    reporter = Reporter(ListWriter(), ListWriter())

    result = check('from fu import * # noqa', 'test', reporter)

    # errors reported
    assert result == 0
    assert len(reporter._stdout) == 0

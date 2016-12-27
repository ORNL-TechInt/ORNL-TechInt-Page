import mkhtml
import pytest


# -----------------------------------------------------------------------------
def test_init_err():
    """
    Running Assembler.__init__() with an invalid input name should throw an
    exception
    """
    with pytest.raises(StandardError) as err:
        a = mkhtml.Assembler('foo.txt', ext='bar')
    assert "I don't know what to do with foo.txt" in str(err)


# -----------------------------------------------------------------------------
def test_init_ok():
    """
    Running Assembler.__init__() with a valid input name should set up the
    object correctly
    """
    a = mkhtml.Assembler('foo.src', ext='bar')
    assert a.iname == 'foo.src'
    assert a.oname == 'foo.bar'
    assert a.instack == []
    assert a.ifstack == []


# -----------------------------------------------------------------------------
def test_output_name_defext():
    """
    Assembler.output_name() should return <stem>.html is ext is not specified
    or empty
    """
    a = mkhtml.Assembler('foo.src')
    assert a.oname == 'foo.html'
    assert a.output_name('fiddle.src', ext='') == 'fiddle.html'


# -----------------------------------------------------------------------------
def test_output_name_nodot():
    """
    Assembler.output_name() should add dot to ext if necessary
    """
    a = mkhtml.Assembler('foo.src', 'nodot')
    assert a.oname == 'foo.nodot'
    assert a.output_name('fiddle.src', ext='nodot') == 'fiddle.nodot'


# -----------------------------------------------------------------------------
def test_output_name_explicit():
    """
    Assembler.output_name() should add dot to ext if necessary
    """
    a = mkhtml.Assembler('foo.src', '.exp')
    assert a.oname == 'foo.exp'
    assert a.output_name('fiddle.src', ext='exp') == 'fiddle.exp'

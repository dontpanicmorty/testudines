import pytest

from solution import unpinned


@pytest.mark.parametrize(
    "text, expected",
    [
        ("pandas==2.2.3\n", []),
        ("pandas>=2.0\n", ["pandas"]),
        ("pandas\n", ["pandas"]),
        ("Pandas~=2.0\nrequests==2.32\n", ["pandas"]),
        ("# only a comment\n\n   \n", []),
        ("-r base.txt\n--index-url my-index\nduckdb==1.0\n", []),
        ("httpx[http2]~=0.27\n", ["httpx"]),
        ("httpx[http2]==0.27.0\n", []),
        ("requests==2.32.3  # pinned\nflask<3  # old\n", ["flask"]),
        ('numpy>=1.26 ; python_version < "3.13"\n', ["numpy"]),
        ('numpy==1.26.4 ; python_version < "3.13"\n', []),
        ("zeta\nalpha>1\nMid<2\n", ["alpha", "mid", "zeta"]),
        ("pandas>=2\npandas>=2.1\n", ["pandas"]),
    ],
)
def test_unpinned(text, expected):
    assert unpinned(text) == expected

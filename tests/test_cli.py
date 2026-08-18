"""Tests for the command line front end."""

from wordcount.cli import main


def test_cli_reads_a_file(tmp_path, capsys):
    target = tmp_path / "sample.txt"
    target.write_text("alpha beta alpha", encoding="utf-8")
    assert main([str(target), "--top", "1"]) == 0
    out = capsys.readouterr().out
    assert "total words   3" in out
    assert "alpha" in out

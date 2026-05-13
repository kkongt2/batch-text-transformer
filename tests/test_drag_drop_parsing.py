import importlib.util
import pathlib
import tkinter as tk
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "batch-text-transformer.py"
spec = importlib.util.spec_from_file_location("batch_text_transformer", MODULE_PATH)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class DummyMaster:
    def __init__(self):
        self.tk = tk.Tcl()


class DragDropParsingTest(unittest.TestCase):
    def setUp(self):
        self.gui = app.WordReplacerGUI.__new__(app.WordReplacerGUI)
        self.gui.master = DummyMaster()

    def test_parses_caja_text_uri_list(self):
        payload = "file:///home/me/a%20file.txt\r\nfile:///home/me/second.txt\r\n"
        self.assertEqual(
            [app.WordReplacerGUI._normalize_file_path(p) for p in self.gui._parse_dropped_files(payload)],
            ["/home/me/a file.txt", "/home/me/second.txt"],
        )

    def test_ignores_gnome_copy_action_lines(self):
        payload = "copy\nfile:///home/me/a.txt\n# comment\nfile:///home/me/b.txt\n"
        self.assertEqual(
            [app.WordReplacerGUI._normalize_file_path(p) for p in self.gui._parse_dropped_files(payload)],
            ["/home/me/a.txt", "/home/me/b.txt"],
        )

    def test_preserves_tk_dnd_files_with_spaces(self):
        payload = "{/home/me/a file.txt} {/home/me/b file.txt}"
        self.assertEqual(
            self.gui._parse_dropped_files(payload),
            ["/home/me/a file.txt", "/home/me/b file.txt"],
        )


if __name__ == "__main__":
    unittest.main()

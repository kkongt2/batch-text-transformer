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

    def test_ignores_gnome_icon_coordinate_lines(self):
        payload = "file:///home/me/a.txt\r\n10:20:30:40\r\nfile:///home/me/b.txt\r\n"
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

    def test_file_drop_action_prefers_event_action(self):
        event = type("DropEvent", (), {"action": "move", "actions": ("copy", "move")})()

        self.assertEqual(app.WordReplacerGUI._file_drop_action(event), "move")

    def test_file_drop_action_uses_supported_fallback(self):
        event = type("DropEvent", (), {"action": "refuse_drop", "actions": ("link", "copy")})()

        self.assertEqual(app.WordReplacerGUI._file_drop_action(event), "copy")

    def test_drop_callback_returns_negotiated_action(self):
        calls = []
        self.gui._add_files = lambda paths, source: calls.append((paths, source))
        self.gui.update_src_list = lambda: calls.append("updated")
        event = type("DropEvent", (), {"data": "file:///home/me/a.txt", "action": "move"})()

        self.assertEqual(self.gui.on_files_dropped(event), "move")
        self.assertEqual(calls, [(["file:///home/me/a.txt"], "Drop Files"), "updated"])


if __name__ == "__main__":
    unittest.main()

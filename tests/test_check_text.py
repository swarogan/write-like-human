import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import check_text  # noqa: E402


def run(text):
    return check_text.check(text, "t")


class CharacterTests(unittest.TestCase):
    def test_plain_ascii_is_clean(self):
        errors, warnings = run("We shipped it on Friday. It works, mostly.\n")
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_em_dash_is_error_and_not_auto_fixed(self):
        text = "It works — mostly."
        errors, _ = run(text)
        self.assertEqual(len(errors), 1)
        self.assertIn("rewrite", errors[0])
        self.assertIn("—", check_text.apply_fixes(text))

    def test_error_reports_line_and_column(self):
        errors, _ = run("ok\nab…\n")
        self.assertTrue(errors[0].startswith("t:2:3:"))

    def test_safe_fixes(self):
        text = "“Hi”, it’s 5 min… • a → b​"
        self.assertEqual(check_text.apply_fixes(text), "\"Hi\", it's 5 min... - a -> b")

    def test_emoji_is_error(self):
        errors, _ = run("Launched today \U0001F680")
        self.assertEqual(len(errors), 1)

    def test_accented_letter_is_only_a_warning(self):
        errors, warnings = run("Thanks, Zoë.")
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)


class PhraseTests(unittest.TestCase):
    def assertFlags(self, text):
        self.assertTrue(run(text)[1], "expected a warning for: %r" % text)

    def assertClean(self, text):
        self.assertEqual(run(text)[1], [], "unexpected warning for: %r" % text)

    def test_stock_phrases(self):
        self.assertFlags("Let's delve into the details.")
        self.assertFlags("Excited to share our new tool.")
        self.assertFlags("It's not just a tool, it's a workflow.")
        self.assertFlags("Start with integration tests. Here is why.")
        self.assertFlags("**Sound.** It is quiet.")

    def test_curly_apostrophe_does_not_hide_phrase(self):
        self.assertFlags("It’s not just a tool, it’s a workflow.")

    def test_word_boundaries(self):
        # "robustness" contains a stock word, and "Here is the" is not a staged reveal.
        self.assertClean("We measured robustness under load.")
        self.assertClean("Here is the config file we use.")

    def test_semicolon_in_prose_flagged(self):
        self.assertFlags("The build is fast; the tests are not.")

    def test_semicolon_in_code_ignored(self):
        self.assertClean("Run `a; b` first.")
        self.assertClean("```\nint x = 1;\n```")
        self.assertClean("    let y = 2;")


class ExitCodeTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        fd, self.path = tempfile.mkstemp(suffix=".md")
        os.close(fd)

    def tearDown(self):
        os.remove(self.path)

    def write(self, text):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(text)

    def test_warnings_pass_unless_strict(self):
        self.write("Let's delve in.")
        self.assertEqual(check_text.main(["--quiet", self.path]), 0)
        self.assertEqual(check_text.main(["--quiet", "--strict", self.path]), 1)

    def test_fix_rewrites_file_but_dash_still_fails(self):
        self.write("“Done” — finally.")
        self.assertEqual(check_text.main(["--quiet", "--fix", self.path]), 1)
        with open(self.path, encoding="utf-8") as f:
            self.assertEqual(f.read(), "\"Done\" — finally.")


if __name__ == "__main__":
    unittest.main()

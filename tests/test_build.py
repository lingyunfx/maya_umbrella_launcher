import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from maya_umbrella_launcher import build


class BuildTests(unittest.TestCase):
    def test_explicit_compiler_path(self):
        with tempfile.TemporaryDirectory() as folder:
            compiler = Path(folder) / "ISCC.exe"
            compiler.touch()
            with patch.dict(os.environ, {"ISCC": str(compiler)}):
                self.assertEqual(build.find_iscc(), str(compiler))

    def test_compile_before_installer_and_fail_fast(self):
        import subprocess
        with patch.object(build, "find_iscc", return_value="ISCC.exe"), \
             patch.object(build.subprocess, "run") as run:
            build.main()
            self.assertEqual(run.call_count, 3)
            self.assertIn("--windows-console-mode=disable", run.call_args_list[0].args[0])
            self.assertIn("--windows-console-mode=force", run.call_args_list[1].args[0])
            self.assertEqual(run.call_args_list[2].args[0][0], "ISCC.exe")
            run.reset_mock()
            run.side_effect = subprocess.CalledProcessError(1, "nuitka")
            with self.assertRaises(subprocess.CalledProcessError):
                build.main()
            self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()

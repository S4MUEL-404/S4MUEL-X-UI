"""Exercise only the update functions; never execute the installer or touch system paths."""
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
SCRIPT = (ROOT / 'install.sh').read_text()
BLOCK = SCRIPT.split('# BEGIN S4MUEL RELIABLE UPDATE\n', 1)[1].split('# END S4MUEL RELIABLE UPDATE', 1)[0]


class UpdateTests(unittest.TestCase):
    def run_case(self, payload, setup='', action='s4_update_script "$target" "$version" "$backups"', mock=''):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            target = root / 'x-ui'
            target.write_text('#!/bin/bash\necho old\n')
            target.chmod(0o755)
            (root / 'version').write_text('v1.0.0-s4\n')
            (root / 'payload').write_text(payload)
            shell = BLOCK + r'''
red() { echo "$*"; }
yellow() { echo "$*"; }
green() { echo "$*"; }
root="$1"
target="$root/x-ui"
version="$root/version"
backups="$root/backups"
curl() {
    while [[ $# -gt 0 ]]; do
        if [[ "$1" == '-o' ]]; then cp "$root/payload" "$2"; return; fi
        shift
    done
    return 1
}
''' + mock + '\n' + setup + '\n' + action
            result = subprocess.run(['bash', '-c', shell, 'test', tmp], capture_output=True, text=True, errors='replace')
            copies = list(root.glob('backups/script.*/install.sh'))
            return result, target.read_text(), (root / 'version').read_text(), [p.read_text() for p in copies], list(root.glob('x-ui.new.*'))

    candidate = "#!/bin/bash\nS4_SCRIPT_VERSION='v1.1.0-s4'\necho new\n"

    def test_success_backs_up_and_installs(self):
        result, script, version, backups, temporary = self.run_case(self.candidate)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(script, self.candidate)
        self.assertEqual(version, 'v1.1.0-s4\n')
        self.assertEqual(backups, ['#!/bin/bash\necho old\n'])
        self.assertEqual(temporary, [])

    def assert_preserved(self, **kwargs):
        result, script, version, _, temporary = self.run_case(**kwargs)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(script, '#!/bin/bash\necho old\n')
        self.assertEqual(version, 'v1.0.0-s4\n')
        self.assertEqual(temporary, [])

    def test_partial_download_failure(self):
        self.assert_preserved(payload=self.candidate, mock='curl() { while [[ $# -gt 0 ]]; do if [[ "$1" == -o ]]; then printf partial > "$2"; return 22; fi; shift; done; return 22; }')

    def test_empty_response(self):
        self.assert_preserved(payload='')

    def test_html_response(self):
        self.assert_preserved(payload='<html>Service unavailable</html>')

    def test_shell_syntax_failure(self):
        self.assert_preserved(payload=self.candidate + 'if then\n')

    def test_missing_version(self):
        self.assert_preserved(payload='#!/bin/bash\necho new\n')

    def test_backup_failure(self):
        self.assert_preserved(payload=self.candidate, setup='printf blocked > "$backups"')

    def test_replace_failure(self):
        self.assert_preserved(payload=self.candidate, mock='mv() { return 1; }')

    def test_restore(self):
        result, script, version, _, _ = self.run_case(self.candidate, action='''
s4_update_script "$target" "$version" "$backups" || exit 1
for backup in "$backups"/script.*; do
    s4_restore_script "$backup" "$target" "$version" || exit 1
done
''')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(script, '#!/bin/bash\necho old\n')
        self.assertEqual(version, 'v1.0.0-s4\n')

    def test_invalid_restore_preserves_script(self):
        self.assert_preserved(payload=self.candidate, action='s4_restore_script "$root/missing" "$target" "$version"')


if __name__ == '__main__':
    unittest.main(verbosity=2)

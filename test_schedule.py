from pathlib import Path
import os, subprocess, tempfile, unittest
s=(Path(__file__).resolve().parent/'install.sh').read_text()
block=s.split('# BEGIN S4MUEL SERVICE SCHEDULE\n')[1].split('# END S4MUEL SERVICE SCHEDULE')[0]
class ScheduleTests(unittest.TestCase):
 def run_case(self, content, release='Debian', failure=False):
  with tempfile.TemporaryDirectory() as d:
   cron=Path(d)/'cron';cron.write_text(content)
   shell=block+'''
crontab(){
 if [[ "$1" == -l ]]; then
  if [[ "$failure" == yes ]]; then echo 'permission denied' >&2; return 1; fi
  cat "$cron"
 else cat "$1" > "$cron"; fi
}
cronxui
result=$?
cat "$cron"
exit "$result"
'''
   return subprocess.run(['bash','-c',shell],env={**os.environ,'cron':str(cron),'release':release,'failure':'yes' if failure else 'no'},capture_output=True,text=True)
 def test_removes_owned_jobs_only(self):
  keep='15 3 * * * systemctl restart x-ui\n0 2 * * * /custom/backup\n'
  r=self.run_case('0 2 * * * systemctl restart x-ui\n* * * * * /usr/local/x-ui/goxui.sh\n'+keep)
  self.assertEqual(r.returncode,0);self.assertEqual(r.stdout,keep)
 def test_idempotent(self):
  text='0 1 * * * /custom/backup\n'
  self.assertEqual(self.run_case(text).stdout,text)
 def test_read_failure_does_not_write(self):
  r=self.run_case('keep\n',failure=True)
  self.assertNotEqual(r.returncode,0);self.assertEqual(r.stdout,'keep\n')
 def test_openrc_watchdog_once(self):
  r=self.run_case('* * * * * /usr/local/x-ui/goxui.sh\n','alpine')
  self.assertEqual(r.stdout,'* * * * * /usr/local/x-ui/goxui.sh\n')
 def test_systemd_watchdog_never_restarts(self):
  watchdog=block.split("<<-'EOF'\n")[1].split('\nEOF')[0]
  r=subprocess.run(['bash','-c','systemctl(){ echo unexpected; return 1; };\n'+watchdog],capture_output=True,text=True)
  self.assertEqual(r.returncode,0);self.assertEqual(r.stdout,'')
if __name__=='__main__': unittest.main(verbosity=2)

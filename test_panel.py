from pathlib import Path
import subprocess, unittest
s=(Path(__file__).resolve().parent / 'install.sh').read_text()
block=s[s.index('s4_panel_scheme() {'):s.index('resinstall(){')]
class PanelTests(unittest.TestCase):
 def run_case(self,mode,expected,cert=''):
  shell=block.replace('/usr/local/x-ui/x-ui setting -show',"printf 'user: test\\npassword: test\\nport: 18443\\npath: /test-panel/\\n'")+'''
red(){ echo "$*"; }
sleep(){ :; }
curl(){
 case "$*" in
  *https://*) [[ "$mode" == https ]] || return 35 ;;
  *http://*) [[ "$mode" == http ]] || return 7 ;;
 esac
 printf '%s' "$response"
}
s4_verify_panel
'''
  r=subprocess.run(['bash','-c',shell],env={'PATH':'/usr/bin:/bin','mode':mode,'response':expected,'cert':cert},capture_output=True,text=True)
  return r.returncode
 def test_https_ready(self): self.assertEqual(self.run_case('https','200','y'),0)
 def test_http_ready(self): self.assertEqual(self.run_case('http','200'),0)
 def test_https_requested_but_http_running(self): self.assertNotEqual(self.run_case('http','200','y'),0)
 def test_no_listener(self): self.assertNotEqual(self.run_case('none','000'),0)
 def test_wrong_path(self): self.assertNotEqual(self.run_case('https','404','y'),0)
if __name__=='__main__': unittest.main(verbosity=2)

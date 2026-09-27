import json,tempfile,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
import app

class TeamPersistence(unittest.TestCase):
    def test_email_roundtrip_and_read_only_host(self):
        data={'team':'Test','members':[{'name':'Test Member','role':'Captain','email':'member@example.com','portfolio':''}]}
        with tempfile.TemporaryDirectory() as temp,patch.object(app,'DATA',Path(temp)),patch.dict('os.environ',{'YUKSAVA_READ_ONLY_SETTINGS':'0'}):
            with TestClient(app.app) as client:
                self.assertEqual(client.put('/api/project',json=data).status_code,200)
                self.assertEqual(client.get('/api/project').json()['members'],data['members'])
                self.assertEqual(json.loads((Path(temp)/'project.json').read_text())['members'],data['members'])
                data['members'][0]['email']='invalid email'
                self.assertEqual(client.put('/api/project',json=data).status_code,422)
                with patch.dict('os.environ',{'YUKSAVA_READ_ONLY_SETTINGS':'1'}):
                    self.assertEqual(client.put('/api/project',json=data).status_code,403)

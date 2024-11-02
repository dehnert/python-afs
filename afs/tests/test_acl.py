import unittest
import afs.acl as acl

class ACLTestCase(unittest.TestCase):
    def test_showRights(self):
        assert acl.showRights(acl.READ | acl.WRITE) == "rw"

    def test_readRights(self):
        assert acl.readRights('read') & acl.READ
        assert acl.readRights('read') & acl.LOOKUP
        assert not acl.readRights('read') & acl.WRITE

    def test_retrieve(self):
        assert acl.ACL.retrieve('/afs/athena.mit.edu/contrib/bitbucket2').pos['system:anyuser'] & acl.WRITE
        assert acl.ACL.retrieve('/afs/athena.mit.edu/astaff/project/macathena/.python-afs-test').neg['mrittenb'] & acl.USR0

    def test_getCallerAccess(self):
        assert acl.getCallerAccess('/afs/athena.mit.edu/contrib/bitbucket2') & acl.WRITE

if __name__ == '__main__':
    unittest.main()

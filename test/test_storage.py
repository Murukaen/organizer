import unittest
import subprocess

class TestStorage(unittest.TestCase):

    db_name = 'test_001.db' # TODO Update name, consider using random name

    def setUp(self) -> None:
        subprocess.run(['caribou', 'upgrade', self.db_name, 'migrations'])

    def tearDown(self) -> None:
        subprocess.run(['rm', self.db_name]);
    
    def test_dummy(self):
        self.assertTrue(True)
    
    def test_read_after_update_should_work(self):
        # TODO
        pass

if __name__ == '__main__':
    unittest.main()
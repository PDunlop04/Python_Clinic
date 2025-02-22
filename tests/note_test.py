import unittest
from datetime import datetime
from clinic.note import Note
from clinic.controller import Controller

class NoteTest(unittest.TestCase):
    def setUp(self):
        self.note = Note(code=1, details = "initial consultation")
        self.controller = Controller()
        self.controller.login("user", "clinic2024") 

    def test_note_initialization(self):
        """Test that Note object is initialized with correct values."""
        self.assertEqual(self.note.code, 1)
        self.assertEqual(self.note.details, "initial consultation")
        self.assertIsInstance(self.note.timestamp, datetime)
    
    def test_note_equality(self):
        note2 = Note(code = 1, details = "initial consultation")
        self.assertEqual(self.note, note2)

        note3 = Note(code =2, details = "follow-up consultation")
        self.assertNotEqual(self.note, note3)
    def test_edge_case(self):
        self.assertFalse(self.controller.update_note(999, "This note does not e>
                     "should not be able to update a note that does not exist")
        self.controller.logout()
        self.assertFalse(self.controller.update_note(3, "Attempt to update afte>
                     "should not be able to update notes after logging out")
        self.assertFalse(self.controller.update_note(3, ""),
                     "should not allow updating a note with an empty string")

    def test_note_string_representation(self):
        expected_string = f"Code: {self.note.code}, Details: {self.note.details>
        self.assertEqual(str(self.note), expected_string)

if __name__ == '__main__':
    unittest.main()





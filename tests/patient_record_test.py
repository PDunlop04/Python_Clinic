import unittest
from unittest import TestCase, main
from clinic.patient_record import *
from clinic.note import Note
from clinic.controller import Controller

class PatientRecordTest(TestCase):
    def setUp(self):
        self.record = PatientRecord()
        self.note1 = Note(code = 1, details = "Initial consultation")
        self.note2 = Note(code = 2, details = "Follow-up consultation")
        self.record.add_note(self.note1)
        self.record.add_note(self.note2)

    def test_add_note(self):
        self.assertEqual(len(self.record.notes), 2)  # Check two notes are added
    def test_delete_note_by_code(self):
        self.assertTrue(self.record.delete_note_by_code(1))  # Should return Tr>
        self.assertEqual(len(self.record.notes), 1)  # One note should be left
        self.assertFalse(self.record.delete_note_by_code(1))  # Should return F>

    def test_list_notes(self):
        self.assertEqual(self.record.list_notes(), [self.note2, self.note1])  #>

    def test_retrieve_notes(self):
        self.assertEqual(self.record.retrieve_notes("Initial"), [self.note1])  >
        self.assertEqual(self.record.retrieve_notes("Nonexistent"), [])  # Shou>

if __name__ == '__main__':
    unittest.main()


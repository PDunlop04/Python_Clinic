from clinic.dao.note_dao_pickle import NoteDAOPickle


class PatientRecord():
	''' class that represents a patient's medical record '''

	def __init__(self, phn, autosave = False):
		''' construct a patient record '''
		self.phn = phn
		self.notes_dao = NoteDAOPickle(phn, autosave=autosave) 

	def search_note(self, code):
		''' search a note in the patient's record '''
		return self.notes_dao.search_note(code)

	def create_note(self, text):
		''' create a note in the patient's record '''
		return self.notes_dao.create_note(text)
	
	def retrieve_notes(self, search_string):
		''' retrieve notes in the patient's record that satisfy a search string '''
		return self.notes_dao.retrieve_notes(search_string)

	def update_note(self, code, new_text):
		''' update a note from the patient's record '''
		return self.notes_dao.update_note(code, new_text)


	def delete_note(self, code):
		''' delete a note from the patient's record '''
		return self.notes_dao.delete_note(code)

	def list_notes(self):
		''' list all notes from the patient's record from the 
			more recently added to the least recently added'''
		return self.notes_dao.list_notes()
	
	@staticmethod
	def from_dict(data: dict, autosave: bool = False) -> 'PatientRecord':
		''' Convert a dictionary back to a PatientRecord object '''
		# Pass the phn and autosave argument to create a PatientRecord
		return PatientRecord(data['phn'], autosave=autosave)

	def to_dict(self) -> dict:
		''' Convert a PatientRecord object to a dictionary for serialization '''
		return {'phn': self.phn}  # Include the PHN
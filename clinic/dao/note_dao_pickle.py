from clinic.dao.note_dao import NoteDAO
from clinic.note import Note
from datetime import datetime

import os
import pickle

class NoteDAOPickle(NoteDAO):
	def __init__(self, phn, autosave = False):
		self.phn = phn 
		self.autosave = autosave

		# Fix the data directory to be inside the clinic directory, using the PHN
		# This line constructs the path to a folder named records
		self.data_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'records')
		self.counter = 1
		self.notes: dict = {}
		self.initialize()
	
	def initialize(self):
		self.load_data()

	def load_data(self):
		''' Load notes from patient record files if autosave is enabled '''
		if not os.path.exists(self.data_directory):
			os.makedirs(self.data_directory) # creates directory if doesnt exist

		# Load each patient's notes from the records directory
		notes_file_path = os.path.join(self.data_directory, f"{self.phn}.dat")
		if os.path.exists(notes_file_path):
			self.load_patient_notes(notes_file_path)
	
	def load_patient_notes(self, notes_file_path):
		''' Load notes for a specific patient from their .dat file '''
		try:
			with open(notes_file_path, 'rb') as file:
				patient_notes = pickle.load(file)
				self.notes[self.phn] = [
					Note(note['code'], note['text'], note['timestamp']) if isinstance(note, dict) else note
					for note in patient_notes
				]
				
				# Set the counter to the max note code + 1
				self.counter = max((note.code for note in self.notes[self.phn]), default=0) + 1
		except Exception as e:
			raise Exception(f"Error loading notes for patient {self.phn}: {e}")


	def search_note(self, code):
		''' search for a note by code '''
		for note in self.notes.get(self.phn, []):
			if note.code == code:
				return note
		return None

	def create_note(self, note_text):
		''' Create a new note for a patient '''
		note_code = self.counter
		self.counter += 1  # Increment after assigning the code to preserve the correct code
		# have to deal with the timestamp now because it is no longer a given input, must read from string
		note_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		note = Note(note_code, note_text, note_timestamp)
		
		if self.phn not in self.notes:
			self.notes[self.phn] = []
		
		self.notes[self.phn].append(note)
		
		if self.autosave:
			self.autosave_note_to_file()
		
		return note
	
	def autosave_note_to_file(self):
		''' Save patient notes to file (autosave functionality) '''
		notes_file_path = os.path.join(self.data_directory, f"{self.phn}.dat")
		try:
			with open(notes_file_path, 'wb') as file:
				patient_notes_data = [note.__dict__ for note in self.notes[self.phn]]
				pickle.dump(patient_notes_data, file)
		except Exception as e:
			raise Exception(f"Error saving notes for patient {self.phn}: {e}")


	def retrieve_notes(self, search_string):
		''' retrieve notes that contain the search string '''
		return [
            note for note in self.notes.get(self.phn, [])
            if search_string.lower() in note.text.lower()
        ]
		#return [note for note in self.notes.values() if search_string in note.text]
		#this is not to 1 specific value's

	def update_note(self, code, new_text):
		''' Update an existing note by its code '''
		for note in self.notes.get(self.phn, []):
			if note.code == code:
				note.text = new_text
				if self.autosave:
					self.autosave_note_to_file()
				return True
		return False

	def delete_note(self, code):
		''' delete a note '''
		for note in self.notes.get(self.phn, []):
			if note.code == code:
				self.notes[self.phn].remove(note)
				if self.autosave:
					self.autosave_note_to_file()
				return True
		return False

	def list_notes(self):
		''' list all notes in reverse order '''
		return list(reversed(self.notes.get(self.phn, [])))
		#return list(self.notes.values())[::-1]
		# commented out one returns all patients notes not specific one

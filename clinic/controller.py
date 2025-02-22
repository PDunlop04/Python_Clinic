from clinic.patient import Patient
from clinic.patient_record import PatientRecord
from clinic.note import Note

from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.dao.note_dao_pickle import NoteDAOPickle

import os
import hashlib


class Controller():
	''' controller class that receives the system's operations '''

	def __init__(self, autosave = False):
		''' construct a controller class '''
		self.users = {"user" : "123456", "ali": "@G00dPassw0rd"}
		self.username = None
		self.password = None
		self.logged = False
		self.current_patient = None
		
		self.autosave = autosave

		self.patients_dao = PatientDAOJSON(autosave=self.autosave)  # Instantiate the PatientDAO class
		
		if self.autosave:
			self.load_users()  # Load users from the users.txt file
			self.patients_dao.load_data()  # Load patients from their respective file

	
	def load_users(self):
		''' Loads users and their password hashes from users.txt '''
		try:
			users_file_path = os.path.join(os.path.dirname(__file__), 'users.txt')
			with open(users_file_path, 'r') as file:
				for line in file:
					username, password_hash = line.strip().split(',')
					self.users[username] = password_hash
		except FileNotFoundError:
			raise Exception(f"User file '{users_file_path}' not found.")
		except Exception as e:
			raise Exception(f"Error reading users file: {e}")

	def login(self, username, password):
		''' user logs in the system '''
		if self.logged:
			raise DuplicateLoginException("User is already logged in.")
		if username not in self.users:
			raise InvalidLoginException("Invalid username or password.")
		if self.autosave:
			stored_password_hash = self.users[username]
			if not self.check_password_hash(password, stored_password_hash):
				raise InvalidLoginException("Invalid username or password.")
		else:
			stored_password = self.users[username]
			if password != stored_password:
				raise InvalidLoginException("Invalid username or password.")

		self.username = username
		self.password = password
		self.logged = True
		return True
	
	def check_password_hash(self, password, stored_password_hash):
		''' Safely checks the password against its hash '''
		entered_hash = hashlib.sha256(password.encode()).hexdigest() #from lab9
		return entered_hash == stored_password_hash



	def logout(self):
		''' user logs out from the system '''
		if not self.logged:
			raise InvalidLogoutException("User is not currently logged in.")
	
		self.username = None
		self.password = None
		self.logged = False
		self.current_patient = None
		return True

	def search_patient(self, phn):
		''' user searches a patient '''
		# must be logged in to do operation
		self._check_access()
		return self.patients_dao.search_patient(phn)


	def create_patient(self, phn, name, birth_date, phone, email, address):
		''' user creates a patient '''
		# must be logged in to do operation
		self._check_access()

		if self.patients_dao.search_patient(phn):
			raise IllegalOperationException("Patient with this PHN already exists.")

		# finally, create a new patient
		patient = Patient(phn, name, birth_date, phone, email, address)
		self.patients_dao.create_patient(patient)
		return patient

	def retrieve_patients(self, name):
		''' user retrieves the patients that satisfy a search criterion '''
		# must be logged in to do operation
		self._check_access()
		return self.patients_dao.retrieve_patients(name)

	def update_patient(self, original_phn, phn, name, birth_date, phone, email, address):
		''' user updates a patient '''
		# must be logged in to do operation
		self._check_access()

		# Ensure PHN update is not to an already registered PHN
		if original_phn != phn and self.patients_dao.search_patient(phn):
			raise IllegalOperationException("Cannot update patient with an already registered PHN.")

    	# Prevent updating the current patient
		if original_phn == self.current_patient.phn if self.current_patient else None:
			raise IllegalOperationException("Cannot update the current patient.")

		patient_to_update = self.patients_dao.search_patient(original_phn)
		if not patient_to_update:
			raise IllegalOperationException("Patient not found.")

		updated_patient = Patient(phn, name, birth_date, phone, email, address)
		updated = self.patients_dao.update_patient(original_phn, updated_patient)
		if not updated:
			raise IllegalOperationException("Failed to update patient.")
		return True
	######could have an error with my first if statement########
	def delete_patient(self, phn):
		''' user deletes a patient '''
		# must be logged in to do operation
		self._check_access()
		# Prevent deleting the current patient
		if self.current_patient is not None and phn == self.current_patient.phn:
			raise IllegalOperationException("Cannot delete the current patient.")

		if not self.patients_dao.search_patient(phn):
			raise IllegalOperationException("Patient not found.")

		self.patients_dao.delete_patient(phn)
		return True

	def list_patients(self):
		''' user lists all patients '''
		# must be logged in to do operation
		self._check_access()
		return self.patients_dao.list_patients()
		

	def set_current_patient(self, phn):
		''' user sets the current patient '''
		# must be logged in to do operation
		self._check_access()

		# first, search the patient by key
		patient = self.patients_dao.search_patient(phn)
		# patient does not exist
		if not patient:
			raise IllegalOperationException("Patient does not exist.")
		
		# patient exists, set them to be the current patient
		self.current_patient = patient
		return True


	def get_current_patient(self):
		''' get the current patient '''
		# must be logged in to do operation
		self._check_access()
		# return current patient
		return self.current_patient

	def unset_current_patient(self):
		''' unset the current patient '''

		# must be logged in to do operation
		self._check_access()
		# unset current patient
		self.current_patient = None
		return True

	def search_note(self, code):
		''' user searches a note from the current patient's record '''
		# there must be a valid current patient and logged in
		self._check_current_patient()
		# search a new note with the given code and return it 
		return self.current_patient.record.search_note(code)

	def create_note(self, text):
		''' user creates a note in the current patient's record '''
		
		# there must be a valid current patient and logged in
		self._check_current_patient()

		# create a new note and return it
		return self.current_patient.record.create_note(text)

	def retrieve_notes(self, search_string):
		''' user retrieves the notes from the current patient's record
			that satisfy a search string '''
		# there must be a valid current patient and logged in
		self._check_current_patient()

		# return the found notes
		return self.current_patient.record.retrieve_notes(search_string)

	def update_note(self, code, new_text):
		''' user updates a note from the current patient's record '''
		
		# there must be a valid current patient and logged in
		self._check_current_patient()

		# update note
		return self.current_patient.record.update_note(code, new_text)

	def delete_note(self, code):
		''' user deletes a note from the current patient's record '''

		# there must be a valid current patient and logged in
		self._check_current_patient()

		# delete note
		return self.current_patient.record.delete_note(code)

	def list_notes(self):
		''' user lists all notes from the current patient's record '''
		# there must be a valid current patient and logged in
		self._check_current_patient()

		return self.current_patient.record.list_notes()
	
	def _check_access(self):
		''' check if the user is logged in '''
		if not self.logged:
			raise IllegalAccessException("User must be logged in to perform this action.")

	def _check_current_patient(self):
		''' check if there is a current patient set '''
		self._check_access()

		if not self.current_patient:
			raise NoCurrentPatientException("No current patient set.")

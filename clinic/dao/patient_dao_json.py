from clinic.patient import Patient
from clinic.exception.illegal_operation_exception import IllegalOperationException

from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder
import os
import json


class PatientDAOJSON():
    ''' DAO for handling patient data in JSON format '''

    def __init__(self, autosave = False):
        ''' initialize an empty patient dictionary '''
        self.patients = {}
        self.autosave = autosave
        if self.autosave:
            self.load_data()
    def load_data(self):
        ''' Load patient data from a JSON file '''
        root_dir = os.path.dirname(os.path.abspath(__file__))
        patients_file_path = os.path.join(root_dir, '..', 'patients.json')
        patients_file_path = os.path.abspath(patients_file_path)

        if not os.path.exists(patients_file_path):
            with open(patients_file_path, 'w') as file:
                json.dump([], file)
            return

        try:
            with open(patients_file_path, 'r') as file:
                # Read content as a list of dictionaries, then manually decode each patient
                patients_data = json.load(file)
                # Pass autosave to PatientDecoder
                patient_decoder = PatientDecoder(autosave=self.autosave)
                for patient_data in patients_data:
                    patient = patient_decoder.decode(json.dumps(patient_data))
                    self.patients[patient.phn] = patient
        except FileNotFoundError:
            raise Exception(f"Patient data file '{patients_file_path}' not found.")
        except json.JSONDecodeError:
            raise Exception(f"Error decoding JSON from '{patients_file_path}'.")
        except Exception as e:
            raise Exception(f"Error loading patient data: {e}")
    
    def save_data(self):
        ''' Save patient data to a JSON file '''
        root_dir = os.path.dirname(os.path.abspath(__file__))
        # Explicitly set the path to the 'clinic' directory
        patients_file_path = os.path.join(root_dir, '..', 'patients.json')  # This points to the clinic directory

        # Ensure the path points to the right location
        patients_file_path = os.path.abspath(patients_file_path)

        try:
            with open(patients_file_path, 'w') as file:
                # Manually serialize Patient objects including PatientRecord
                serializable_patients = []
                for patient in self.patients.values():
                    patient_data = patient.__dict__.copy()  # Create a dictionary of Patient attributes
                    # Manually serialize PatientRecord 
                    if hasattr(patient.record, 'to_dict'):
                        patient_data['record'] = patient.record.to_dict()
                    serializable_patients.append(patient_data)
                # Write the serialized data to the file
                json.dump(serializable_patients, file, cls=PatientEncoder) #like in lab 9
        except Exception as e:
            raise Exception(f"Error saving patient data: {e}")

    def search_patient(self, phn):
        ''' search for a patient by PHN '''
        return self.patients.get(phn, None)

    def create_patient(self, patient):
        ''' create a new patient '''
        if patient.phn in self.patients:
            raise IllegalOperationException("Patient with this PHN already exists.")
        self.patients[patient.phn] = patient
        if self.autosave:
            self.save_data()  # Save after creating a patient
        return patient


    def retrieve_patients(self, name):
        ''' retrieve patients whose name matches the search string '''
        return [patient for patient in self.patients.values() if name.lower() in patient.name.lower()]

    def update_patient(self, phn, updated_patient):
        ''' update an existing patient '''
        # Check if the original PHN exists in the system
        if phn not in self.patients:
            raise IllegalOperationException(f"Patient with PHN {phn} not found.")

        # Delete the original patient entry using the old PHN
        del self.patients[phn]

        # Update the patient record in the dictionary
        self.patients[updated_patient.phn] = updated_patient

        if self.autosave:
            self.save_data()  # Save after updating a patient
        

        # If the code reaches here, the update succeeded
        return True
    
    def update_patient_data(self, phn, name, birth_date, phone, email, address):
        ''' Updates patient data based on PHN '''
        patient = self.patients.get(phn)
        if patient:
            updated_patient = Patient(phn, name, birth_date, phone, email, address)
            self.update_patient(phn, updated_patient)
        else:
            raise IllegalOperationException("Patient not found.")
    
    def delete_patient(self, phn):
        ''' delete a patient '''
        if phn not in self.patients:
            raise IllegalOperationException("Patient does not exist.")
        del self.patients[phn]
        if self.autosave:
            self.save_data()  # Save after deleting a patient
        return True
    
    def create_patient_from_data(self, phn, name, birth_date, phone, email, address):
        ''' Creates and returns a patient using the provided data '''
        patient = Patient(phn, name, birth_date, phone, email, address)
        return self.create_patient(patient)
    
    def retrieve_patients_by_name(self, name):
        ''' Retrieves patients that match the name '''
        return [patient for patient in self.patients.values() if name.lower() in patient.name.lower()]


    def list_patients(self):
        ''' list all patients '''
        return list(self.patients.values())
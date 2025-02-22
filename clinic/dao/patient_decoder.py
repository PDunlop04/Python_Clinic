import json
from clinic.patient import Patient
from clinic.patient_record import PatientRecord

class PatientDecoder(json.JSONDecoder):
    ''' Custom decoder for Patient objects '''
    def __init__(self, autosave=False):
        # Accept autosave argument in the constructor
        self.autosave = autosave
        super().__init__()

    def decode(self, s):
        ''' Override the decode method to handle custom decoding '''
        data = super().decode(s)
        if 'phn' in data:
            # Pass the autosave parameter here to create PatientRecord with it
            patient = Patient(
                phn=data['phn'],
                name=data['name'],
                birth_date=data['birth_date'],
                phone=data['phone'],
                email=data['email'],
                address=data['address']
            )
            if 'record' in data and data['record'] is not None:
                # Pass autosave as per the current context
                patient.record = PatientRecord.from_dict(data['record'], autosave=self.autosave)
            return patient
        return data
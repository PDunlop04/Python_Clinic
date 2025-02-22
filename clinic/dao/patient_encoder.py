import json
from clinic.patient import Patient
from clinic.patient_record import PatientRecord

class PatientEncoder(json.JSONEncoder):
    ''' Custom encoder for Patient objects '''
    def default(self, obj):
        if isinstance(obj, Patient):
            return {
                'phn': obj.phn,
                'name': obj.name,
                'birth_date': obj.birth_date,
                'phone': obj.phone,
                'email': obj.email,
                'address': obj.address,
                'record': obj.record.to_dict() if obj.record else None
            }
        return super().default(obj)
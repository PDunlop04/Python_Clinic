from unittest import TestCase
from unittest import main
from clinic.patient import *
from clinic.controller import *
class PatientTest(TestCase):
        def setUp(self):
                self.patient = Patient(9798884444, "Ali Mesbah", "1980-03-03", >
                self.controller = Controller()

        def test_patient_initialization(self):
                #Test initialization of Patient object with expected values.
                self.assertEqual(self.patient.phn, 9798884444)
                self.assertEqual(self.patient.name, "Ali Mesbah")
                self.assertEqual(self.patient.birth_date, "1980-03-03")
                self.assertEqual(self.patient.phone, "250 301 6060")
                self.assertEqual(self.patient.email, "mesbah.ali@gmail.com")
                self.assertEqual(self.patient.address, "500 Fairfield Rd, Victo>
        def test_patient_equality(self):
                # Test equality method for two Patient instances with the same >
                same_patient = Patient(9798884444, "Ali Mesbah", "1980-03-03", >
                different_patient = Patient(9792225555, "Joe Hancock", "1990-01>
                self.assertEqual(self.patient, same_patient)
                self.assertNotEqual(self.patient, different_patient)

                # retriving with partial word, should be false
                retrieved_list = self.controller.retrieve_patients("Jo")
                self.assertIsNone(retrieved_list, "retrieved list of patients h>


        def test_patient_string_representation(self):
                expected_string = (f"Patient PHN: {self.patient.phn}, Name: {se>
                                f"DOB: {self.patient.birth_date}, Phone: {self.>
                                f"Email: {self.patient.email}, Address: {self.p>
                self.assertEqual(str(self.patient), expected_string)

if __name__ == '__main__':
        unittest.main()
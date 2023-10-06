import sys
import datetime
from operator import itemgetter

user_table = {}
visit_table = {}
gender_table = {}
permissions_group_table = {}

patient0 = {"username": "patient0", "password": "hashed0", "first_name": "John", "last_name": "Smith", "date_of_birth": "1958-06-25", "gender": 1, "address": "123 Main Street", "city": "Yonkers", "state": "NY", "zipcode": 10470, "email": "josmith@email.com", "permission_group_id": 1}
patient1 = {"username": "patient1", "password": "hashed1", "first_name": "Jill", "last_name": "Smith", "date_of_birth": "1956-03-21", "gender": 2, "address": "123 Main Street", "city": "Yonkers", "state": "NY", "zipcode": 10470, "email": "jismith@email.com", "permission_group_id": 1}
patient2 = {"username": "patient3", "password": "hashed2", "first_name": "Bill", "last_name": "Johnson", "date_of_birth": "1968-04-15", "gender": 1, "address": "33 Main Street", "city": "Houston", "state": "TX", "zipcode": 77002, "email": "bjohns@email.com", "permission_group_id": 1}
doctor0 = {"username": "drchao", "password": "hashed3", "first_name": "Ken", "last_name": "Jeong", "date_of_birth": "1968-07-13", "gender": 1, "address": "334 Durham Street", "city": "Los Angeles", "state": "CA", "zipcode": 90012, "email": "kjeong@email.com", "permission_group_id": 2}
doctor1 = {"username": "aj", "password": "hashed4", "first_name": "Alice", "last_name": "Jackson", "date_of_birth": "1998-03-20", "gender": 2, "address": "14 Second Street", "city": "Los Angeles", "state": "CA", "zipcode": 90012, "email": "aj@email.com", "permission_group_id": 2}
doctor2 = {"username": "doctor2", "password": "hashed5", "first_name": "Tamika", "last_name": "Jennings", "date_of_birth": "1976-03-30", "gender": 2, "address": "22 Bellamy Street", "city": "Los Angeles", "state": "CA", "zipcode": 90012, "email": "doctor2@email.com", "permission_group_id": 3}

user_table = {1: patient0, 2: patient1, 3: patient2, 4: doctor0, 5: doctor1, 6: doctor2}

permission_group0 = {"permission_group_name": "Patient"}
permission_group1 = {"permission_group_name": "Diagnostic Doctor"}
permission_group2 = {"permission_group_name": "Treatment Doctor"}
permission_group_table = {1: permission_group0, 2: permission_group1, 3: permission_group2}

medical_visit0 = {"patient_id": 1, "date_of_visit": datetime.date(2021,1,1), "visit_type": 1, "height": 62, "weight": 140, "blood_pressure":120, "Notes": "Patient exhibited signs XYZ", "doctor_id":4}
medical_visit1 = {"patient_id": 2, "date_of_visit": datetime.date(2021,3,1), "visit_type": 1, "height": 65, "weight": 140, "blood_pressure":120, "Notes": "Patient exhibited signs XYZ", "doctor_id":5}
medical_visit2 = {"patient_id": 3, "date_of_visit": datetime.date(2021,7,1), "visit_type": 2, "height": 72, "weight": 140, "blood_pressure":150, "Notes": "Patient exhibited signs XYZ", "doctor_id":6}
medical_visit3 = {"patient_id": 1, "date_of_visit": datetime.date(2021,8,1), "visit_type": 1, "height": 63, "weight": 140, "blood_pressure":150, "Notes": "Patient exhibited signs XYZ", "doctor_id":4}
medical_visit4 = {"patient_id": 2, "date_of_visit": datetime.date(2021,9,1), "visit_type": 1, "height": 68, "weight": 140, "blood_pressure":150, "Notes": "Patient exhibited signs XYZ", "doctor_id":5}
medical_visit5 = {"patient_id": 1, "date_of_visit": datetime.date(2021,11,1), "visit_type": 2, "height": 61, "weight": 140, "blood_pressure":150, "Notes": "Patient exhibited signs XYZ", "doctor_id":6}
medical_visit6 = {"patient_id": 1, "date_of_visit": datetime.date(2022,3,1), "visit_type": 1, "height": 64, "weight": 180, "blood_pressure":180, "Notes": "Patient exhibited signs XYZ", "doctor_id":4}
medical_visit7 = {"patient_id": 3, "date_of_visit": datetime.date(2021,5,13), "visit_type": 1, "height": 64, "weight": 180, "blood_pressure":180, "Notes": "Patient exhibited signs XYZ", "doctor_id":4}
medical_visit8 = {"patient_id": 3, "date_of_visit": datetime.date(2021,5,12), "visit_type": 1, "height": 64, "weight": 180, "blood_pressure":180, "Notes": "Patient exhibited signs XYZ", "doctor_id":4}

visit_table = {1: medical_visit0, 2: medical_visit1, 3: medical_visit2, 4: medical_visit3, 5: medical_visit4, 6: medical_visit5, 7: medical_visit6, 8: medical_visit7}


visit_type0 = {"visit_type_name": "Diagnostic"}
visit_type1 = {"visit_type_name": "Treatment"}
visit_type_table = {1:visit_type0, 2: visit_type1}

gender_type0 = {"Name": "Male"}
gender_type1 = {"Name": "Female"}
gender_table = {1: gender_type0, 2: gender_type1}

class MedicalInformationService:
    DOCTOR_ACCESS_EVERY_PATIENTS_INFO = False
    DOCTOR_VIEW_ALL_DATA_FROM_PATIENT = False
    FAILED_AUTHORIZATION_RESPONSE = {"status": 403, "response_text": "Unauthorized"}

    def __init__(self, logged_in_user, user_table={}, visit_table={}, gender_table={}, permissions_group_table={}):
        self.logged_in_user = logged_in_user
        self.user_table = user_table
        self.visit_table = visit_table
        self.gender_table = gender_table
        self.permissions_group_table = permissions_group_table
        self.personal_info = {}
        self.last_12_months_visits = {} # dictionary to keep cache all patients' medical visits in last 12 months, key user_id, values list of medical visits
        self.sorted_blood_pressure_last_12_months = {} # dictionary to keep cache all patients' blood pressures from last 12 months, key user_id, values sorted list of blood pressure from last 12 months
        self.doctor_patients = set() # set of a user's patients
        self.medical_histories = {} # dictionary to keep cache all patients' medical histories, key user_id, values list of medical visits
        self.permissions_group = user_table[logged_in_user]["permission_group_id"]
    
    #################
    # authorization #
    #################

    def user_exists(self, user_id):
        try:
            id = int(user_id)
            if id in self.user_table.keys():
                return True
            else:
                return False
        except:
            print("Invalid id type")
            return False

    def is_doctor(self):
        if self.user_exists(self.logged_in_user):
            return self.user_table[self.logged_in_user]["permission_group_id"] > 1
        return False

    def authorize_doctor(self, patient_id, visit_type=0, see_every_patient_data=DOCTOR_ACCESS_EVERY_PATIENTS_INFO, see_all_data_from_patient=DOCTOR_VIEW_ALL_DATA_FROM_PATIENT):
        if self.is_doctor() and self.user_exists(patient_id):
            if see_every_patient_data:
                return True
            elif see_all_data_from_patient and patient_id in self.get_doctor_patients():
                return True
            else:
                if patient_id in self.get_doctor_patients() and self.permissions_group - 1 == visit_type:
                    return True
        return False

    def authorize_patient(self, patient_id):
        if self.user_exists(patient_id) and self.logged_in_user == patient_id:
            return True
        else:
            return False
            
    def authorize_patient_or_patient_doctor(self, user_id, see_every_patient_data=DOCTOR_ACCESS_EVERY_PATIENTS_INFO):
        if self.authorize_patient(user_id) or self.authorize_doctor(user_id, see_every_patient_data=see_every_patient_data):
            return True
        return False
    
    def get_doctor_patients(self):
        if self.doctor_patients:
            return self.doctor_patients
        else:
            patients = set()
            if self.is_doctor():
                for visit_id in self.visit_table.keys():
                    if self.visit_table[visit_id]["doctor_id"] == self.logged_in_user:
                        patients.add(self.visit_table[visit_id]["patient_id"])
                self.doctor_patients = patients
            return patients

    # This would be replaced with a SELECT {user_info_fields} FROM Users WHERE patient_id = {user}
    def get_personal_info(self, patient_id):
        if self.authorize_patient_or_patient_doctor(patient_id, see_every_patient_data=True):
            if patient_id in self.personal_info.keys() and self.personal_info[patient_id]:
                return {"status": 200, "response_text" : self.personal_info[patient_id], "cached": True}
            user_info_fields = ["first_name", "last_name", "date_of_birth", "address", "city", "state", "zipcode", "email", "gender"]
            user_info = self.user_table[patient_id]
            info = {}
            for field in user_info_fields:
                info[field] = user_info[field]
            info['gender'] = self.gender_table[info['gender']]['Name']
            self.personal_info[patient_id] = info
            return {"status": 200, "response_text" : info}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

    # This would be replaced with a UPDATE Users SET {query_string} WHERE user_id = {user}
    def edit_personal_info(self, patient_id, **kwargs):
        if self.authorize_patient(patient_id):
            for k in kwargs:
                if k in self.user_table[patient_id].keys():
                    self.user_table[patient_id][k] = kwargs[k]
            if patient_id in self.personal_info.keys():
                del self.personal_info[patient_id]
            return {"status": 200, "response_text": "OK"}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

    # This would be replaced with a SELECT * FROM visits WHERE patient_id = {user} ORDER BY date_of_visit DESC
    def get_medical_history(self,patient_id):
        if self.authorize_patient_or_patient_doctor(patient_id, see_every_patient_data=True):
            if patient_id in self.medical_histories.keys() and self.medical_histories[patient_id]:
                return {"status": 200, "response_text": self.medical_histories[patient_id], "cached": True}
            else:
                visits = []
                for v in self.visit_table.keys():
                    visit = self.visit_table[v]
                    if  visit["patient_id"] == patient_id and (self.authorize_doctor(patient_id, visit["visit_type"]) or self.authorize_patient(patient_id)):
                        visits.append(visit)
                sorted_visits = sorted(visits, key=itemgetter('date_of_visit'), reverse=True)
                self.medical_histories[patient_id] = sorted_visits
                return {"status": 200, "response_text": sorted_visits}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

    def edit_medical_history(self, patient_id, visit, **kwargs):
        if self.user_exists(patient_id) and visit in self.visit_table and self.authorize_doctor(patient_id, self.visit_table[visit]["visit_type"]):
            visit_to_update = self.visit_table[visit]
            for k in kwargs:
                if k in self.visit_table[visit].keys():
                    visit_to_update[k] = kwargs[k]
            return {"status": 200, "response_text": "OK"}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

    # This would be replaced with a SELECT * FROM visits WHERE date_of_visit > CONVERT(DATE, GETDATE()) ORDER BY date_of_visit DESC
    def get_last_12_months_visits(self, patient_id):
        if self.authorize_patient_or_patient_doctor(patient_id, see_every_patient_data=True):
            if patient_id in self.last_12_months_visits and self.last_12_months_visits[patient_id]:
                return {"status": 200, "response_text": self.last_12_months_visits[patient_id], "cached": True}
            elif patient_id in self.medical_histories.keys() and self.medical_histories[patient_id]:
                visits = self.medical_histories[patient_id]
            else:
                self.get_medical_history(patient_id)
                visits = self.medical_histories[patient_id]
            today = datetime.date.today()
            last_12 = []
            i = 0
            print(len(visits))
            while i < len(visits) and visits[i]['date_of_visit'] >= today + datetime.timedelta(days=Helpers.calculate_year_ago_in_days(today)):
                last_12.append(visits[i])
                i += 1
            self.last_12_months_visits[patient_id] = last_12
            return {"status": 200, "response_text": last_12}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

    def get_sorted_blood_pressure_last_12_months(self, patient_id, desc=True):
        if self.authorize_patient_or_patient_doctor(patient_id, see_every_patient_data=True):
            if patient_id in self.last_12_months_visits.keys() and self.last_12_months_visits[patient_id]:
                pass
            else:
                self.get_last_12_months_visits(patient_id)
            if self.last_12_months_visits:
                sorted_blood_pressure = sorted(self.last_12_months_visits[patient_id], key=itemgetter('blood_pressure'), reverse=desc)
                temp = []
                for bp in sorted_blood_pressure:
                    temp.append(bp["blood_pressure"])
                self.sorted_blood_pressure_last_12_months[patient_id] = temp
                return {"status": 200, "response_text": sorted_blood_pressure}
            else:
                return {"status": 404, "response_text": "No recent visits"}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

    # This would be replaced with a SELECT MIN(blood_pressure) FROM visits WHERE patient_id = {user} AND date_of_visit > DATEADD(year, -1, CONVERT(DATE, GETDATE()) GROUP BY patient_id
    def get_min_blood_pressure_last_12_months(self, patient_id):
        if self.authorize_patient_or_patient_doctor(patient_id, see_every_patient_data=True):
            if patient_id in self.sorted_blood_pressure_last_12_months.keys() and self.sorted_blood_pressure_last_12_months[patient_id]:
                return {"status": 200, "response_text": self.sorted_blood_pressure_last_12_months[patient_id][len(self.sorted_blood_pressure_last_12_months[patient_id])-1], "cached": True}
            self.get_sorted_blood_pressure_last_12_months(patient_id)['response_text']
            sorted_blood_pressure = self.sorted_blood_pressure_last_12_months[patient_id]
            if len(sorted_blood_pressure) > 0:
                return {"status": 200, "response_text": sorted_blood_pressure[len(sorted_blood_pressure)-1]}
            else:
                return {"status": 404, "response_text": "No blood pressure history"}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

    # This would be replaced with a SELECT MAX(blood_pressure) FROM visits WHERE patient_id = {user} AND date_of_visit > DATEADD(year, -1, CONVERT(DATE, GETDATE()) GROUP BY patient_id
    def get_max_blood_pressure_last_12_months(self, patient_id):
        if self.authorize_patient_or_patient_doctor(patient_id, see_every_patient_data=True):
            if patient_id in self.sorted_blood_pressure_last_12_months.keys() and self.sorted_blood_pressure_last_12_months[patient_id]:
                return {"status": 200, "response_text": self.sorted_blood_pressure_last_12_months[patient_id][0], "cached": True}
            self.get_sorted_blood_pressure_last_12_months(patient_id)
            if len(self.sorted_blood_pressure_last_12_months) > 0:
                return {"status": 200, "response_text": self.sorted_blood_pressure_last_12_months[patient_id][0]}
            else:
                return {"status": 404, "response_text": "No blood pressure history"}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

    # This would be replaced with a SELECT AVG(blood_pressure) FROM visits WHERE patient_id = {user} AND date_of_visit > DATEADD(year, -1, CONVERT(DATE, GETDATE()) GROUP BY patient_id
    def get_avg_blood_pressure_last_12_months(self, patient_id):
        if self.authorize_patient_or_patient_doctor(patient_id, see_every_patient_data=True):
            if patient_id in self.sorted_blood_pressure_last_12_months.keys() and self.sorted_blood_pressure_last_12_months[patient_id]:
                pass
            else:
                self.get_sorted_blood_pressure_last_12_months(patient_id)
            sorted_blood_pressure = self.sorted_blood_pressure_last_12_months[patient_id]
            if type(sorted_blood_pressure) == str:
                return {"status": 404, "response_text": sorted_blood_pressure}
            else:
                if len(sorted_blood_pressure) > 0:
                    avg = sum(sorted_blood_pressure)/len(sorted_blood_pressure)
                    return {"status": 200, "response_text": avg}
                else:
                    return {"status": 404, "response_text": "No blood pressure history"}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

    def get_median_blood_pressure_last_12_months(self, patient_id):
        if self.authorize_patient_or_patient_doctor(patient_id, see_every_patient_data=True):
            if patient_id in self.sorted_blood_pressure_last_12_months.keys() and self.sorted_blood_pressure_last_12_months[patient_id]:
                pass
            else:
                self.get_sorted_blood_pressure_last_12_months(patient_id)
            sorted_blood_pressure = self.sorted_blood_pressure_last_12_months[patient_id]
            if len(sorted_blood_pressure) > 0:
                if len(sorted_blood_pressure) % 2 == 1:
                    median = sorted_blood_pressure[len(sorted_blood_pressure)//2]
                else:
                    middle = len(sorted_blood_pressure)//2
                    median = (sorted_blood_pressure[middle] + sorted_blood_pressure[middle-1])/2
                return {"status":200, "response_text": median}
            else:
                return {"status": 404, "response_text": "No blood pressure history"}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE


    # This would be replaced with a SELECT TOP 1 height FROM visits WHERE patient_id = {user} ORDER BY date_of_visit DESC
    def get_height(self, patient_id):
        if self.authorize_patient_or_patient_doctor(patient_id):
            if patient_id in self.medical_histories.keys() and self.medical_histories[patient_id]:
                return {"status":200, "response_text": self.medical_histories[patient_id][0]["height"]}
            else:
                self.get_medical_history(patient_id)
            if self.medical_histories[patient_id]:
                return {"status":200, "response_text": self.medical_histories[patient_id][0]["height"]}
            else:
                return {"status": 404, "response_text": "No height history"}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

    # This would be replaced with a SELECT TOP 1 weight FROM visits WHERE patient_id = {user} ORDER BY date_of_visit DESC
    def get_weight(self, patient_id):
        if self.authorize_patient_or_patient_doctor(patient_id):
            if patient_id in self.medical_histories.keys() and self.medical_histories[patient_id]:
                return {"status":200, "response_text": self.medical_histories[patient_id][0]["weight"], "cached":True}
            else:
                self.get_medical_history(patient_id)
            if self.medical_histories[patient_id]:
                return {"status":200, "response_text": self.medical_histories[patient_id][0]["weight"]}
            else:
                return {"status": 404, "response_text": "No weight history"}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

    def get_current_BMI(self, patient_id):
        if self.authorize_patient_or_patient_doctor(patient_id):
            kgs = Helpers.convert_lbs_to_kgs(self.get_weight(patient_id)['response_text'])
            m = Helpers.convert_inches_to_meters(self.get_height(patient_id)['response_text'])
            return {"status": 200, "response_text" : (kgs/(m**2))}
        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

   
    def get_summary(self, patient_id):
        '''
        Basic patient information such as name, birthday, gender, height, and weight.
        Current BMI calculated from the medical history.
        Min, mean, median, and max for blood pressure and heart rate within the last 12 months.
        List of visits within the last 12 months.
        '''  
        if self.authorize_patient_or_patient_doctor(patient_id):
            data = {}
            personal_info = self.get_personal_info(patient_id)['response_text']
            data["last_name"] = personal_info['last_name']
            data["fist_name"] = personal_info['first_name']
            data["gender"] = personal_info["gender"]
            data["height"] = self.get_height(patient_id)['response_text']
            data["weight"] = self.get_weight(patient_id)['response_text']
            data["bmi"] = self.get_current_BMI(patient_id)['response_text']
            data["min_blood_pressure"] = self.get_min_blood_pressure_last_12_months(patient_id)['response_text']
            data["avg_blood_pressure"] = self.get_avg_blood_pressure_last_12_months(patient_id)['response_text']
            data["median_blood_pressure"] = self.get_median_blood_pressure_last_12_months(patient_id)['response_text']
            data["max_blood_pressure"] = self.get_max_blood_pressure_last_12_months(patient_id)['response_text']
            data["visits_last_12_months"] = self.get_last_12_months_visits(patient_id)['response_text']
            return {"status": 200, "response_text": data}

        else:
            return self.FAILED_AUTHORIZATION_RESPONSE

class Helpers:
    def convert_inches_to_meters(inches: int):
        centimeters = inches * 2.58
        meters = centimeters / 100
        return meters

    def convert_lbs_to_kgs(lbs: float):
        return lbs * 0.45359237

    def calculate_year_ago_in_days(d: datetime):
        today = datetime.date.today()
        if today.year % 4 == 0 and today.month > 2:
            return -366
        elif today.year % 4 == 1 and today.month <= 2:
            return -366
        else:
            return -365
    
    
class TestHelpers:

    def test_convert_inches_to_meters():
        assert Helpers.convert_inches_to_meters(100) == 2.58

    def test_convert_lbs_to_kgs():
        assert Helpers.convert_lbs_to_kgs(3) == 1.36077711

class TestMedicalInformationService:
    patient0 = {"username": "patient0", "password": "hashed0", "first_name": "John", "last_name": "Smith", "date_of_birth": "1958-06-25", "gender": 1, "address": "123 Main Street", "city": "Yonkers", "state": "NY", "zipcode": 10470, "email": "josmith@email.com", "permission_group_id": 1}
    patient1 = {"username": "patient1", "password": "hashed1", "first_name": "Jill", "last_name": "Smith", "date_of_birth": "1956-03-21", "gender": 2, "address": "123 Main Street", "city": "Yonkers", "state": "NY", "zipcode": 10470, "email": "jismith@email.com", "permission_group_id": 1}
    patient2 = {"username": "patient3", "password": "hashed2", "first_name": "Bill", "last_name": "Johnson", "date_of_birth": "1968-04-15", "gender": 1, "address": "33 Main Street", "city": "Houston", "state": "TX", "zipcode": 77002, "email": "bjohns@email.com", "permission_group_id": 1}
    doctor0 = {"username": "drchao", "password": "hashed3", "first_name": "Ken", "last_name": "Jeong", "date_of_birth": "1968-07-13", "gender": 1, "address": "334 Durham Street", "city": "Los Angeles", "state": "CA", "zipcode": 90012, "email": "kjeong@email.com", "permission_group_id": 2}
    doctor1 = {"username": "aj", "password": "hashed4", "first_name": "Alice", "last_name": "Jackson", "date_of_birth": "1998-03-20", "gender": 2, "address": "14 Second Street", "city": "Los Angeles", "state": "CA", "zipcode": 90012, "email": "aj@email.com", "permission_group_id": 2}
    doctor2 = {"username": "doctor2", "password": "hashed5", "first_name": "Tamika", "last_name": "Jennings", "date_of_birth": "1976-03-30", "gender": 2, "address": "22 Bellamy Street", "city": "Los Angeles", "state": "CA", "zipcode": 90012, "email": "doctor2@email.com", "permission_group_id": 3}

    user_table = {1: patient0, 2: patient1, 3: patient2, 4: doctor0, 5: doctor1, 6: doctor2}

    permission_group0 = {"permission_group_name": "Patient"}
    permission_group1 = {"permission_group_name": "Diagnostic Doctor"}
    permission_group2 = {"permission_group_name": "Treatment Doctor"}
    permission_group_table = {1: permission_group0, 2: permission_group1, 3: permission_group2}

    medical_visit0 = {"patient_id": 1, "date_of_visit": datetime.date(2021,1,1), "visit_type": 1, "height": 62, "weight": 140, "blood_pressure":120, "Notes": "Patient exhibited signs XYZ", "doctor_id":4}
    medical_visit1 = {"patient_id": 2, "date_of_visit": datetime.date(2021,3,1), "visit_type": 1, "height": 65, "weight": 140, "blood_pressure":120, "Notes": "Patient exhibited signs XYZ", "doctor_id":5}
    medical_visit2 = {"patient_id": 3, "date_of_visit": datetime.date(2021,7,1), "visit_type": 2, "height": 72, "weight": 140, "blood_pressure":150, "Notes": "Patient exhibited signs XYZ", "doctor_id":6}
    medical_visit3 = {"patient_id": 1, "date_of_visit": datetime.date(2021,8,1), "visit_type": 1, "height": 63, "weight": 140, "blood_pressure":150, "Notes": "Patient exhibited signs XYZ", "doctor_id":4}
    medical_visit4 = {"patient_id": 2, "date_of_visit": datetime.date(2021,9,1), "visit_type": 1, "height": 68, "weight": 140, "blood_pressure":150, "Notes": "Patient exhibited signs XYZ", "doctor_id":5}
    medical_visit5 = {"patient_id": 1, "date_of_visit": datetime.date(2021,11,1), "visit_type": 2, "height": 61, "weight": 140, "blood_pressure":150, "Notes": "Patient exhibited signs XYZ", "doctor_id":6}
    medical_visit6 = {"patient_id": 1, "date_of_visit": datetime.date(2023,3,1), "visit_type": 1, "height": 64, "weight": 180, "blood_pressure":180, "Notes": "Patient exhibited signs XYZ", "doctor_id":4}
    medical_visit7 = {"patient_id": 3, "date_of_visit": datetime.date.today(), "visit_type": 1, "height": 64, "weight": 180, "blood_pressure":180, "Notes": "Patient exhibited signs XYZ", "doctor_id":4}
    medical_visit8 = {"patient_id": 3, "date_of_visit": datetime.date.today() + datetime.timedelta(days=-1), "visit_type": 1, "height": 64, "weight": 180, "blood_pressure":180, "Notes": "Patient exhibited signs XYZ", "doctor_id":4}

    visit_table = {1: medical_visit0, 2: medical_visit1, 3: medical_visit2, 4: medical_visit3, 5: medical_visit4, 6: medical_visit5, 7: medical_visit6, 8: medical_visit7}


    visit_type0 = {"visit_type_name": "Diagnostic"}
    visit_type1 = {"visit_type_name": "Treatment"}
    visit_type_table = {1:visit_type0, 2: visit_type1}

    gender_type0 = {"Name": "Male"}
    gender_type1 = {"Name": "Female"}
    gender_table = {1: gender_type0, 2: gender_type1}

    def initializeMIS(self, user, user_table=user_table, visit_table=visit_table, permissions_group_table=permissions_group_table, gender_table=gender_table):
        return MedicalInformationService(user, user_table=self.user_table, visit_table=self.visit_table, gender_table=self.gender_table, permissions_group_table=self.permission_group_table)

    def test_user_exists(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.user_exists(1)
        assert mis.user_exists(6)
        
    def test_user_exists_fail(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert not mis.user_exists(0)
        assert mis.user_exists(1)
        assert mis.user_exists(6)
        assert not mis.user_exists(7)

    def test_is_doctor(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        return mis.is_doctor()
    
    def test_is_doctor_fail(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        return not mis.is_doctor()

    def test_auth_doctor(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.authorize_doctor(1, visit_type=1)

    def test_auth_doctor_see_every_patient(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.authorize_doctor(3, see_every_patient_data=True)

    def test_auth_doctor_see_all_data_from_patient(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.authorize_doctor(3, see_every_patient_data=True)
    
    def test_auth_doctor_fail_wrong_visit(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert not mis.authorize_doctor(1, visit_type=2)

    def test_auth_doctor_fail_wrong_patient(self):
        mis = self.initializeMIS(5, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert not mis.authorize_doctor(3, visit_type=1)

    def test_auth_patient(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.authorize_patient(1)

    def test_auth_patient_fail(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert not mis.authorize_patient(2)

    def test_get_doctor_patients(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        mis.get_doctor_patients()
        assert 1 in mis.doctor_patients and 3 in mis.doctor_patients

    def test_get_doctor_patients_fail(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        mis.get_doctor_patients()
        assert not mis.doctor_patients

    def test_get_personal_info(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        history = mis.get_personal_info(1)
        assert history['response_text'] == {'first_name': 'John', 'last_name': 'Smith', 'date_of_birth': '1958-06-25', 'address': '123 Main Street', 'city': 'Yonkers', 'state': 'NY', 'zipcode': 10470, 'email': 'josmith@email.com', 'gender': 'Male'}
        assert 'cached' not in history.keys()

    def test_get_personal_info_cached(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        mis.get_personal_info(1)
        history2 = mis.get_personal_info(1)
        assert 'cached' in history2

    def test_get_personal_info_as_doctor(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        history = mis.get_personal_info(1)
        assert history['response_text'] == {'first_name': 'John', 'last_name': 'Smith', 'date_of_birth': '1958-06-25', 'address': '123 Main Street', 'city': 'Yonkers', 'state': 'NY', 'zipcode': 10470, 'email': 'josmith@email.com', 'gender': 'Male'}

    def test_get_personal_info_fail_auth(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        history = mis.get_personal_info(2)
        assert history == mis.FAILED_AUTHORIZATION_RESPONSE
     
    def test_edit_personal_info(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        mis.edit_personal_info(1,address="890 New Street", city="Brooklyn")
        assert self.user_table[1]["address"] == "890 New Street"
        assert self.user_table[1]["city"] == "Brooklyn"
        assert mis.get_personal_info(1)['response_text'] == {'first_name': 'John', 'last_name': 'Smith', 'date_of_birth': '1958-06-25', 'address': '890 New Street', 'city': 'Brooklyn', 'state': 'NY', 'zipcode': 10470, 'email': 'josmith@email.com', 'gender': 'Male'}

    def test_edit_personal_info_fail_auth(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        resp = mis.edit_personal_info(2,address="890 New Street", city="Brooklyn")
        assert resp == mis.FAILED_AUTHORIZATION_RESPONSE

    def test_get_medical_history(self):
        mis = self.initializeMIS(5, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        resp = mis.get_medical_history(2)
        assert resp == {'status': 200, 'response_text': [{'patient_id': 2, 'date_of_visit': datetime.date(2021, 9, 1), 'visit_type': 1, 'height': 68, 'weight': 140, 'blood_pressure': 150, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 5}, {'patient_id': 2, 'date_of_visit': datetime.date(2021, 3, 1), 'visit_type': 1, 'height': 65, 'weight': 140, 'blood_pressure': 120, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 5}]}
        assert 'cached' not in resp.keys()

    def test_get_medical_history_patient(self):
        mis = self.initializeMIS(2, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        history = mis.get_medical_history(2)
        assert history == {'status': 200, 'response_text': [{'patient_id': 2, 'date_of_visit': datetime.date(2021, 9, 1), 'visit_type': 1, 'height': 68, 'weight': 140, 'blood_pressure': 150, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 5}, {'patient_id': 2, 'date_of_visit': datetime.date(2021, 3, 1), 'visit_type': 1, 'height': 65, 'weight': 140, 'blood_pressure': 120, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 5}]}

    def test_get_medical_history_cached(self):
        mis = self.initializeMIS(5, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        resp = mis.get_medical_history(2)
        assert resp == {'status': 200, 'response_text': [{'patient_id': 2, 'date_of_visit': datetime.date(2021, 9, 1), 'visit_type': 1, 'height': 68, 'weight': 140, 'blood_pressure': 150, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 5}, {'patient_id': 2, 'date_of_visit': datetime.date(2021, 3, 1), 'visit_type': 1, 'height': 65, 'weight': 140, 'blood_pressure': 120, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 5}]}
        resp2 = mis.get_medical_history(2)
        resp['cached'] = True
        assert resp2 == resp

    def test_get_medical_history_fail_wrong_doctor(self):
        mis = self.initializeMIS(5, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_medical_history(3) == {'status': 200, 'response_text': []}

    def test_edit_medical_history(self):
        mis = self.initializeMIS(5, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        mis.edit_medical_history(2, 5, height= 70, weight=131)
        assert self.visit_table[5]["height"] == 70
        assert self.visit_table[5]["weight"] == 131

    def test_edit_medical_history_fail_doctor_auth(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        mis.edit_medical_history(2, 5, height=74, weight=141)
        assert not self.visit_table[5]["height"] == 74
        assert not self.visit_table[5]["weight"] == 141
        history = mis.get_medical_history(2)
        assert not history == {'status': 200, 'response_text': [{'patient_id': 2, 'date_of_visit': datetime.date(2021, 9, 1), 'visit_type': 1, 'height': 74, 'weight': 141, 'blood_pressure': 150, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 5}, {'patient_id': 2, 'date_of_visit': datetime.date(2021, 3, 1), 'visit_type': 1, 'height': 65, 'weight': 140, 'blood_pressure': 120, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 5}]}
    
    def test_get_last_12_months_visits(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        resp = mis.get_last_12_months_visits(1)
        assert resp['response_text'] == [{'patient_id': 1, 'date_of_visit': datetime.date(2023, 3, 1), 'visit_type': 1, 'height': 64, 'weight': 180, 'blood_pressure': 180, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 4}, {'patient_id': 1, 'date_of_visit': datetime.date(2021, 8, 1), 'visit_type': 1, 'height': 63, 'weight': 140, 'blood_pressure': 150, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 4}]
        assert 'cached' not in resp.keys()

    def test_get_last_12_months_visits_cached(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        resp = mis.get_last_12_months_visits(1)
        assert resp['response_text'] == [{'patient_id': 1, 'date_of_visit': datetime.date(2022, 3, 1), 'visit_type': 1, 'height': 64, 'weight': 180, 'blood_pressure': 180, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 4}, {'patient_id': 1, 'date_of_visit': datetime.date(2021, 8, 1), 'visit_type': 1, 'height': 63, 'weight': 140, 'blood_pressure': 150, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 4}]
        resp2 = mis.get_last_12_months_visits(1)
        assert resp2['response_text'] == resp['response_text']
        assert resp2['cached']
        
    def test_get_last_12_months_visits_patient(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        resp = mis.get_last_12_months_visits(1)
        assert resp == {'status': 200, 'response_text': [{'patient_id': 1, 'date_of_visit': datetime.date(2022, 3, 1), 'visit_type': 1, 'height': 64, 'weight': 180, 'blood_pressure': 180, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 4}, {'patient_id': 1, 'date_of_visit': datetime.date(2021, 11, 1), 'visit_type': 2, 'height': 61, 'weight': 140, 'blood_pressure': 150, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 6}, {'patient_id': 1, 'date_of_visit': datetime.date(2021, 8, 1), 'visit_type': 1, 'height': 63, 'weight': 140, 'blood_pressure': 150, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 4}]}

    def test_get_last_12_months_visits_fail_auth(self):
        mis = self.initializeMIS(2, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_last_12_months_visits(1) == mis.FAILED_AUTHORIZATION_RESPONSE

    def test_get_last_12_months_visits_corner_cases(self):
        mis = self.initializeMIS(3, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert len(mis.get_last_12_months_visits(3)['response_text']) == 2

    def test_get_min_blood_pressure_last_12_months(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        resp = mis.get_min_blood_pressure_last_12_months(1)
        print(resp)
        assert resp['response_text'] == 150
        resp2 = mis.get_min_blood_pressure_last_12_months(1)
        assert resp2['response_text'] == 150
        assert resp2['cached'] == True
    
    def test_get_min_blood_pressure_last_12_months_patient(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_min_blood_pressure_last_12_months(1)['response_text'] == 150
    
    def test_get_min_blood_pressure_last_12_months_fail_auth(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_min_blood_pressure_last_12_months(2) == mis.FAILED_AUTHORIZATION_RESPONSE

    def test_get_max_blood_pressure_last_12_months(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_max_blood_pressure_last_12_months(1)['response_text'] == 180

    def test_get_max_blood_pressure_last_12_months_patient(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_max_blood_pressure_last_12_months(1)['response_text'] == 180

    def test_get_max_blood_pressure_last_12_months_fail_auth(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_max_blood_pressure_last_12_months(2) == mis.FAILED_AUTHORIZATION_RESPONSE

    def test_get_avg_blood_pressure_last_12_months(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_avg_blood_pressure_last_12_months(1)['response_text'] == 165

    def test_get_avg_blood_pressure_last_12_months_patient(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_avg_blood_pressure_last_12_months(1)['response_text'] == 160

    def test_get_avg_blood_pressure_last_12_months_fail_auth(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_avg_blood_pressure_last_12_months(2) == mis.FAILED_AUTHORIZATION_RESPONSE

    def test_get_median_blood_pressure_last_12_months(self):
        mis = self.initializeMIS(4, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_median_blood_pressure_last_12_months(1)['response_text'] == 165

    def test_get_median_blood_pressure_last_12_months_patient(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_median_blood_pressure_last_12_months(1)['response_text'] == 150
    
    def test_get_median_blood_pressure_last_12_months_fail_auth(self):
        mis = self.initializeMIS(2, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_median_blood_pressure_last_12_months(1) == mis.FAILED_AUTHORIZATION_RESPONSE

    def test_get_height(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_height(1)['response_text'] == 64
    
    def test_get_weight(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        resp = mis.get_weight(1)
        assert resp['response_text'] == 180
        assert 'cached' not in resp.keys()
        resp2 = mis.get_weight(1)
        assert 'cached' in resp2.keys()
        assert resp2['response_text'] == 180
        
    def test_calculate_bmi(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_current_BMI(1)['response_text'] == 29.946004517855936

    def test_calculate_bmi_fail_auth(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_current_BMI(2) == mis.FAILED_AUTHORIZATION_RESPONSE

    def test_get_summary(self):
        mis = self.initializeMIS(1, user_table=self.user_table, visit_table=self.visit_table, permissions_group_table=self.permission_group_table, gender_table=self.gender_table)
        assert mis.get_summary(1) == {'status': 200, 'response_text': {'last_name': 'Smith', 'fist_name': 'John', 'gender': 'Male', 'height': 64, 'weight': 180, 'bmi': 29.946004517855936, 'min_blood_pressure': 150, 'avg_blood_pressure': 160.0, 'median_blood_pressure': 150, 'max_blood_pressure': 180, 'visits_last_12_months': [{'patient_id': 1, 'date_of_visit': datetime.date(2022, 3, 1), 'visit_type': 1, 'height': 64, 'weight': 180, 'blood_pressure': 180, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 4}, {'patient_id': 1, 'date_of_visit': datetime.date(2021, 11, 1), 'visit_type': 2, 'height': 61, 'weight': 140, 'blood_pressure': 150, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 6}, {'patient_id': 1, 'date_of_visit': datetime.date(2021, 8, 1), 'visit_type': 1, 'height': 63, 'weight': 140, 'blood_pressure': 150, 'Notes': 'Patient exhibited signs XYZ', 'doctor_id': 4}]}}

def run_tests():
    tester = TestMedicalInformationService()
    tester.test_user_exists()
    tester.test_user_exists_fail()
    tester.test_is_doctor()
    tester.test_is_doctor_fail()
    tester.test_auth_doctor()
    tester.test_auth_doctor_see_all_data_from_patient()
    tester.test_auth_doctor_see_every_patient()
    tester.test_auth_doctor_fail_wrong_visit()
    tester.test_auth_doctor_fail_wrong_patient()
    tester.test_auth_patient()
    tester.test_auth_patient_fail()
    tester.test_get_doctor_patients()
    tester.test_get_doctor_patients_fail()
    tester.test_get_personal_info()
    tester.test_get_personal_info_as_doctor()
    tester.test_get_personal_info_cached()
    tester.test_get_personal_info_fail_auth()
    tester.test_edit_personal_info()
    tester.test_edit_personal_info_fail_auth()
    tester.test_get_height()
    tester.test_get_weight()
    tester.test_calculate_bmi()
    tester.test_calculate_bmi_fail_auth()
    tester.test_edit_personal_info()
    tester.test_get_medical_history()
    tester.test_get_medical_history_cached()
    tester.test_get_medical_history_patient()
    tester.test_get_medical_history_fail_wrong_doctor()
    tester.test_edit_medical_history()
    tester.test_edit_medical_history_fail_doctor_auth()
    # last 12 months call will not work unless you update the dates of the visits.
    tester.test_get_last_12_months_visits()
    tester.test_get_last_12_months_visits_cached()
    tester.test_get_last_12_months_visits_fail_auth()
    tester.test_get_last_12_months_visits_patient()
    tester.test_get_last_12_months_visits_corner_cases()
    tester.test_get_min_blood_pressure_last_12_months()
    tester.test_get_min_blood_pressure_last_12_months_patient()
    tester.test_get_min_blood_pressure_last_12_months_fail_auth()
    tester.test_get_max_blood_pressure_last_12_months()
    tester.test_get_max_blood_pressure_last_12_months_patient()
    tester.test_get_max_blood_pressure_last_12_months_fail_auth()
    tester.test_get_avg_blood_pressure_last_12_months()
    tester.test_get_avg_blood_pressure_last_12_months_patient()
    tester.test_get_avg_blood_pressure_last_12_months_fail_auth()
    tester.test_get_median_blood_pressure_last_12_months()
    tester.test_get_median_blood_pressure_last_12_months_patient()
    tester.test_get_median_blood_pressure_last_12_months_fail_auth()
    tester.test_get_summary()

i = 1
if sys.argv[i] != 'run_tests':
    logged_in_user = int(sys.argv[i])
    i += 1
    mis = MedicalInformationService(logged_in_user, user_table=user_table, visit_table=visit_table, permissions_group_table=permission_group_table, gender_table=gender_table)
while i < len(sys.argv) - 1:
    if sys.argv[i].lower() == 'run_tests':
        run_tests()
        print("Tests Success")
        i += 1
    else:
        endpoint = sys.argv[i]
        i += 1
        user = int(sys.argv[i])
        i += 1
        if sys.argv[i-2].lower() == 'MedicalInformationService'.lower():
            user = int(sys.argv[i-1])
            mis = MedicalInformationService(logged_in_user,user_table=user_table, visit_table=visit_table, permissions_group_table=permission_group_table, gender_table=gender_table)
        elif endpoint.lower() == 'get_weight':
            print(mis.get_weight(user))
        elif endpoint.lower() == 'get_height':
            print(mis.get_height(user))
        elif endpoint.lower() == 'get_median_blood_pressure_last_12_months':
            print(mis.get_median_blood_pressure_last_12_months(user))
        elif endpoint.lower() == 'get_avg_blood_pressure_last_12_months':
            print(mis.get_avg_blood_pressure_last_12_months(user))
        elif endpoint.lower() == 'get_min_blood_pressure_last_12_months':
            print(mis.get_min_blood_pressure_last_12_months(user))
        elif endpoint.lower() == 'get_max_blood_pressure_last_12_months':
            print(mis.get_max_blood_pressure_last_12_months(user))
        elif endpoint.lower() == 'get_last_12_months_visits':
            print(mis.get_last_12_months_visits(user))
        elif endpoint.lower() == 'get_medical_history':
            print(mis.get_medical_history(user))
        elif endpoint.lower() == 'get_avg_blood_pressure_last_12_months':
            print(mis.get_avg_blood_pressure_last_12_months(user))
        elif endpoint.lower() == 'get_personal_info':
            print(mis.get_personal_info(user))
        elif endpoint.lower() == 'get_current_BMI':
            print(mis.get_current_BMI(user))
        elif endpoint.lower() == 'edit_medical_history':
            data = {}
            i += 1
            visit = int(sys.argv[i])
            i += 1
            integer_keys = ['patient_id', 'visit_type', 'height', 'doctor_id']
            while i < len(sys.argv) and sys.argv[i] != '-':
                key = sys.argv[i].lower()
                i += 1
                value = sys.argv[i]
                if key in integer_keys:
                    value = int(value)
                elif key == 'weight'.lower():
                    value = float(value)
                data[key] = value
                i += 1
            print(mis.edit_medical_history(user, visit, **data))
            print(mis.get_medical_history(user))
            i += 1 # move past the '-'
        elif endpoint.lower() == 'edit_personal_info':
            data = {}
            while i < len(sys.argv)-1 and sys.argv[i] != '-':
                key = sys.argv[i]
                i += 1
                data[key] = sys.argv[i]
                i += 1
            mis.edit_personal_info(user, **data)
            print(mis.get_personal_info(user))
            i += 1 # move past the '-'

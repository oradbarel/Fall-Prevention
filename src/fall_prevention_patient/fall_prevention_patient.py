import json

ID_LEN = 9
MIN_AGE = 0
MAX_AGE = 128
MIN_WEIGHT = 0
MAX_WEIGHT = 256
MIN_HEIGHT = 0
MAX_HEIGHT = 256
MIN_FLOOR = -16
MAX_FLOOR = 32
MIN_ROOM = 0
MAX_ROOM = 64
MIN_BED = 0
MAX_BED = 8

class Patient():
    def __init__(self, name, id, age, weight, height, sex, floor, room, bed, doctor, nurse):
        self.sex_dict = None
        self.doctor_dict = None
        self.nurse_dict = None
    
        self.name = name
        self.id = id
        self.age = age
        self.weight = weight
        self.height = height
        self.sex = sex
        self.floor = floor
        self.room = room
        self.bed = bed
        self.doctor = doctor
        self.nurse = nurse

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name) -> None:
        if not isinstance(name, str):
            raise TypeError("Invalid Name!")
        self._name = name

    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, id) -> None:
        try:
            int_id = int(id)
        except ValueError:
            raise TypeError("Invalid ID! (must be number)")

        if len(str(id).strip()) != ID_LEN:
            raise ValueError(f"Invalid ID! (ID contain exactly 9 digits)")

        self._id = int_id

    @property
    def age(self) -> int:
        return self._age
    
    @age.setter
    def age(self, age) -> None:
        try:
            int_age = int(age)
        except ValueError:
            raise TypeError("Invalid Age! (must be number)")

        if int_age < MIN_AGE or int_age > MAX_AGE:
            raise ValueError(f"Invalid Age! (age should be in {MIN_AGE}-{MAX_AGE} range)")

        self._age = int_age
    
    @property
    def weight(self) -> int:
        return self._weight
    
    @weight.setter
    def weight(self, weight) -> None:
        try:
            int_weight = int(weight)
        except ValueError:
            raise TypeError("Invalid Weight! (must be number)")

        if int_weight < MIN_WEIGHT or int_weight > MAX_WEIGHT:
            raise ValueError(f"Invalid Weight! (weight should be in {MIN_WEIGHT}-{MAX_WEIGHT} range)")

        self._weight = int_weight

    @property
    def height(self) -> int:
        return self._height
    
    @height.setter
    def height(self, height) -> None:
        try:
            int_height = int(height)
        except ValueError:
            raise TypeError("Invalid Height! (must be number)")

        if int_height < MIN_HEIGHT or int_height > MAX_HEIGHT:
            raise ValueError(f"Invalid Height! (height should be in {MIN_HEIGHT}-{MAX_HEIGHT} range)")

        self._height = int_height
        
    @property
    def sex(self) -> str:
        return self._sex
    
    @sex.setter
    def sex(self, sex) -> None:
        if not isinstance(sex, str):
            raise TypeError("Invalid Sex!")

        with open("fall_prevention_web/assets/json/sex.json") as f:
            json_dict = json.load(f)
            if sex not in json_dict:
                raise TypeError("Invalid Sex!")
            
            self.sex_dict = json_dict[sex]
        self._sex = sex
        
    @property
    def floor(self) -> int:
        return self._floor
    
    @floor.setter
    def floor(self, floor) -> None:
        try:
            int_floor = int(floor)
        except ValueError:
            raise TypeError("Invalid Floor! (must be number)")

        if int_floor < MIN_FLOOR or int_floor > MAX_FLOOR:
            raise ValueError(f"Invalid Floor! (floor should be in {MIN_FLOOR}-{MAX_FLOOR} range)")

        self._floor = int_floor

    @property
    def room(self) -> int:
        return self._room
    
    @room.setter
    def room(self, room) -> None:
        try:
            int_room= int(room)
        except ValueError:
            raise TypeError("Invalid Room! (must be number)")

        if int_room < MIN_ROOM or int_room > MAX_ROOM:
            raise ValueError(f"Invalid Room! (room should be in {MIN_ROOM}-{MAX_ROOM} range)")

        self._room = int_room

    @property
    def bed(self) -> int:
        return self._bed
    
    @bed.setter
    def bed(self, bed) -> None:
        try:
            int_bed = int(bed)
        except ValueError:
            raise TypeError("Invalid Bed! (must be number)")

        if int_bed < MIN_BED or int_bed > MAX_BED:
            raise ValueError(f"Invalid Bed! (bed should be in {MIN_BED}-{MAX_BED} range)")

        self._bed = int_bed

    @property
    def doctor(self) -> str:
        return self._doctor
    
    @doctor.setter
    def doctor(self, doctor) -> None:
        if not isinstance(doctor, str):
            raise TypeError("Invalid Doctor!")

        with open("fall_prevention_web/assets/json/doctor.json") as f:
            json_dict = json.load(f)
            if doctor not in json_dict:
                raise TypeError("Invalid Doctor!")
            self.doctor_dict = json_dict[doctor]

        self._doctor = doctor

    @property
    def nurse(self) -> str:
        return self._nurse
    
    @nurse.setter
    def nurse(self, nurse) -> None:
        if not isinstance(nurse, str):
            raise TypeError("Invalid Nurse!")

        with open("fall_prevention_web/assets/json/nurse.json") as f:
            json_dict = json.load(f)
            if nurse not in json_dict:
                raise TypeError("Invalid Nurse!")
            self.nurse_dict = json_dict[nurse]

        self._nurse = nurse

    @staticmethod
    def readPatient(patient_dict: dict):
        return Patient(patient_dict["name"], patient_dict["id"], patient_dict["age"], patient_dict["weight"], patient_dict["height"],
        patient_dict["sex"], patient_dict["floor"], patient_dict["room"], patient_dict["bed"], patient_dict["doctor"], patient_dict["nurse"])

    @staticmethod
    def readPatientsJson(json_path: str) -> list:
        with open(json_path) as f:
            return [Patient.readPatient(patient) for patient in json.load(f).values()]

    def update(self, patient_form_dict: dict):
        new_patient = Patient.readPatient(patient_form_dict)
        self.__dict__.update(new_patient.__dict__)
        dic = {"1": patient_form_dict}
        with open("fall_prevention_web/assets/json/patient.json", 'w') as outfile:
            json.dump(dic, outfile)


if __name__ == '__main__':
    print("Fall Prevention Patient")
    a = Patient.readPatientsJson("fall_prevention_web/assets/json/patient.json")
    for p in a:
        for i, j in vars(p).items():
            print(f"{i}: {j}")

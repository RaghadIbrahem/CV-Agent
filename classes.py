class RSAccount:
    __username: str
    __password: str

    def signUp(self, username: str, password: str):
        pass

    def login(self, username: str, password: str):
        pass

    def __logout(self):
        pass

    def setPositionRequirement(self, positionID: int):
        pass

    def requestCandidatesList(self, positionID: int):
        pass


class Entity:
    ExtractedEntities: str = []

    def extractInformation(self):
        pass


class form:
    cvID: int
    fullName: str
    email: str
    jobTitle: str
    education: str = []
    contact: str = []
    skill: str = []
    experience: str = []
    courses: str = []
    specalizedCertificate: str = []
    achievement: str
    language: str = []

    def __init__(self, fullName, email, jobTitle, education, contact, skill,
                 experience, courses, specalizedCertificate, achievement, language):
        self.fullName = fullName
        self.email = email
        self.jobTitle = jobTitle
        self.education = education
        self.contact = contact
        self.skill = skill
        self.experience = experience
        self.courses = courses
        self.specalizedCertificate = specalizedCertificate
        self.achievement = achievement
        self.language = language

    def createCv(self):
        pass

    def addFullName(self):
        pass

    def addEmail(self):
        pass

    def addjobtitle(self):
        pass

    def addEducation(self):
        pass

    def addContact(self):
        pass

    def addSkill(self):
        pass

    def addExperience(self):
        pass

    def addCourses(self):
        pass

    def addlanguage(self):
        pass

    def addSpecalized_certificate(self):
        pass

    def addAchievement(self):
        pass

    def displayCv(self):
        pass


class PositionRequirement:
    _positionId: int
    _positionTitle: str
    _requirements: str = []

    def _deletePosition(self):
        pass

    def _confirmPositionRequirement(self):
        pass

    def __addNewpPosition(self, positiontitle: str, _requirements: str = []) -> int:
        pass

    def __addRequirement(self, _requirements: str = []):
        pass

    def __useExistingPosition(self, positionid: int):
        pass

    def __displayExistingPosition(self):
        pass

    def __modifyRequirement(self):
        pass


class Operation(Entity):
    # unique attribute u must search how to write it
    __highLevelPriority: str = []
    __middleLevelPriority: str = []
    __lowLevelPriority: str = []
    ExtractedEntities: str = []

    def initialSort(self):
        pass

    def finalSort(self):
        pass

    def displayPriorityList(self):
        pass

    def matching(self):
        pass


class Email:
    __emailsOfRejected: str = []
    __emailsOfAccepted: str = []

    def sendemail(self, rejectionEmailDescription: str):
        pass


class InitialAcceptanceEmail(Email):
    __initialAcceptanceEmailDescription: str

    def sendemail1(self, emailsOfAccepted: str = []):
        pass


class RejectionEmail(Email):
    __rejectionEmailDescription: str

    def sendemail2(self, emailsOfRejected: str = []):
        pass


object1 = InitialAcceptanceEmail()
object2 = RejectionEmail()
object1.sendemail()
object1.sendemail1()
object2.sendemail()
object2.sendemail2()

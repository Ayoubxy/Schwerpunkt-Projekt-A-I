class Student:
    def __init__(self, name, matrikelnummer, studiengang, startdatum, credits):
        self.name = name
        self.matrikelnummer = matrikelnummer
        self.studiengang = studiengang
        self.startdatum = startdatum
        self.credits = credits

    def to_dict(self):
        return {
            "name": self.name,
            "matrikelnummer": self.matrikelnummer,
            "studiengang": self.studiengang,
            "startdatum": self.startdatum,
            "credits": self.credits
        }

students = [
    Student("Anna Schmidt", "123456", "Informatik", "2022-04-01", 180),
    Student("Max Müller", "234567", "Wirtschaft", "2021-10-01", 210),
    Student("Lea Becker", "345678", "Elektrotechnik", "2023-04-01", 180),
    Student("Tim Wagner", "456789", "Informatik", "2022-04-01", 180),
    Student("Lisa Hoffmann", "567890", "Wirtschaft", "2021-10-01", 210),
    Student("Jonas Keller", "678901", "Elektrotechnik", "2023-04-01", 180),
    Student("Nina Braun", "789012", "Informatik", "2022-04-01", 180),
    Student("Paul Schneider", "890123", "Wirtschaft", "2021-10-01", 210),
    Student("Mia Neumann", "901234", "Elektrotechnik", "2023-04-01", 180),
    Student("Felix Maier", "012345", "Informatik", "2022-04-01", 180),
    Student("Julia König", "112233", "Wirtschaft", "2021-10-01", 210),
    Student("Lukas Hartmann", "223344", "Elektrotechnik", "2023-04-01", 180),
    Student("Laura Frank", "334455", "Informatik", "2022-04-01", 180),
    Student("Tobias Weiß", "445566", "Wirtschaft", "2021-10-01", 210),
    Student("Sarah Busch", "556677", "Elektrotechnik", "2023-04-01", 180),
    Student("Leon Roth", "667788", "Informatik", "2022-04-01", 180),
    Student("Emily Fuchs", "778899", "Wirtschaft", "2021-10-01", 210),
    Student("David Simon", "889900", "Elektrotechnik", "2023-04-01", 180),
    Student("Sophie Albrecht", "990011", "Informatik", "2022-04-01", 180),
    Student("Jan Krüger", "101112", "Wirtschaft", "2021-10-01", 210)
    
]
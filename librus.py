import requests
from unidecode import unidecode


class Librus:
	host = "https://api.librus.pl/"
	headers = {
		"Authorization": "Basic Mjg6ODRmZGQzYTg3YjAzZDNlYTZmZmU3NzdiNThiMzMyYjE="
	}

	grades = {}
	subjects = {}
	categories = {}

	def __init__(self):
		self.make_connection()

	# Make connection and get access token
	def make_connection(self):
		r = requests.post(self.host + "OAuth/Token", data={"username": str(input("Login: ")),
														   "password": str(input("Hasło: ")),
														   "librus_long_term_token": "1",
														   "grant_type": "password"},
						  headers=self.headers)

		self.headers["Authorization"] = "Bearer " + r.json()["access_token"]

	def get_lucky_number(self):
		r = requests.get(self.host + "2.0/LuckyNumbers", headers=self.headers)
		print("Szczęśliwy numerek: " + str(r.json()["LuckyNumber"]["LuckyNumber"]))

	def get_grades(self):
		r = requests.get(self.host + "2.0/Grades", headers=self.headers)

		if not self.subjects:
			self.get_subjects()

		if not self.categories:
			self.get_categories()

		self.grades = {

		}

		"""
		grades format:
		
		grades = {
			"Subject": [
				{
					"Grade": "",
					"Weight": "",
					"Teacher": "",
					"Category": "",
				},
			],
		}
		"""

		for i in r.json()["Grades"]:
			try:
				self.grades[self.subjects[i["Subject"]["Id"]]].append({
					"Ocena": i["Grade"],
					"Waga": self.categories[i["Category"]["Id"]]["Weight"],
					"Kategoria": self.categories[i["Category"]["Id"]]["Name"],
				})
			except KeyError:
				self.grades[self.subjects[i["Subject"]["Id"]]] = [{
					"Ocena": i["Grade"],
					"Waga": self.categories[i["Category"]["Id"]]["Weight"],
					"Kategoria": self.categories[i["Category"]["Id"]]["Name"],
				}]

		print(self.grades)

	def get_subjects(self):
		r = requests.get(self.host + "2.0/Subjects", headers=self.headers)

		self.subjects = {i["Id"]: i["Name"] for i in r.json()["Subjects"]}

	def get_categories(self):
		r = requests.get(self.host + "2.0/Grades/Categories", headers=self.headers)

		for i in r.json()["Categories"]:
			try:
				self.categories[i["Id"]] = {
						"Name": i["Name"],
						"Weight": i["Weight"],
						"CountToTheAverage": i["CountToTheAverage"],
					}

			except KeyError:
				self.categories[i["Id"]] = {
						"Name": i["Name"],
						"Weight": None,
						"CountToTheAverage": i["CountToTheAverage"],
					}

	def get_lessons(self):
		r = requests.get(self.host + "2.0/Lessons", headers=self.headers)

	def get_teachers(self):
		r = requests.get(self.host + "2.0/Users", headers=self.headers)

		[print(str(teacher["Id"]) + ". " + teacher["FirstName"] + " " + teacher["LastName"]) for teacher in r.json()["Users"]]

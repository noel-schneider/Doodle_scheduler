import pandas as pd


class Integration_session:
	data = None
	ca_members = []
	new_members = []

	def __init__(self):
		self.data = self.init_data()
		self.ca_members = self.init_ca_members()
		self.new_members = self.init_new_members()


	def init_data(self):
		data = pd.read_excel("Doodle.xls", header=4)
		data = data.rename(columns={"Unnamed: 0": "name"})	
		days_columns = [str(elem) for elem in data.columns.tolist()]
		hours_columns = [str(elem) for elem in data.loc[0].values]

		for i, day in enumerate(days_columns):
			if day.startswith("Unnamed"):
				days_columns[i] = days_columns[i-1]

		data.columns = [ts + " | " + hours_columns[i] if hours_columns[i] != 'nan' else ts for i, ts in enumerate(days_columns)]
		data = data.drop(0, axis=0)
		return data


	def init_ca_members(self):
		return [CA_member(name, self.data) for name in self.data.name.unique() if "[CA]" in name]


	def init_new_members(self):
		return [m for m in self.data.name.unique() if ("[CA]" not in m and "Nombre" not in m)]


	def __str__(self):
		description = "\n#####################################################\n>>>> C.A. MEMBERS\n"
		for m in self.ca_members:
			description += m.__str__()
		description += "\n>>>> NEW MEMBERS\n{}\n#####################################################".format(self.new_members)
		return description


	def sort_ca_members(self):
		self.ca_members.sort(key=lambda x: x.nombre_de_dispos)


	def sort_potential_events(self):
		for ca_member in self.ca_members:
			ca_member.potential_events.sort(key=lambda x: (self.data[x.date].count()-1), reverse=True)


	def first_assignment(self):
		for ca_m in self.ca_members:
			for member in ca_m.potential_events[0].potential_members:
				if member in self.new_members:
					ca_m.potential_events[0].actual_members.append(member)
					self.new_members.remove(member)
					



class CA_member:
	name = None
	potential_events = []
	nombre_de_dispos = None

	def __init__(self, name, data):
		self.name = name

		data_ca_member = data[data.name == self.name]
		available_dates = [col for col in data_ca_member.columns if data_ca_member[col].values[0] == "OK"]
		
		self.potential_events = [Event(date, data) for date in available_dates]
		self.nombre_de_dispos = len(	available_dates)


	def __str__(self, events=True):
		description = "{}\n".format(self.name)
		if events:
			for event in self.potential_events:
				description += "   |-----  {} ".format(event.__str__(potential=False, actual=True))
		return description

		


class Event:
	date = None
	potential_members = []
	actual_members = []

	def __init__(self, date, data):
		self.date = date
		self.potential_members = [m for m in data[data[date] == "OK"]["name"].tolist() if "[CA]" not in m]

	def __str__(self, potential=True, actual=False):
		description = "{}".format(self.date)
		
		if potential:
			description += " --- potential members: {}".format(self.potential_members)
		if actual:
			description += " --- actual members: {}".format(self.actual_members)

		description += "\n"

		return description







session = Integration_session()

print(session)

session.sort_ca_members()

print(session)

#pd.set_option('max_columns', None)
session.sort_potential_events()

print(session)
#print(session.new_members)
session.first_assignment()
print(session)
#print(session.new_members)
#for ca_m in session.ca_members:
#	print(ca_m.new_members)

import pandas as pd


class Integration_session:
	data = None
	ca_members = []
	new_members = []

	def __init__(self):
		self.data = self.init_data()
		self.ca_members = self.init_ca_members()
		self.new_members = self.init_new_members()


	def __str__(self, actual=True, potential=False):
		description = "\n#####################################################\n>>>> C.A. MEMBERS\n"
		for m in self.ca_members:
			description += m.__str__(actual=actual, potential=potential)
		description += "\n>>>> NEW MEMBERS\n{}\n#####################################################".format(self.new_members)
		return description


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


	def sort_ca_members(self):
		self.ca_members.sort(key=lambda x: x.nombre_de_dispos)


	def sort_potential_events(self):
		for ca_member in self.ca_members:
			ca_member.potential_events.sort(key=lambda x: (self.data[x.date].count()-1), reverse=True)


	def first_assignment(self):
		for ca_m in self.ca_members:
			ca_m.potential_events[0].actual_members = [] #TODO: Comprendre pourquoi il faut ajouter cette ligne ????
			for member in ca_m.potential_events[0].potential_members:
				if member in self.new_members:
					ca_m.potential_events[0].actual_members.append(member)
					self.new_members.remove(member)

	def when_can_join(self, member_name):
		data_member = self.data[self.data.name == member_name]
		print("###########")
		print("{} can join at {}".format(member_name, [col for col in self.data.columns.values if data_member[col].values[0] == "OK"]))
		print("###########")
	

	def where_can_go(self, name):
		liste = []
		for ca in self.ca_members:
			for i in range(len(ca.potential_events)):
				if name in ca.potential_events[i].potential_members:
					liste.append((ca.name, ca.potential_events[i].date))
		#liste = [ca.name for ca in self.ca_members if name in ca.potential_events[i].potential_members for i in range(len(ca.potential_events))]
		print("###########")
		print("{} can go to:".format(name))
		for doublet in liste:
			print(" ---> {} at {}".format(doublet[0], doublet[1]))
		print("###########")
		return liste


	def add_new_member_to_event(self, member_name, ca_destination_name, specific_date):
		for ca_i, ca in enumerate(self.ca_members):
			if ca.name == ca_destination_name:
				for ev_i, event in enumerate(ca.potential_events):
					if event.date == specific_date:
						return ca_i, ev_i
		raise ValueError


	def move_to(self, member_name, ca_destination_name, specific_date):
		if member_name not in self.new_members:
			for ca in self.ca_members:
				for i, event in enumerate(ca.potential_events):
					if member_name in ca.potential_events[i].actual_members:
						ca_origin, event_index = ca, i
						break
			ca_origin.potential_events[event_index].actual_members.remove(member_name)
		else:
			self.new_members.remove(member_name)

		#ca_origin, event_index = [ca for ca in self.ca_members if member_name in ca.potential_events[0].actual_members][0]
		

		if specific_date:
			print("1111111111111")
			print(self)
			ca_i, ev_i = session.add_new_member_to_event(member_name, ca_destination_name, specific_date)
			print("eeeeeeeeeeeeeeeh", ca_i, ev_i)
			print(self.ca_members[ca_i].potential_events[ev_i].actual_members)
			self.ca_members[ca_i].potential_events[ev_i].actual_members += [member_name]
			print("222222222222222222")
			print(self)
						
			

		#ca_dest = [cam for cam in self.ca_members if cam.name == ca_destination_name][0]
		#ca_dest.potential_events[event_index].actual_members.append(member_name)
		print("{} has been moved to {}".format(member_name, ca_destination_name))


					



class CA_member:
	name = None
	potential_events = []
	nombre_de_dispos = None

	def __init__(self, name, data):
		self.name = name

		data_ca_member = data[data.name == self.name]
		available_dates = [col for col in data_ca_member.columns if data_ca_member[col].values[0] == "OK"]
		
		self.potential_events = [Event(date, data) for date in available_dates]
		self.nombre_de_dispos = len(available_dates)


	def __str__(self, events=True, potential=False, actual=True):
		description = "{}\n".format(self.name)
		if events:
			for event in self.potential_events:
				description += "   |-----  {} ".format(event.__str__(potential=potential, actual=actual))
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

session.sort_ca_members()
session.sort_potential_events()

print(session)

session.first_assignment()

print(session)

#session.where_can_go("Rodolphe")
session.where_can_go("Alex")
session.where_can_go("Martin Evrard")
session.where_can_go("Arnaud H.")
session.where_can_go("Jonathan")
session.where_can_go("Vincent")
session.where_can_go("Martin Castin")
#session.move_to("Raphael", "Dominique [CA]", "ven. 2 | 18:00 – 19:00")

print(session)

#print(session.new_members)
#for ca_m in session.ca_members:
#	print(ca_m.new_members)

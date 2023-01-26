from datetime import datetime
from itertools import chain
import pickle
import argparse
from os import startfile

class Date:

	"""Class Date"""

	def __init__(self):

		"""Set the date to the current local date and time"""

		self.date = datetime.now()

	def __repr__(self):

		"""
		Return the object representation in string format
		'{day}-{month}-{year} {hours}:{minutes}:{seconds}'
		"""

		return self.date.strftime('%d-%m-%Y %H:%M:%S')


class Task:

	"""Class Task"""

	def __init__(self, order=0, priority=None, context=None, project=None,
	 			 text=None, metadata=None):

		"""
		Constructor of the class:
		:param order: int, Order of the task
		:param priority: str, Priority of the task
		:param contect: str, Context of the task
		:param project: str, Project of the task
		:param text: str, Text of the task
		:param metadata: str, Metadata of the task
		"""

		self.order = int(order)
		self._completed = False
		self.priority = priority
		self._completionDate = False
		self._creationDate = Date()
		self.text = text
		self.context = context
		self.project = project
		self.metadata = metadata

	@property
	def completed(self):

		"""
		Property of the class. Use to call class.completed
		:return: bool, self._completed
		"""

		return self._completed

	@completed.setter
	def completed(self, value):

		"""
		Setter of the completed property
		Call set_completion_date to set the date if _completed's value is
		setted to true
		:param value: bool, Value given to the attribute when it is called by
				class.attr = value
		"""

		if self._completed != value:
			self.set_completion_date()
		self._completed = value

	def set_completion_date(self):

		"""Set a date to _completionDate"""

		self._completionDate = Date()

	def __repr__(self):

		"""Representation of the class"""

		return """---------------------------------------
	Order :           {}
	Completed :       {}
	Completion Date : {}
	Creation Date :   {}
	Priority :        {}
	Text :            {}
	Context :         {}
	Project :         {}
	Metadata :        {}
			""".format(self.order, self._completed, self._completionDate,
			self._creationDate, self.priority, self.text, self.context,
			self.project, self.metadata)


def save(dic):

	"""
	Save a dic
	:param dic: dict, Dictionary of tasks
	"""
	
	with open('data', 'wb') as f:
		my_pickler = pickle.Pickler(f)
		my_pickler.dump(dic)

def load():

	"""
	Load a dic. If it doesn't exists create it
	:return: a dictionary of tasks
	"""

	try:
		with open('data', 'rb') as f:
			pass
	except IOError:
		task_dict = {"uncompleted_task": [], "completed_task": []}
	else:
		with open('data', 'rb') as f:
			my_unpickler = pickle.Unpickler(f)
			task_dict = my_unpickler.load()

	return task_dict

def str_task(task):
	
	"""
	Format a task into a string with all attibutes if attributes
	are not None or False
	:param task: task object, a task
	:retrun: str, a string 
	"""

	liste = []
	for key, val in task.__dict__.items():
		if val is not None and val is not False and key != "order":
			if key == "_completed" and val is True:
				val = "x"
			liste.append(str(val))
	
	return " ".join(liste) 

def add(index, value):

	"""
	Add a string task into a text file. If the text file doesn't exists
	create it
	:param index: int, the index where to insert the task
	:param value: str, the string task
	"""

	try:
		with open('todo.txt'):
			pass
	except IOError:
		with open('todo.txt', 'w') as f:
			text = """###################
#   Tasks To Do   #
###################


###################
# Completed Tasks #
###################

"""
			f.write(text)

	with open('todo.txt', 'r') as f:
		contents = f.readlines()
	value = str(value) + '\n'
	contents.insert(index + 4, value)

	with open('todo.txt', 'w') as f:
		f.writelines(contents)

def modify_line(index, value):

	"""Modify a line of the text file.
	:param index: int, the index of the line to modify
	:param value: str, the new value of the new string task
	"""

	with open('todo.txt', 'r') as f:
		contents = f.readlines()

	value = str(value) + '\n'
	contents[index + 4] = value

	with open("todo.txt", "w") as f:
		 f.writelines(contents)

def del_line(index):

	"""
	Delete a line of the text file
	:param index: int, the index of the line to delete
	"""

	with open('todo.txt', 'r') as f:
		contents = f.readlines()

	del contents[index]

	with open("todo.txt", "w") as f:
		 f.writelines(contents)

def index_completed():

	"""
	Set a index 3 line after the line of the text file where is writing
	'Completed task'
	:return: int, the index
	"""

	with open("todo.txt", "r") as f:
		contents = f.readlines()

	for i, elt in enumerate(contents):
		if "Completed Tasks" in elt:
			index = i + 3

	return index

def set_order(task_list):

	"""
	Sort the list of tasks by the order key
	:param: list, the list of uncomplete task
	:return: list, the sorted list
	"""
	liste = sorted(task_list, key=lambda x:x.order)
	for i, elt in enumerate(liste):
		elt.order = i

	return liste

def search():
	pass

def main():

	"""Main program"""

	# Parse argument
	args = parse_argument()
	# Load the dict
	task_dict = load()
	task_list = task_dict["uncompleted_task"]
	completed_task_list = task_dict["completed_task"]

	# Create a task
	if args.create:
		dic = {
			"order": input("Order : "),
			"priority": input("Priority : "),
			"text": input("Text : "),
			"context": input("Context : "),
			"project": input("Project : "),
			"metadata": input("Metadata : "),
			}
		dic = {key : val for key, val in dic.items() if val != ""}
		# Create a task object
		task = Task(**dic)
		# Set order to make it not higher than the length of the list
		if task.order > len(task_list):
			task.order = len(task_list)
		# Insert the task into the list in according to is order
		task_list.insert(task.order, task)
		# Set the order so that the numbers follow each other
		for i, elt in enumerate(task_list):
			elt.order = i
		# Save the dict of tasks
		save(task_dict)
		# Add the string task to the text file
		add(task.order, str_task(task))
		
	# Display a list of tasks
	if args.listing:
		if args.listing == "c" or args.listing == "completed":
			for elt in completed_task_list:
				print(elt)
		else:
			for elt in chain(task_list, completed_task_list):
				print(elt)

	# Search a task
	if args.search:
		try:
			key, val = args.search.split("=")
		except ValueError:
			for elt in chain(task_list, completed_task_list): # chain the two lists
				if getattr(elt, args.search): # si la clé renvoi True
					print(elt)
		else:
			for elt in chain(task_list, completed_task_list):
				if val in str(getattr(elt, key)):
					print(elt)

	# End a task
	if args.end:
		text = " ".join(args.end)
		for i, elt in enumerate(task_list):
			if text in elt.text:
				task = task_list.pop(i)
				task.completed = True
				del_line(i + 4)
				task.order = "Completed"
				index = index_completed()
				add(index, str_task(task))
				completed_task_list.insert(0, task)
				print(task)
		task_list = set_order(task_list)
		save(task_dict)

	# Modify a task
	if args.modify:
		order = int(args.modify)
		if order < len(task_list):
			task = ''
			for elt in task_list:
				if order == getattr(elt, 'order'):
					task = elt
					print(task)

			if args.attributes:
				dic = {}
				for elt in args.attributes:
					value = input('{} : '.format(elt))
					if value != '':
						if elt == 'order':
							try:
								int(value)
							except ValueError as e:
								print(e, 'Order must be a positive integer')
							else:
								dic[elt] = int(value)
						else:
							dic[elt] = value
			else:
				dic = {
					"order": int(input("Order : ")),
					"priority": input("Priority : "),
					"text": input("Text : "),
					"context": input("Context : "),
					"project": input("Project : "),
					"metadata": input("Metadata : "),
				}
			for key, val in dic.items():
				if val != '':
					setattr(task, key, val)
			# MODIFIER ORDER ERREUR SI INPUT = '' INT WITH BASE 10
			modify_line(order, str_task(task))
			save(task_dict)
			print(task)
		else:
			print("Order doesn't exist please use -ls to list task and select an existing one")

	if args.open:
		startfile('todo.txt')

def parse_argument():

	"""Argument parser"""
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--create", action="store_true", 
						help="Create new task")
	parser.add_argument("-ls", "--listing", help="List all tasks",
						nargs="?", const=True)
	parser.add_argument("-s", "--search", help="Search task by key=value")
	parser.add_argument("-e", "--end", nargs="+", help='End a task')
	parser.add_argument("-m", "--modify", help='Modify a task')
	parser.add_argument("-a", "--attributes",
						choices=['order','priority', 'text', 'context',
						 		'project', 'metadata'], nargs='+',
						help="Select attributes to change")
	parser.add_argument("-o", "--open", action='store_true',
						help='Open the text file in default editor')
	return parser.parse_args()

	
if __name__ == '__main__':
	main() 

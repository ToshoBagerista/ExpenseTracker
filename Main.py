import csv, os.path, argparse, sys, json
from datetime import datetime
from tabulate import tabulate
from expense import Expense, Args

dict = {}
global file
id = 1
args = Args()
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
parser = argparse.ArgumentParser("ExpenseTracker")

def inp():
	global parser, args
	parser.add_argument("-a", "--amount", nargs="?", type=float, default=0)
	parser.add_argument("--id", nargs="?")
	parser.add_argument("-m", "--month", type=int, default=None, nargs="?")
	parser.add_argument("-d", "--description", nargs='?', type=str, default=None)
	parser.parse_args(sys.argv[2:], namespace=args)
	
def load():
	global dict, id
	info = json.load(file)
	for task in info.values():
		dict[id] = Expense(id, task['description'], task["amount"], task["date"])
		id += 1
	file.close()
	os.remove("data.json")
	
def save():
	global dict, file
	with open("data.json", "w") as file:
		json.dump({id: expense.__dict__() for (id, expense) in dict.items()}, file, indent=2)

def export():
	global dict
	if os.path.isfile("data.csv"): os.remove("data.csv")
	with open("data.csv", "w", newline='') as file:
		writer = csv.DictWriter(file, fieldnames=["id", "date", "description", "amount"])
		writer.writeheader()
		for expense in dict.values(): writer.writerow(expense.__dict__())
	
def add():
	global dict, args, id
	dict[id] = Expense(id, args.description, args.amount)
	id += 1
	
def delete():
	global dict, args
	try:
		del dict[int(args.id)]
	except KeyError:
		print("No expense found with that ID")
		
def list():
	global dict
	print(tabulate((exp.__dict__().values() for exp in dict.values()), headers=("ID", "Description", "Amount", "Date"), tablefmt='orgtbl'))
	
def update():
	global dict, args
	try: dict[int(args.id)].update(args.description, args.amount)
	except KeyError: print("No expense found with that ID")
	
def summary():
	if args.month is None: print(f"Total expenses for the year: {sum(expense.amount for expense in dict.values() if expense.date.year == datetime.now().year)}$")
	else: print(f"Total expenses for {months[args.month-1]}: {sum(expense.amount for expense in dict.values() if expense.date.month == args.month and expense.date.year == datetime.now().year)}$")
	
def main():
	global dict, file
	if len(sys.argv) < 2:
		print(f"Usage: expensetracker <operation> [<attributes>]")
		return
	inp()
	if os.path.isfile("data.json"):
		file = open("data.json", "r")
		load()
	file = open("data.json", "w")
	match(sys.argv[1]):
		case "add": add()
		case "list": list()
		case "summary": summary()
		case "delete": delete()
		case "update": update()
		case "export": export()
	save()
main()
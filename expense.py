from datetime import datetime

class Args:
    pass

class Expense:
    def __init__(self, id, description, amount = 0, date=None):
        self.id = id
        self.description = description
        self.amount = amount
        if date is None: self.date = datetime.now()
        else: self.date = datetime.strptime(date, "%d/%m/%y")

    def __dict__(self):
        return {"id": self.id, "description": self.description, "amount": self.amount, "date": str(f"{self.date :%d/%m/%y}")}

    def __str__(self):
        return f"desc: {self.description}, amount: {self.amount}, date: {self.date :%d/%m/%y}"

    def update(self, **kwargs):
        if kwargs.get('desc') is not None: self.description = kwargs["desc"]
        if kwargs.get('amount') is not None: self.amount = kwargs["amount"]
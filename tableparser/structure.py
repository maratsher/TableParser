from typing import Literal

from numpy import subtract

PLAN_TYPES = Literal["Годовой план", "Осенний семестр", "Весенний семестр"]
SEMESTR_TYPES = Literal["Осенний семестр", "Весенний семестр"]
MONTHS_TYPE = Literal[
    "сентябрь"    
    "октябрь",
    "ноябрь",
    "декабрь",
    "февраль",
    "март",
    "апрель",
    "май",
    "июнь",
    "июль",
    "август"]

PLANS = ["Годовой план", "Осенний семестр", "Весенний семестр"]

MONTHS = [
    "сентябрь",    
    "октябрь",
    "ноябрь",
    "декабрь",
    "январь",
    "февраль",
    "март",
    "апрель",
    "май",
    "июнь",
    "июль",
    "август"
]

class Cell():
    def __init__(self ,row: int, col: int, val = None):
        self.val = val
        self.row = row
        self.col = col
    
    def __add__(self, other):
        if(not isinstance(other, Cell)):
            raise TypeError("Ячейку можео пересечь только с другой ячейкой")
        else:
            return Cell(self.row, other.col)

class Week:
    def __init__(self, n_lec: int, n_prac: int) -> None:
        self.n_lec = n_lec
        self.n_prac = n_prac

class Month:
    def __init__(self, name: MONTHS_TYPE, num_week: int, weeks: list[Week],) -> None:
        self.name = name
        self.num_week = num_week
        self.weeks = weeks

class Plan:

    def __init__(self, name: PLAN_TYPES, ksd: int, lecs: int, pracs: int, labs: int) -> None:
        self.name = name
        self.ksd = ksd
        self.lecs = lecs
        self.pracs = pracs
        self.labs = labs

    def show(self):
        print(self.name, self.ksd, self.lecs, self.pracs,
              self.labs, sep="\n")


class Semestr:

    def __init__(self, name: SEMESTR_TYPES, months: list[Month]) -> None:
        self.name = name
        months = [m for m in months if len(m.weeks) != 0]
        self.months = months
        self.num_months = len(months)


    def get_months_name(self):
        return [m.name for m in self.months]

    def get_month(self, name: MONTHS_TYPE):
        for m in self.months:
            if m.name == name:
                return m

        return "Такого месяца в этом семестре нет"

class Subject:

    def __init__(self, name: str, plans: list[Plan], semestrs: list[Semestr], control_form: tuple[bool]) -> None:
        self.name = name
        self.plans = plans
        semestrs = [s for s in semestrs if len(s.months) != 0]
        self.semestrs = semestrs
        self.control_form = control_form

    def get_semestrs_list(self):
        return [sem.name for sem in self.semestrs]

    def get_semestr(self, name):
        for sem in self.semestrs:
            if(sem.name == name):
                return sem
        
    def get_plans_list(self):
        return [p.name for p in self.plans]

    def get_plan(self, name):
        for plan in self.plans:
            if(plan.name == name):
                return plan

        
        
class Table:
    
    def __init__(self, name: str, subjects: list[Subject]) -> None:
        self.name = name
        self.subjects = subjects

    def get_subjects_name(self):
        return [s.name for s in self.subjects]

    def get_subject(self, name):
        for s in self.subjects:
            if(s.name == name):
                return s

        return "Такого предмета нет"

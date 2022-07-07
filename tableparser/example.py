from parser import get_data
from pprint import pprint


data = get_data("~/Code/SummerPractic/Data/График 3 курс_01.03.01_21.xls")

pprint(data, sort_dicts=False)

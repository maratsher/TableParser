import parser

table = parser.get_table("~/Code/SummerPractic/Data/График 5 курс_01.05.01_21.xls")

parser.get_all_data(table)



print(*parser.table.get_subjects_name)

print(parser.table.get_subject("Математический практикум").get_semestr("Осенний семестр").get_month("октябрь"))

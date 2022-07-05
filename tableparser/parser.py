import pandas as pd
import numpy as np
from structure import Cell, Week, Month, Semestr, Plan, Subject, Table
from structure import PLAN_TYPES, SEMESTR_TYPES, MONTHS, PLANS

def isint(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def get_amount_classses_per_week(df: pd.DataFrame, numbers_weeks: list[Cell], 
                                 subjects_name_cells: list[Cell]) -> dict:

    amount_classes = dict()
    for c in subjects_name_cells:
        subject_line = []
        for w in numbers_weeks:
            v = c + w
            subject_line.append( ( df.iloc[v.row, v.col], df.iloc[v.row+1, v.col] ) )
        amount_classes.update({c.val:subject_line})

    return amount_classes



def get_months_dict(df: pd.DataFrame, col_line_for_s1_start: int, col_line_for_s1_end: int,
                row_line_for_s1_top: int) -> tuple[dict,list] :

    months = dict()
    for m in MONTHS:
        months.update({m:[]})

    numbers_weeks = []
    for row in range(6, row_line_for_s1_top):
        for col in range(col_line_for_s1_start, col_line_for_s1_end):
            if(df.iloc[row, col] is np.nan):
                continue
            numbers_weeks.append(Cell(row, col, df.iloc[row, col]))
        if(len(numbers_weeks) == col_line_for_s1_end - col_line_for_s1_start -1):
            break
        else:
            numbers_weeks = []

    key = ""
    m_weeks = []
    for c in numbers_weeks:
        if(df.iloc[c.row+1, c.col] in months.keys()):
            months.update({key:m_weeks})
            m_weeks = []
            key = df.iloc[c.row+1, c.col]
        m_weeks.append(c)
        if(c.col == col_line_for_s1_end - 1):
            months.update({key:m_weeks})
        
    return (months, numbers_weeks)


def get_subject_name_cells(df: pd.DataFrame,rows: int, col_num = 0 ) -> list[Cell]:
    subjects_name_cells = []
    numbers = []
    for row in range(rows):
        val = df.iloc[row, col_num] 
        if(val in numbers):
            df.loc[row,:] = np.nan
            val = np.nan
        if((not val is np.nan) and isint(val)):
            subjects_name_cells.append(Cell(row, 1, df.iloc[row, 1]))
            numbers.append(df.iloc[row, 0])
    return subjects_name_cells

def get_plans(df: pd.DataFrame, rows: int, columns: int,
              subjects_name_cells: list[Cell]) -> tuple[list[Cell], tuple[list, list, list, list]]:

    #Получение опорных точек с значением КСР
    ref_points_plan = []
    for row in range(1, rows):
        for col in range(1, columns):
            val = df.iloc[row, col]
            if(val == "КСР"):
                ref_points_plan.append(Cell(row, col, val))

    #Получение общих количества лаб/практик/лаб за год и за каждый семестр
    ksrs = []
    lecs = []
    pracs = []
    labs = []

    i = 0
    for p in ref_points_plan:
        ksrs.append([])
        lecs.append([])
        pracs.append([])
        labs.append([])
        for r in subjects_name_cells:
            v = r+p
            v.val = df.iloc[v.row, v.col]
            ksrs[i].append(v)
            
            lec_v = df.iloc[v.row, v.col+1]
            lecs[i].append(Cell(v.row, v.col+1, lec_v))
            
            if(df.iloc[v.row, v.col+2] is np.nan):
                prac_v = df.iloc[v.row+1, v.col+2]
                pracs[i].append(Cell(v.row+1, v.col+2, prac_v))
            else:
                prac_v = df.iloc[v.row, v.col+2]
                pracs[i].append(Cell(v.row, v.col+2, prac_v))
            
            if(df.iloc[v.row, v.col+3] is np.nan):
                lab_v = df.iloc[v.row+1, v.col+3]
                labs[i].append(Cell(v.row+1, v.col+3, lab_v))
            else:
                lab_v = df.iloc[v.row, v.col+3]
                labs[i].append(Cell(v.row, v.col+3, lab_v))
         
        i+=1 

    return ref_points_plan, (ksrs, lecs, pracs, labs)

def get_name(df: pd.DataFrame, columns: int):
    for col in range(columns):
        val = df.iloc[1, col]
        if(not val is np.nan):
            return val


def get_table(file_name: str):
    df = pd.read_excel(file_name,engine='xlrd')
    # Очистить строки и столбцы, которые полностью пустые
    # df = df.dropna(how='all')
    two_sem = False

    # Кол-во строк и столбов в нашей таблице
    rows = df.shape[0]
    columns = df.shape[1]

    #Получение имени таблицы
    table_name = get_name(df, columns)

    # Получение ячеек, где хроняться все названия предметов
    subjects_name_cells = get_subject_name_cells(df, rows)


    ref_points_plan, plans = get_plans(df, rows, columns, subjects_name_cells)
    if(len(ref_points_plan) == 3):
        two_sem = True

    #Получение ячеек с номeрами недель для перво
    col_line_for_s1_start = ref_points_plan[0].col+3
    col_line_for_s1_end = ref_points_plan[1].col
    row_line_for_s1_top = subjects_name_cells[0].row


    month_for_s1, numbers_weeks_s1 = get_months_dict(df, col_line_for_s1_start, col_line_for_s1_end,
                                   row_line_for_s1_top)



    amount_classes_s1 = get_amount_classses_per_week(df, numbers_weeks_s1,
                                                     subjects_name_cells)


    if(two_sem):
        col_line_for_s2_start = ref_points_plan[1].col+3+2
        col_line_for_s2_end = ref_points_plan[2].col
        row_line_for_s2_top = subjects_name_cells[0].row
        
        month_for_s2,numbers_weeks_s2 = get_months_dict(df, col_line_for_s2_start, col_line_for_s2_end,
                                       row_line_for_s2_top)

        amount_classes_s2 = get_amount_classses_per_week(df, numbers_weeks_s2,
                                                         subjects_name_cells)


    # контруирование классов
    plans_obj_for_subject = []
    for n_subject in range(len(subjects_name_cells)):
        name = subjects_name_cells[n_subject].val
        plans_obj_for_subject.append([])
        for type in range(len(ref_points_plan)):
            plans_obj_for_subject[n_subject].append(Plan(PLANS[type], plans[0][type][n_subject].val,
                                  plans[1][type][n_subject].val,
                                  plans[2][type][n_subject].val,
                                 plans[3][type][n_subject].val))


    month_obj_for_s1 = []
    month_obj_for_s2 = []
    weeks = []
    subjects_obj = []
    for n_subject in range(len(subjects_name_cells)):
        name_sub = subjects_name_cells[n_subject].val
        for m in range(len(MONTHS)):
            for w in month_for_s1.get(MONTHS[m]):
                t = amount_classes_s1.get(subjects_name_cells[n_subject].val)[int(w.val-1)]
                weeks.append(Week(t[0], t[1]))
            month_obj_for_s1.append(Month(MONTHS[m],
                                          len(month_for_s1.get(MONTHS[m])),
                                          weeks))
            weeks = []

        if(two_sem):
            for m in range(len(MONTHS)):
                for w in month_for_s2.get(MONTHS[m]):
                    t = amount_classes_s2.get(subjects_name_cells[n_subject].val)[int(w.val-1)]
                    weeks.append(Week(t[0], t[1]))
                month_obj_for_s2.append(Month(MONTHS[m],
                                              len(month_for_s2.get(MONTHS[m])),
                                              weeks))
                weeks = []

        subjects_obj.append(Subject(name_sub,plans_obj_for_subject[n_subject],
                [Semestr("Осенний семестр", month_obj_for_s1),
                Semestr("Весенний семестр", month_obj_for_s2)],
                (True, True)))
        month_obj_for_s1 = []
        month_obj_for_s2 = []

    return Table(table_name, subjects_obj) 
               

def get_all_data(table: Table):
    print(table.name)

    
    subs = [_ for _ in table.subjects]
    for s in subs:
        print("="*50)
        print(s.name)
        for p in s.plans:
            print(p.name)
            print("КСР: ", p.ksd)
            print("лекции: ", p.lecs)
            print("практические: ", p.pracs)
            print("лабораторные: ", p.labs)

        print("="*50)
        for sem in s.semestrs:
            print(sem.name)
            for m in sem.months:
                print(m.name)
                for w in m.weeks:
                    print(w.n_lec, end=" ")
                    print(w.n_prac)
                print("")
        print("="*50)







import pandas as pd
import numpy as np

class Cell():
    def __init__(self ,row, col, val = None):
        self.val = val
        self.row = row
        self.col = col
    
    def __add__(self, other):
        if(not isinstance(other, Cell)):
            raise TypeError("Неверная операция")
        else:
            return Cell(self.row, other.col)
        
        
def isint(val):
    try:
        int(val)
        return True
    except ValueError:
        return False



def get_data(filename: str):
    df = pd.read_excel(filename, engine='xlrd')

    rows = df.shape[0]
    columns = df.shape[1]

    subjects_name_cells = []
    numbers = []

    for row in range(rows):
        val = df.iloc[row, 0] 
        if(val in numbers):
            df.loc[row,:] = np.nan
            val = np.nan
        if((not val is np.nan) and isint(val)):
            subjects_name_cells.append(Cell(row, 1, df.iloc[row, 1]))
            numbers.append(df.iloc[row, 0])

    #Получение опорных точек с значением КСР
    ref_points_plan = []
    for row in range(1, rows):
        for col in range(1, columns):
            val = df.iloc[row, col]
            if(val == "КСР"):
                ref_points_plan.append(Cell(row, col, val))

    ref_points_sem = ref_points_plan[1:]

    #Получение общих количества лаб/практик/лаб за год и за каждый семестр
    ksrs = []
    lecs = []
    pracs = []
    labs = []
    cf_for_subjects = []

    i = 0
    for p in ref_points_sem:
        ksrs.append([])
        lecs.append([])
        pracs.append([])
        labs.append([])
        cf_for_subjects.append([])
        
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
                
            cf_for_subjects[i].append((df.iloc[v.row, v.col+4], df.iloc[v.row, v.col+5]))

        i+=1

    number_week_for_sems = []
    for n_sem in range(len(ref_points_sem)):
        col_line1 = ref_points_plan[n_sem].col+3+2*n_sem
        col_line2 = ref_points_plan[n_sem+1].col
        row_line2 = subjects_name_cells[0].row
        number_week_for_sems.append([])
        for row in range(6, row_line2):
            for col in range(col_line1, col_line2):
                if df.iloc[row, col] is np.nan:
                    continue
                number_week_for_sems[n_sem].append(Cell(row, col, df.iloc[row, col]))
            if(len(number_week_for_sems[n_sem]) == col_line2-col_line1-1):
                break
            else:
                number_week_for_sems[n_sem] = []

    subject_weeks = []
    for n_sub in subjects_name_cells:
        sems = []
        for sem in range(len(ref_points_sem)):
            weeks = []
            for n in number_week_for_sems[sem]:
                w = n_sub + n
                weeks.append( (df.iloc[w.row, w.col], df.iloc[w.row+1, w.col])  )
            sems.append(weeks)
        subject_weeks.append(sems)


    pars_data = dict()

    SEMS = ["Осенний семестр", "Весенний семестр"]

    for n_sub, sub in enumerate(subjects_name_cells, 0):
        sems_dict = dict()
        for n_sem in range(len(ref_points_sem)):
            sem_dict = dict()
            sem_dict.update({
                             "КСР":ksrs[n_sem][n_sub].val,
                             "ЛК":lecs[n_sem][n_sub].val,
                             "ПР":pracs[n_sem][n_sub].val,
                             "ЛБ": labs[n_sem][n_sub].val,
                             "Форма контроля": cf_for_subjects[n_sem][n_sub]
                            })
            for n,val in enumerate(subject_weeks[n_sub][n_sem],1):
                key = "Неделя "+str(n)
                sem_dict.update({key:val})
            
            sems_dict.update({SEMS[n_sem]:sem_dict})
        
        pars_data.update({sub.val:sems_dict})

    return pars_data



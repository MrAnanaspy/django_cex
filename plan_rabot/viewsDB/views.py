import openpyxl
from django.shortcuts import render
from .models import Appeal, TimeCosts
import datetime


def get_data(request):
    data = list(Appeal.objects.all())  # Получение всех объектов
    generate_production_plan()
    return render(request, "index.html") #, context={'data':data}


def generate_production_plan():
    # Load the workbook
    wb = openpyxl.load_workbook("viewsDB/templates/documents/exel/stata.xlsx")

    # Select the active sheet
    sheet = wb.active

    count = 1
    # Read and print the data
    for appeal in Appeal.objects.all():
        count += 1

        # add id
        sheet.cell(row=count, column=1, value=appeal.id)

        # add EAM
        sheet.cell(row=count, column=2, value=appeal.EAM.EAM)

        # add name
        sheet.cell(row=count, column=3, value=appeal.EAM.name)

        # add quantity
        sheet.cell(row=count, column=4, value=appeal.quantity)

        # add time_work
        if TimeCosts.objects.filter(appeal_id=appeal.id).exists():
            time_cost = TimeCosts.objects.get(appeal_id_id=appeal.id)
            time = time_cost.twt + time_cost.twd + time_cost.mwt + time_cost.mwd + time_cost.tmwt + time_cost.tmwd + time_cost.procurement_work
        else:
            time = 0
        sheet.cell(row=count, column=5, value=time)

        # add AWP
        sheet.cell(row=count, column=6, value=appeal.AWP)

        # косвенные затраты
        sheet.cell(row=count, column=7, value=appeal.material_price)

        # add material_price
        sheet.cell(row=count, column=8, value=0)

        #  затраты на персонал
        pers_cost = round(time * 837.83, 3)
        sheet.cell(row=count, column=8, value=pers_cost)

        #  затраты на амортизацию
        time_a = 0
        production_time = 0
        amort_prise = 230000
        if TimeCosts.objects.filter(appeal_id=appeal.id).exists():
            time_cost = TimeCosts.objects.get(appeal_id_id=appeal.id)
            time_a = time_cost.twt + time_cost.mwt + time_cost.tmwt
            for ap in Appeal.objects.filter(start_time__year=2025):
                t_c = TimeCosts.objects.get(appeal_id=ap.id)
                production_time += t_c.twt + t_c.mwt + t_c.tmwt
        amort = time_a * appeal.quantity / production_time * amort_prise
        sheet.cell(row=count, column=9, value=amort)

        #  затраты на электроэнергию
        if TimeCosts.objects.filter(appeal_id=appeal.id).exists():
            time_cost = TimeCosts.objects.get(appeal_id_id=appeal.id)
            electricity = (time_cost.twt * 30 * + time_cost.mwt * 24 + time_cost.tmwt * 30) * 1.9
            sheet.cell(row=count, column=10, value=electricity)
        else:
            sheet.cell(row=count, column=10, value=0)

        # Себестоимость
        cost_price = round((pers_cost + sheet.cell(row=count, column=10).value) / appeal.quantity + appeal.material_price, 3)
        sheet.cell(row=count, column=11, value=cost_price)

        # start_time
        sheet.cell(row=count, column=12, value=appeal.start_time)

        # end_time
        sheet.cell(row=count, column=13, value=appeal.end_time)
    wb.save("viewsDB/templates/documents/exel/stata_done.xlsx")


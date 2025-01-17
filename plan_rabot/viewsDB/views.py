import os
from django.conf import settings
from django.http import HttpResponse, Http404
import openpyxl
from django.shortcuts import render
from openpyxl.styles import PatternFill

from .models import Appeal, TimeCosts
import datetime


def get_data(request):
    generate_production_plan()
    data = "media/documents/exel/stata_done.xlsx"
    return render(request, "stata.html", context={'exel':data}) #, context={'data':data}



def generate_production_plan():
    # Load the workbook
    wb = openpyxl.load_workbook("media/documents/exel/stata_done.xlsx")

    # Select the active sheet
    sheet = wb.active

    count = 1
    # Read and print the data
    for appeal in Appeal.objects.all():
        count += 1
        color = 'FFFFFF'
        if appeal.production_status == 'accept':
            color = 'FFFF00'
        elif appeal.production_status == 'in_work':
            color = '00B0F0'
        elif appeal.production_status == 'done':
            color = '00D050'

        # add id
        sheet.cell(row=count, column=1, value=appeal.id)
        sheet.cell(row=count, column=1).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        # add EAM
        sheet.cell(row=count, column=2, value=appeal.EAM.EAM)
        sheet.cell(row=count, column=2).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        # add name
        sheet.cell(row=count, column=3, value=appeal.EAM.name)
        sheet.cell(row=count, column=3).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        # add quantity
        sheet.cell(row=count, column=4, value=appeal.quantity)
        sheet.cell(row=count, column=4).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        # add time_work
        if TimeCosts.objects.filter(appeal_id=appeal.id).exists():
            time_cost = TimeCosts.objects.get(appeal_id_id=appeal.id)
            time = time_cost.twt + time_cost.twd + time_cost.mwt + time_cost.mwd + time_cost.tmwt + time_cost.tmwd + time_cost.procurement_work
        else:
            time = 0
        sheet.cell(row=count, column=5, value=time)
        sheet.cell(row=count, column=5).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        # add material_price
        sheet.cell(row=count, column=6, value=appeal.material_price)
        sheet.cell(row=count, column=6).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        # косвенные затраты
        sheet.cell(row=count, column=7, value=0)
        sheet.cell(row=count, column=7).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        #  затраты на персонал
        pers_cost = round(time * 837.83, 3)
        sheet.cell(row=count, column=8, value=pers_cost)
        sheet.cell(row=count, column=8).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

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
        sheet.cell(row=count, column=9).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        #  затраты на электроэнергию
        if TimeCosts.objects.filter(appeal_id=appeal.id).exists():
            time_cost = TimeCosts.objects.get(appeal_id_id=appeal.id)
            electricity = (time_cost.twt * 30 * + time_cost.mwt * 24 + time_cost.tmwt * 30) * 1.9
            sheet.cell(row=count, column=10, value=electricity)
        else:
            sheet.cell(row=count, column=10, value=0)
        sheet.cell(row=count, column=10).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        # Себестоимость
        cost_price = round((pers_cost + electricity) / appeal.quantity + appeal.material_price, 3)
        sheet.cell(row=count, column=11, value=cost_price)
        sheet.cell(row=count, column=11).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        # start_time
        if appeal.start_time is not None:
            sheet.cell(row=count, column=12, value=appeal.start_time)
        else:
            sheet.cell(row=count, column=12, value=datetime.date.today())
        sheet.cell(row=count, column=12).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        # end_time
        if appeal.end_time is not None:
            sheet.cell(row=count, column=13, value=appeal.end_time)
        else:
            sheet.cell(row=count, column=13, value=datetime.date.today())
        sheet.cell(row=count, column=13).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

    wb.save("media/documents/exel/stata_done.xlsx")


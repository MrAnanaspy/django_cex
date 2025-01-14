from sys import executable
from django import forms
from django.db import models
from multiselectfield import MultiSelectField

def image_directory_path(instance, filename):
    return '{0}/img/{1}'.format(instance.EAM, filename)


def model_directory_path(instance, filename):
    return '{0}/model/{1}'.format(instance.EAM, filename)


def plan_directory_path(instance, filename):
    return '{0}/plan/{1}'.format(instance.EAM, filename)


def route_map_directory_path(instance, filename):
    return '{0}/route_map/{1}'.format(instance.EAM, filename)


def testing_act_directory_path(instance, filename):
    return '{0}/testing_act/{1}'.format(instance.EAM, filename)


def solid_cam_project_directory_path(instance, filename):
    return '{0}/solid_cam_project/{1}'.format(instance.EAM, filename)


class Detail(models.Model):
    EAM = (models.CharField
           (max_length=20, primary_key=True))
    name = (models.CharField
            (max_length=100, verbose_name='Название', null=True, blank=True))
    material = (models.CharField
                (max_length=30, verbose_name='Материал', null=True, blank=True))
    size = (models.IntegerField
            (null=True, blank=True, verbose_name='Размер заготовки в мм'))
    AWP = (models.IntegerField
           (verbose_name="Средневзвешенная цена", null=True, blank=True))
    photo = (models.ImageField
             (max_length=260, verbose_name='Ссылка на фото', upload_to=image_directory_path, null=True, blank=True))
    model = (models.FileField
             (max_length=260, verbose_name='Ссылка на модель', upload_to=model_directory_path, null=True, blank=True))
    plan = (models.FileField
            (max_length=260, verbose_name='Ссылка на чертеж', upload_to=plan_directory_path, null=True, blank=True))
    route_map = (models.FileField
                 (max_length=260, verbose_name='Ссылка на маршрутный лист', upload_to=route_map_directory_path, null=True, blank=True))
    testing_act = (models.FileField
                   (max_length=260, verbose_name='Ссылка на акт тестирования', upload_to=testing_act_directory_path, null=True, blank=True))
    solid_cam_project = (models.FileField
                         (max_length=260, verbose_name='Ссылка на SolidCam проэкт', upload_to=solid_cam_project_directory_path,
                             null=True, blank=True))
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.EAM} - {self.name}"

    class Meta:
        db_table = "Detail"
        verbose_name_plural = 'Детали'


class Materials(models.Model):
    SHAPE = (
        ('circle ', 'круг'),
        ('square ', 'квадрат'),
        ('sheet ', 'лист'),
        ('hexagon ', 'шестигранник'),
        ('pipe ', 'труба'),
        ('corner ', 'уголок')
    )
    #Переделать на отдельную БД
    name = (models.CharField
            (max_length=100, verbose_name='Наименование', null=True, blank=True))
    brand = (models.CharField
             (max_length=100, verbose_name='Марка', null=True, blank=True))
    shape = (models.CharField
             (max_length=30, choices=SHAPE, verbose_name='Форма материала', null=True, blank=True))
    width = (models.IntegerField
             (verbose_name='Ширина/Диаметр в мм', null=True, blank=True))
    long = (models.IntegerField
            (verbose_name='Длинна в мм', null=True, blank=True))
    height = (models.IntegerField
              (verbose_name='Толщина в мм', null=True, blank=True))
    certificate = (models.CharField
                   (max_length=50, verbose_name='№ сертификата', null=True, blank=True))
    melting = (models.CharField
               (max_length=50, verbose_name='№ плавки', null=True, blank=True))
    party = (models.CharField
             (max_length=50, verbose_name='№ партии', null=True, blank=True))
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.shape}: {self.name}. № Партии:{self.party} "

    class Meta:
        db_table = "Materials"
        verbose_name_plural = 'Материалы'


class Materials3D(models.Model):
    TECHNOLOGY = (
        ('FDM ', 'FDM'),
        ('SLA', 'SLA'),
    )
    name = models.CharField(max_length=50, verbose_name='Обозначение', primary_key=True)
    printing_technology = models.CharField(max_length=50, choices=TECHNOLOGY, verbose_name='Технология', null=True,
                                           blank=True)
    quantity = models.IntegerField(verbose_name='Количество в кг/л', null=True, blank=True)
    link = models.URLField(verbose_name='Ссылка на материал', null=True, blank=True)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.printing_technology}"

    class Meta:
        db_table = "Materials3D"
        verbose_name_plural = 'Материалы 3Д'


class Equipment(models.Model):
    designation = models.CharField(max_length=100, verbose_name='Обозначение', primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Наименование', null=True, blank=True)
    type = models.CharField(max_length=50, verbose_name='Тип', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='кол-во', null=True, blank=True)
    price = models.IntegerField(verbose_name='Стоимость в рублях', null=True, blank=True)
    link = models.URLField(verbose_name='Ссылка на инструмент', null=True, blank=True)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.name}: {self.designation}"

    class Meta:
        db_table = "Equipment"
        verbose_name_plural = 'Оборудование'


class AdditionalEexpenses(models.Model):
    designation = models.CharField(max_length=100, verbose_name='Обозначение инструмента')
    appeal_id = models.IntegerField(verbose_name='Номер заявки')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.appeal_id}: {self.designation}"

    class Meta:
        db_table = "AdditionalExpenses"
        verbose_name_plural = 'Вышедшее из строя оборудование'



class Appeal(models.Model):
    RODUCTION_STATUS = (
        ('accept', 'Принята в работу'),
        ('in_work', 'В работе'),
        ('done', 'Готово')
    )
    READY_STATUS = (
        ('material', 'Ожидание поставки материала'),
        ('equipment', 'Ожидание поставки оснастки'),
        ('document', 'Ожидание документации')
    )
    MACHINE = (
        ('milling', 'Фрезерный'),
        ('turning', 'Токарный'),
        ('turning_milling', 'Токарно фрезерный'),
        ('fdm', 'FDM принтер'),
        ('sla', 'SLA принтер'),
    )
    BRANCH = (
        ('yaroslavl', 'Пивзавод Ярпиво'),
        ('piter', 'Балтика-Санкт-Петербург'),
        ('tula', 'Тульский пивзавод'),
        ('samara', 'Балтика-Самара'),
        ('novosibirsk', 'Балтика-Новосибирск'),
        ('habarovsk', 'Балтика-Хабаровск'),
        ('rostow', 'Пивзавод Южная заря 1974'),
        ('voronej', 'Воронежский пивзавод')
    )

    EAM = models.ForeignKey(Detail, on_delete=models.CASCADE, verbose_name='Деталь')
    quantity = (models.IntegerField(verbose_name='Количество'))
    responsible_client = (models.CharField
                          (max_length=30, verbose_name='Ответственный заказчик и контактная информация'))
    branch = (models.CharField(max_length=30, choices=BRANCH, default='accept', verbose_name='Филиал'))
    material = models.ForeignKey(Materials, on_delete=models.CASCADE, max_length=100, verbose_name='Материал', null=True, blank=True)
    product_contact = (models.BooleanField(verbose_name='Контакт с продуктом'))
    startAppeal_time = (models.DateField(verbose_name='Время подачи заявки', null=True, blank=True))
    start_time = (models.DateField(verbose_name='Время начала изготовления', null=True, blank=True))
    end_time = (models.DateField(verbose_name='Время окончания изготовления', null=True, blank=True))
    link = (models.CharField(max_length=150, verbose_name='Ссылка на заявку', null=True, blank=True, default='/'))
    machine = (MultiSelectField(max_length=110, choices=MACHINE, verbose_name='Станок', null=True, blank=True))
    quantity_defect = (models.IntegerField(verbose_name='Брак', null=True, blank=True, default=0))
    ready_status = (MultiSelectField
                    (max_length=50, choices=READY_STATUS, default='accept', verbose_name='Ожидаем', null=True, blank=True))
    production_status = (models.CharField
                         (max_length=100, choices=RODUCTION_STATUS, verbose_name='Статус выполнения', null=True,
                          blank=True))
    material_price = (models.IntegerField
                      (verbose_name='Прямые затраты на сырье, Руб', null=True, blank=True))
    equipment_price = (models.IntegerField
                      (verbose_name='Прямые затраты на инструмент', null=True, blank=True))
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.EAM}"

    class Meta:
        db_table = "Appeal"
        verbose_name_plural = 'Заявки'


class TimeCosts(models.Model):
    appeal_id = models.OneToOneField(Appeal, on_delete = models.CASCADE, primary_key = True)
    twt = models.FloatField(max_length=30, verbose_name='Время работы токарного станка на 1 шт (мин)', null=True, blank=True)
    twd = models.FloatField(max_length=30, verbose_name='Время простоя токарного станка на 1 шт (мин)', null=True, blank=True)
    mwt = models.FloatField(max_length=30, verbose_name='Время работы фрезерного станка на 1 шт (мин)', null=True, blank=True)
    mwd = models.FloatField(max_length=30, verbose_name='Время простоя фрезерного станка на 1 шт (мин)', null=True,
                            blank=True)
    tmwt = models.FloatField(max_length=30, verbose_name='Время работы токарного-фрезерного станка на 1 шт (мин)', null=True,
                             blank=True)
    tmwd = models.FloatField(max_length=30, verbose_name='Время простоя токарно-фезерного станка на 1 шт (мин)', null=True,
                             blank=True)
    procurement_work = models.FloatField(max_length=30,
                                         verbose_name='Время потраченое на заготовительные операции (Пила, плазма, электроэррозия) 1 шт (мин)',
                                         null=True, blank=True)
    comment = models.TextField(verbose_name='Комментарий')

    class Meta:
        db_table = "TimeCosts"
        verbose_name_plural = 'Время работы станков'

from django.contrib import admin
from .models import Appeal, Detail, Materials, Materials3D, Equipment, AdditionalEexpenses, TimeCosts
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import format_html


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('id', 'EAM', 'name', 'image_tag', 'zayavka_link')
    list_filter = ('start_time', 'production_status', 'machine')

    def name(self, obj):
        if Detail.objects.filter(EAM=obj.EAM).exists():
            result = Detail.objects.get(EAM=obj.EAM).name
        else:
            result = '-'
        return result

    def image_tag(self, obj):
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.EAM.photo.url))
    image_tag.short_description = 'Фото/Рендер'
    image_tag.allow_tags = True

    def zayavka_link(self, obj):
        if obj.link and obj.link != '/':
            return format_html('<a href="{}">Ссылка на заявку</a>'.format(obj.link))
        else:
            return "Нет ссылки"
    zayavka_link.allow_tags = True
    zayavka_link.short_description = 'Ссылка'


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ('EAM', 'name', 'image_tag', 'model_link', 'plan_link')
    list_filter = ('EAM', 'name')

    def image_tag(self, obj):
        print(Detail.objects.raw("SELECT id FROM appeal"))
        return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.photo.url))
    image_tag.short_description = 'Фото/Рендер'
    image_tag.allow_tags = True

    def model_link(self, obj):
        if obj.model:
            return format_html('<a href="{}" download">Скачать модель</a>'.format(obj.model.url))
        else:
            return "Нет модели"

    model_link.allow_tags = True
    model_link.short_description = 'Модель'


    def plan_link(self, obj):
        if obj.plan:
            return format_html('<a href="{}" download">Скачать чертеж</a>'.format(obj.plan.url))
        else:
            return "Нет чертежа"

    plan_link.allow_tags = True
    plan_link.short_description = 'Чертеж'


@admin.register(Materials)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'shape', 'width', 'long', 'height', 'certificate', 'melting', 'party')
    list_filter = ('name', 'shape')


@admin.register(Materials3D)
class Material3dAdmin(admin.ModelAdmin):
    list_display = ('name', 'printing_technology', 'quantity')
    list_filter = ('name', 'printing_technology')


@admin.register(AdditionalEexpenses)
class AdditionalEexpenseAdmin(admin.ModelAdmin):
    list_display = ('designation', 'name_equip', 'name_detail', 'img_detail')

    def name_equip(self, obj):
        if Equipment.objects.filter(designation=obj.designation).exists():
            result = Equipment.objects.get(designation=obj.designation).name
        else:
            result = '-'
        return result

    name_equip.allow_tags = True
    name_equip.short_description = 'Название инструмента'

    def name_detail(self, obj):
        if Appeal.objects.filter(id=obj.appeal_id).exists():
            eam = Appeal.objects.get(id=obj.appeal_id).EAM
            result = Detail.objects.get(EAM=eam).name
        else:
            result = '-'
        return result

    name_detail.allow_tags = True
    name_detail.short_description = 'Название детали'

    def img_detail(self, obj):
        if Appeal.objects.filter(id=obj.appeal_id).exists():
            eam = Appeal.objects.get(id=obj.appeal_id).EAM
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'
                               .format(Detail.objects.get(EAM=eam).photo.url))

    img_detail.allow_tags = True
    img_detail.short_description = 'Фото/Рендер детали'


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'type', 'quantity')
    list_filter = ('name', 'type')


@admin.register(TimeCosts)
class TimeCostsAdmin(admin.ModelAdmin):
    list_display = ('name_detail', 'img_detail', 'twt', 'mwt', 'tmwt', 'procurement_work')

    def name_detail(self, obj):
        if Appeal.objects.filter(id=obj.appeal_id_id).exists():
            result = Appeal.objects.get(id=obj.appeal_id_id).EAM.name
        else:
            result = '-'
        return result

    def img_detail(self, obj):
        if Appeal.objects.filter(id=obj.appeal_id_id).exists():
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'
                               .format(Appeal.objects.get(id=obj.appeal_id_id).EAM.photo.url))

    img_detail.allow_tags = True
    img_detail.short_description = 'Фото/Рендер детали'


@receiver(post_save, sender=Detail)
def generate_data(sender, instance, created, **kwargs):
    if created:
        if not instance.photo:
            instance.photo='/zaglushka.jpg'


@receiver(post_save, sender=AdditionalEexpenses)
def delete_equip(sender, instance, created, **kwargs):
    if created:
        num = Equipment.objects.get(designation=instance.designation).quantity
        Equipment.objects.filter(designation=instance.designation).update(quantity=(num - 1))

@receiver(post_save, sender=Materials)
def add_material(sender, instance, created, **kwargs):
    if created:
        pass
from django.urls import path

from apps.equipment.views import equipment_overview_page, equipment_get, equipment_manage, equipment_delete, \
    equipment_restore

urlpatterns = [
    path("equipment", equipment_overview_page, name="equipment_list"),
    path("equipment/get", equipment_get, name="equipment_get"),
    path("equipment/manage/", equipment_manage, name="equipment_manage_create"),
    path("equipment/manage/<int:pk>", equipment_manage, name="equipment_manage_update"),
    path("equipment/delete/<int:pk>", equipment_delete, name="equipment_delete"),
    path("equipment/restore/<int:pk>", equipment_restore, name="equipment_restore"),
]

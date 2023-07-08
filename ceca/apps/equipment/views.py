import datetime
import json
import math
from functools import reduce

from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator, Page
from django.db import transaction
from django.db.models import Q, QuerySet
from django.forms import modelformset_factory, BaseModelFormSet
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils.timezone import make_aware
from typing_extensions import OrderedDict, Type

from apps.equipment.forms import EquipmentForm, PortEquipmentForm, PortEquipmentFormSet
from apps.equipment.models import Equipment, ModelEquipment, PortEquipment
from apps.equipment.serializers import EquipmentSerializer
from apps.user.utils import redirect_not_auth_user
from apps.vendor.models import Vendor


def equipment_overview_page(request: WSGIRequest) -> HttpResponse | HttpResponseRedirect:
    redirection: HttpResponseRedirect = redirect_not_auth_user(request)
    if redirection:
        return redirection

    equip_status_list: list[set] = Equipment.Status.choices

    vendor_list: QuerySet = Vendor.objects.filter(status=Vendor.Status.ACTIVATED).order_by("name").values("id", "name")

    model_list: QuerySet = ModelEquipment.objects \
        .filter(status=ModelEquipment.Status.ACTIVATED).order_by("name").values("id", "name")

    return render(request, "equipment/equipment_list.html", {
        'equip_status_list': equip_status_list,
        'vendor_list': vendor_list,
        'model_list': model_list
    })


def equipment_manage(request: WSGIRequest, pk: int = None) -> HttpResponse | HttpResponseRedirect:
    redirection: HttpResponseRedirect = redirect_not_auth_user(request)
    if redirection:
        return redirection

    equipment_edit: Equipment | None = None if pk is None else Equipment.objects.filter(id=pk).first()

    equipment_port_list: QuerySet = PortEquipment.objects.none()
    if equipment_edit is not None:
        equipment_port_list = equipment_edit.ports.order_by("id").all()

    if pk is not None and equipment_edit is None:
        messages.error(request, f"The equipment with ID '{pk}' does not exist.")
        return redirect("equipment_list")

    if equipment_edit is not None and equipment_edit.status != Equipment.Status.ACTIVATED:
        messages.error(request, f"The equipment with ID '{pk}' is not activated. It is not possible edit.")
        return redirect("equipment_list")

    equipment_form: EquipmentForm = EquipmentForm(request.POST or None, instance=equipment_edit,
                                                  user=request.user, label_suffix="")

    PortFormSet = modelformset_factory(model=PortEquipment, form=PortEquipmentForm,
                                       formset=PortEquipmentFormSet, extra=0)

    port_form_set: PortEquipmentFormSet = PortFormSet(request.POST or None, queryset=equipment_port_list)

    if request.method == 'POST':
        if not port_form_set.is_valid():
            port_form_set.custom_set_errors_msgs(request)

            return render(request, 'equipment/equipment_manage.html', {
                'equipment_form': equipment_form,
                'port_form_set': port_form_set
            })

        if not equipment_form.is_valid():
            equipment_form.custom_set_errors_msgs(request)
            return render(request, 'equipment/equipment_manage.html', {
                'equipment_form': equipment_form,
                'port_form_set': port_form_set
            })

        try:
            with transaction.atomic():
                equipment_form.save()

                for form in port_form_set:
                    form.instance.equipment = equipment_form.instance
                    form.save()

                messages.success(request, 'Equipment saved correctly')
                return redirect('equipment_list')
        except Exception as ex:
            messages.error(request, 'An unexpected error happened. Try again or contact the support')

    return render(request, 'equipment/equipment_manage.html', {
        'equipment_form': equipment_form,
        'port_form_set': port_form_set
    })


def equipment_delete(request: WSGIRequest, pk: int = None) -> HttpResponse | HttpResponseRedirect:
    redirection: HttpResponseRedirect = redirect_not_auth_user(request)
    if redirection:
        return redirection

    equipment: Equipment | None = None if pk is None else Equipment.objects.filter(id=pk).first()

    if pk is not None and equipment is None:
        messages.error(request, f"The equipment with ID '{pk}' does not exist.")
        return redirect("equipment_list")

    if equipment.status != Equipment.Status.ACTIVATED:
        messages.error(request, f"The equipment with ID '{pk}' is already disabled.")
        return redirect("equipment_list")

    equipment.status = Equipment.Status.DISABLE
    equipment.date_updated = make_aware(datetime.datetime.now())
    equipment.updated_by = request.user
    equipment.save()

    messages.success(request, f"The equipment with ID '{pk}' was disabled correctly")

    return redirect("equipment_list")


def equipment_restore(request: WSGIRequest, pk: int = None) -> HttpResponse | HttpResponseRedirect:
    redirection: HttpResponseRedirect = redirect_not_auth_user(request)
    if redirection:
        return redirection

    equipment: Equipment | None = None if pk is None else Equipment.objects.filter(id=pk).first()

    if pk is not None and equipment is None:
        messages.error(request, f"The equipment with ID '{pk}' does not exist.")
        return redirect("equipment_list")

    if equipment.status != Equipment.Status.DISABLE:
        messages.error(request, f"The equipment with ID '{pk}' is already activated.")
        return redirect("equipment_list")

    equipment.status = Equipment.Status.ACTIVATED
    equipment.date_updated = make_aware(datetime.datetime.now())
    equipment.updated_by = request.user
    equipment.save()

    messages.success(request, f"The equipment with ID '{pk}' was activated correctly")

    return redirect("equipment_list")


def equipment_get(request: WSGIRequest) -> JsonResponse | None:
    if request.method != "POST":
        return None

    body: dict = json.loads(request.body)

    filter_limit_scope: Q = build_query_filter_limit_scope(body)
    filter_search_by_text: Q = build_query_filter_search_by_text(body)

    order_by_list: list[str] = build_query_order_by(body)

    found_equipments_pagination: QuerySet = Equipment.objects\
        .select_related('model') \
        .select_related('model__vendor') \
        .select_related('model__type') \
        .select_related('created_by') \
        .select_related('updated_by') \
        .filter(filter_limit_scope & filter_search_by_text) \
        .order_by(*order_by_list)

    paginator: Paginator = Paginator(found_equipments_pagination, body["length"])

    found_equipments: Page = paginator.get_page(math.ceil(body["start"] / body["length"]) + 1)

    data: list[OrderedDict] = EquipmentSerializer(found_equipments.object_list, many=True).data

    response: dict = {
        'data': data,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
    }

    return JsonResponse(response)


def build_query_order_by(body: dict) -> list[str]:
    return list(map(
        lambda x: ("" if x["dir"].lower() == "asc" else "-") + body["columns"][x["column"]]["name"], body["order"]
    ))


def build_query_filter_search_by_text(body: dict) -> Q:
    search_text: str = body["search"]["value"].strip()

    if not search_text:
        return Q(**{f'id__isnull': False})

    query_filter: list = list()
    for col in body["columns"]:
        if col["searchable"] is False:
            continue

        query_filter.append(Q(**{f'{col["name"]}__icontains': search_text}))
        continue

    return reduce(lambda x, acc: acc | x, query_filter)


def build_query_filter_limit_scope(body: dict) -> Q:
    query_filter: list = list()
    for col in body["columns"]:
        if col["searchable"] is False:
            continue

        search_value: str | list = col["search"]["value"]
        if isinstance(search_value, str) and search_value.strip() != "":
            query_filter.append(Q(**{f'{col["name"]}__icontains': search_value}))
            continue

        if isinstance(search_value, list) and len(search_value) != 0:

            sub_filter: list = list()
            for i in search_value:
                sub_filter.append(Q(**{f'{col["name"]}__icontains': i}))

            sub_filter: Q = reduce(lambda x, acc: acc | x, sub_filter)

            query_filter.append(Q(sub_filter))

    return reduce(lambda x, acc: acc & x, query_filter)

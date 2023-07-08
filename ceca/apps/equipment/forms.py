import datetime
import re
from re import Pattern

from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.forms import HiddenInput, BaseModelFormSet
from django.utils.timezone import make_aware

from apps.equipment.models import Equipment, ModelEquipment, PortEquipment


class EquipmentForm(forms.ModelForm):
    model = forms.ModelChoiceField(
        queryset=ModelEquipment.objects.filter(status=ModelEquipment.Status.ACTIVATED).order_by("name"),
        initial=ModelEquipment.objects.filter(status=ModelEquipment.Status.ACTIVATED).order_by("name")
    )

    class Meta:
        model = Equipment
        fields = (
            'id', 'hostname', 'os_version', 'ip', 'model', 'observation', 'date_created', 'created_by', 'date_updated',
            'updated_by')
        labels = {
            'íd': 'id',
            'hostname': 'Hostname',
            'os_version': 'OS Version',
            'ip': 'IP',
            'model': 'Model',
            'observation': 'Observations'
        }

        widgets = {
            'ip': forms.TextInput(attrs={
                'data-mask': '099.099.099.099'
            }),
            'observation': forms.Textarea(attrs={'rows': '3'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EquipmentForm, self).__init__(*args, **kwargs)

        for hidden_field in ['date_created', 'created_by', 'date_updated', 'updated_by']:
            self.fields[hidden_field].widget = HiddenInput()
            self.fields[hidden_field].required = False

    def clean(self) -> dict:
        cleaned_data: dict = super().clean()

        if self.instance.id is None:
            cleaned_data["date_created"] = make_aware(datetime.datetime.now())
            cleaned_data["created_by"] = self.user
        else:
            cleaned_data["date_updated"] = make_aware(datetime.datetime.now())
            cleaned_data["updated_by"] = self.user

        return cleaned_data

    def clean_ip(self) -> str:
        ip: str = self.cleaned_data['ip']

        re_ip: Pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if not re_ip.match(ip):
            raise forms.ValidationError("The IP is not valid")

        return ip

    def custom_set_errors_msgs(self, request: WSGIRequest):
        for error in self.errors.values():
            messages.error(request, error[0])


class PortEquipmentForm(forms.ModelForm):
    class Meta:
        model = PortEquipment
        fields = ('id', 'port', 'observation', 'status')
        labels = {
            'id': 'IDDDD',
            'port': 'Port',
            'observation': 'Observation',
            'status': 'Status'
        }

    def __init__(self, *args, **kwargs):
        super(PortEquipmentForm, self).__init__(*args, **kwargs)

        for hidden_field in ('port', 'observation', 'status'):
            self.fields[hidden_field].widget = HiddenInput()
            self.fields[hidden_field].required = False


class PortEquipmentFormSet(BaseModelFormSet):
    def clean(self) -> dict:
        super(PortEquipmentFormSet, self).clean()

        ports_list: dict = dict()

        for form in self.forms:
            if form.instance.port in ports_list.keys():
                ports_list[form.instance.port] = ports_list[form.instance.port] + 1
            else:
                ports_list[form.instance.port] = 1

        duplicated_ports: str = ", ".join(map(lambda x: x[0], filter(lambda x: x[1] != 1, ports_list.items())))

        if duplicated_ports != "":
            raise ValidationError(f"The following port numbers are duplicated: {duplicated_ports}.")

    def custom_set_errors_msgs(self, request: WSGIRequest):
        for error in self._non_form_errors:
            messages.error(request, error)

        for idx, error_form in enumerate(self.errors):
            if len(error_form.keys()) == 0:
                continue

            fields_errors: str = ", ".join(map(lambda x: f"field '{x[0]}': {','.join(x[1])}", error_form.items()))

            port_number: str = self.forms[idx].instance.port
            error_msg: str = f"The port number '{port_number}' has the following errors - {fields_errors}."

            messages.error(request, error_msg)

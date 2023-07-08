function btn_search_table(event) {
    event.preventDefault()
    $('#tbl_equipments').DataTable().draw()
}

function btn_equipment_item_call_modal_delete(event) {
    tr_parent = $($(event.target).parents("tr")[0])
    if (tr_parent.attr("class").includes("child")) {
        tr_parent = tr_parent.prev()
    }

    data = $("#tbl_equipments").DataTable().row(tr_parent).data()

    if (data.status != 'A') {
        $("#modal_message_title").text("It is not possible delete an item that already is deleted")
        new bootstrap.Modal(document.getElementById('modal_message')).show()
        return
    }

    modal_message = `Confirm delete of equipment: ID '${data.id}' and port number '${data.hostname}'`

    $("#modal_delete_equipment_title").text(modal_message)
    $("#modal_delete_equipment").prop("id_delete", data.id)

    new bootstrap.Modal(document.getElementById('modal_delete_equipment')).show()
}

function btn_modal_delete_equipment_save(event) {
    id_delete = $("#modal_delete_equipment").prop("id_delete")
    call_url = url_equipment_delete.replace(/\d+/, id_delete)
    window.location.replace(call_url)
}

function btn_equipment_item_call_modal_restore(event) {
    tr_parent = $($(event.target).parents("tr")[0])
    if (tr_parent.attr("class").includes("child")) {
        tr_parent = tr_parent.prev()
    }

    data = $("#tbl_equipments").DataTable().row(tr_parent).data()

    if (data.status == 'A') {
        $("#modal_message_title").text("It is not possible restore an item that already is activated")
        new bootstrap.Modal(document.getElementById('modal_message')).show()
        return
    }

    modal_message = `Confirm restore of equipment: ID '${data.id}' and port number '${data.hostname}'`

    $("#modal_restore_equipment_title").text(modal_message)
    $("#modal_restore_equipment").prop("id_restore", data.id)

    new bootstrap.Modal(document.getElementById('modal_restore_equipment')).show()
}

function btn_modal_restore_equipment_save(event) {
    id_restore = $("#modal_restore_equipment").prop("id_restore")
    call_url = url_equipment_restore.replace(/\d+/, id_restore)
    window.location.replace(call_url)
}

$(window).on( 'resize', function () {
    $('#tbl_equipments').DataTable().columns.adjust()
} );

$(document).ready(function(){
    columns = [
        {
            name: 'id',
            data: 'id'
        },
        {
            name: 'hostname',
            data: 'hostname'
        },
        {
            name: 'ip',
            data: 'ip'
        },
        {
            name: 'model__id',
            data: 'model.id',
            visible: false
        },
        {
            name: 'model__name',
            data: 'model.name'
        },
        {
            name: 'model__vendor__id',
            data: 'model.vendor.id',
            visible: false
        },
        {
            name: 'model__vendor__name',
            data: 'model.vendor.name'
        },
        {
            name: 'updated_by__email',
            data: 'updated_by.email',
            defaultContent: ''
        },
        {
            name: 'date_updated',
            data: 'date_updated',
            defaultContent: '',
            render: function (data) {
                if(data !== null){
                    return moment(data).format('DD/MM/YYYY HH:mm')
                }else{
                    return data
                }
          }
        },
        {
            name: 'status',
            data: 'status',
            defaultContent: '',
            width: '100px',
            render: function (data) {
                if (data == 'A') {
                    return '<span class="badge text-bg-success">Activated</span>'
                } else {
                    return '<span class="badge text-bg-danger">Disabled</span>'
                }
            }
        },
        {
            name: 'custom_actions',
            data: 'custom_actions',
            defaultContent: '',
            sortable: false,
            searchable: false,
            width: '1px',
            render: function (data, type, row) {
                const specific_update_url = url_equipment_manage_update.replace(/\d+/, row.id)

                custom_actions = '<a href="' + specific_update_url + '" class="btn btn-warning btn-sm" title="Edit">\
                        <i class="bi bi-pencil-square" aria-hidden="true"></i></a>'

                if (row.status == 'A') {
                    custom_actions += '<a onclick="btn_equipment_item_call_modal_delete(event)" class="ms-1 btn btn-danger btn-sm" title="Disable">\
                        <i class="bi bi-trash-fill" aria-hidden="true"></i></a>'
                } else {
                    custom_actions += '<a onclick="btn_equipment_item_call_modal_restore(event)" class="ms-1 btn btn-success btn-sm" title="Restore">\
                        <i class="bi bi-bootstrap-reboot" aria-hidden="true"></i></a>'
                }

                return custom_actions
            }
        },
    ]

    $('#tbl_equipments').DataTable(
        {
            order: [[0, 'asc']],
            language: {
                search: 'Filter table',
                searchPlaceholder: "filter table"
            },
            scrollY: "50vh",
            stateSave: true,
            responsive: true,
            processing: true,
            serverSide: true,
            ajax: {
                url: url_equipment_get,
                type: 'POST',
                contentType: 'application/json',
                data: function (d) {
                    $("*[data-table-search-field]").each(function(idx) {
                        col_name = $(this).data("table-search-field")
                        idx = columns.indexOf(columns.find(x => x.name==col_name))
                        d.columns[idx].search.value = $("#" + this.id).val()
                    })

                    return JSON.stringify(d)
                },
                headers: {
                    'X-CSRFToken': $("#tbl_equipments > input")[0].value
                }
            },
            columns: columns,
            createdRow: function (row, data, index) {
                if (index % 2 == 0)
                    $('td', row).css('background-color', 'color-mix(in srgb, #fff4f4, transparent 30%)')
                    $('td', row).css('box-shadow', 'none')
                    $('td', row).css('border', 'none')
            },
        }
    );

    $('#tbl_equipments').on( 'page.dt', function () {$('.dataTables_scrollBody').scrollTop(0);});

});
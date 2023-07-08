function adjust_port_forms_idxs() {
    data_list = $('#tbl_ports').DataTable().data().toArray()

    $("#port_form_set > input[name=form-TOTAL_FORMS]").val(data_list.length)
    $("#port_form_set > div").remove()

    cols = ["id", "port", "observation", "status"]

    data_list.forEach((data_item, idx_data) => {
        form_add = ""

        cols.forEach( col_name => {
            value = data_item[get_column_index_by_name("tbl_ports", col_name)]
            form_add += `<input type="hidden" name="form-${idx_data}-${col_name}" value="${value}" id="id_form-${idx_data}-${col_name}">`
        })

        form_add = `<div>${form_add}</div>`
        $("#port_form_set ").append(form_add)
    })
}

function btn_save_equipment(event) {
    adjust_port_forms_idxs()
    return true
}

function btn_port_item_call_modal_delete(event) {
    tr_parent = $($(event.target).parents("tr")[0])
    if (tr_parent.attr("class").includes("child")) {
        tr_parent = tr_parent.prev()
    }

    row = $("#tbl_ports").DataTable().row(tr_parent)
    data = row.data()

    id = data[get_column_index_by_name("tbl_ports", "id")]
    port_number = data[get_column_index_by_name("tbl_ports", "port")]
    status = data[get_column_index_by_name("tbl_ports", "status")]

    if (status != 'A') {
        $("#modal_message_title").text("It is not possible delete an item that already is deleted")
        new bootstrap.Modal(document.getElementById('modal_message')).show()
        return
    }

    modal_message = `Confirm delete of port: ID '${id}' and port number '${port_number}'`

    $("#modal_delete_port_title").text(modal_message)
    $("#modal_delete_port").prop("row_delete_idx", row.index())

    new bootstrap.Modal(document.getElementById('modal_delete_port')).show()
}

function btn_modal_delete_port_save(event) {
    row_idx = $("#modal_delete_port").prop("row_delete_idx")

    data = $("#tbl_ports").DataTable().row(row_idx).data()
    id = data[get_column_index_by_name("tbl_ports", "id")]

    bootstrap.Modal.getInstance(document.getElementById('modal_delete_port')).hide()
    if (id.trim() === "") {
        $('#tbl_ports').DataTable().rows(parseInt(row_idx, 10)).remove().draw()
    } else {
        idx_status = get_column_index_by_name("tbl_ports", "status")
        idx_actions = get_column_index_by_name("tbl_ports", "actions")

        $('#tbl_ports').DataTable().cell({row:row_idx,column:idx_status}).data("D").draw()
        $('#tbl_ports').DataTable().cell({row:row_idx,column:idx_actions}).data("").draw()
    }
}

function btn_port_item_call_modal_restore(event) {
    tr_parent = $($(event.target).parents("tr")[0])
    if (tr_parent.attr("class").includes("child")) {
        tr_parent = tr_parent.prev()
    }

    row = $("#tbl_ports").DataTable().row(tr_parent)
    data = row.data()

    id = data[get_column_index_by_name("tbl_ports", "id")]
    port_number = data[get_column_index_by_name("tbl_ports", "port")]
    status = data[get_column_index_by_name("tbl_ports", "status")]

    if (status == 'A') {
        $("#modal_message_title").text("It is not possible restore an item that already is activated")
        new bootstrap.Modal(document.getElementById('modal_message')).show()
        return
    }

    modal_message = `Confirm restore of port: ID '${id}' and port number '${port_number}'`

    $("#modal_restore_port_title").text(modal_message)
    $("#modal_restore_port").prop("row_restore_idx", row.index())

    new bootstrap.Modal(document.getElementById('modal_restore_port')).show()
}

function btn_modal_restore_port_save(event) {
    row_idx = $("#modal_restore_port").prop("row_restore_idx")

    data = $("#tbl_ports").DataTable().row(row_idx).data()
    id = data[get_column_index_by_name("tbl_ports", "id")]

    bootstrap.Modal.getInstance(document.getElementById('modal_restore_port')).hide()

    idx_status = get_column_index_by_name("tbl_ports", "status")
    idx_actions = get_column_index_by_name("tbl_ports", "actions")

    $('#tbl_ports').DataTable().cell({row:row_idx,column:idx_status}).data("A").draw()
    $('#tbl_ports').DataTable().cell({row:row_idx,column:idx_actions}).data("").draw()
}

function btn_port_item_call_modal_add(event) {
    Object.freeze(["txt_modal_port_id", "txt_modal_port_port", "txt_modal_observation"]).forEach( input_name => {
        $("#" + input_name).val("")
    })

    $("#modal_add_edit_port").removeProp("row_edit_idx")

    new bootstrap.Modal(document.getElementById('modal_add_edit_port')).show()
}

function btn_port_item_call_modal_edit(event) {
    tr_parent = $($(event.target).parents("tr")[0])
    if (tr_parent.attr("class").includes("child")) {
        tr_parent = tr_parent.prev()
    }

    row_idx = $("#tbl_ports").DataTable().row(tr_parent).index()

    data = $("#tbl_ports").DataTable().row(row_idx).data()

    id = data[get_column_index_by_name("tbl_ports", "id")]
    port_number = data[get_column_index_by_name("tbl_ports", "port")]
    observation = data[get_column_index_by_name("tbl_ports", "observation")]
    status = data[get_column_index_by_name("tbl_ports", "status")]

    if (status != 'A') {
        $("#modal_message_title").text("It is not possible edit a port which is disabled")
        new bootstrap.Modal(document.getElementById('modal_message')).show()
        return
    }

    td_list =  tr_parent.children("td").toArray()

    $("#txt_modal_port_id").val(id)
    $("#txt_modal_port_port").val(port_number)
    $("#txt_modal_observation").val(observation)

    $("#modal_add_edit_port").prop("row_edit_idx", row_idx)

    new bootstrap.Modal(document.getElementById('modal_add_edit_port')).show()
}

function btn_add_edit_port_save(event) {
    event.preventDefault()

    obj_change = [
        $("#txt_modal_port_id").val(),
        $("#txt_modal_port_port").val(),
        $("#txt_modal_observation").val(),
        "A",
        ""
    ]

    bootstrap.Modal.getInstance(document.getElementById('modal_add_edit_port')).hide()

    row_idx = $("#modal_add_edit_port").prop("row_edit_idx")
    $("#modal_add_edit_port").removeProp("row_edit_idx")

    if (typeof row_idx === "undefined") {
        $('#tbl_ports').DataTable().row.add(obj_change).draw()
    } else {
        $('#tbl_ports').DataTable().row(row_idx).data(obj_change).draw();
    }
}

$(window).on('resize', function () {

    $('#tbl_ports').DataTable().columns.adjust()
} );

function get_column_index_by_name(tbl_name, column_search) {
    columns_header = $(`#${tbl_name}`).DataTable().columns().header()

    return columns_header
        .map((x, idx) => [idx, x.textContent.toLowerCase()])
        .filter(x => x[1] == column_search.toLowerCase())[0][0]
}

$("document").ready(function(){
    $('#tbl_ports').DataTable({
        order: [[0, 'asc']],
        oSearch: {
            "sSearch": "Activated"
        },
        language: {
            search: 'Filter table',
            searchPlaceholder: "filter table"
        },
        autoWidth: true,
        scrollY: "50vh",
        paging: false,
        columnDefs: [
            {
                target: 0,
                responsivePriority: 0
            },
            {
                target: 1,
                responsivePriority: 0,
                render: DataTable.render.ellipsis(30)
            },
            {
                target: 2,
                render: DataTable.render.ellipsis(30)
            },
            {
                target: 3,
                width: '1px',
                responsivePriority: 1,
                render: function (data) {
                    if (data == 'A') {
                        return '<span class="badge text-bg-success">Activated</span>'
                    } else {
                        return '<span class="badge text-bg-danger">Disabled</span>'
                    }
                }
            },
            {
                target: 4,
                width: '1px',
                sortable: false,
                searchable: false,
                responsivePriority: 1,
                render: function (data, type, row) {
                    actions = '<a onclick="btn_port_item_call_modal_edit(event)" class="btn btn-warning btn-sm" title="Edit">\
                        <i class="bi bi-pencil-square" aria-hidden="true"></i></a>'

                    if (row[get_column_index_by_name("tbl_ports", "status")] == "A") {
                        actions += '<a onclick="btn_port_item_call_modal_delete(event)" class="ms-1 btn btn-danger btn-sm" title="Disable">\
                            <i class="bi bi-trash-fill" aria-hidden="true"></i></a>'
                    } else {
                        actions += '<a onclick="btn_port_item_call_modal_restore(event)" class="ms-1 btn btn-success btn-sm" title="Restore">\
                            <i class="bi bi-bootstrap-reboot" aria-hidden="true"></i></a>'
                    }

                    return actions
                }
            },
        ],
        createdRow: function (row, data, index) {
            if (index % 2 == 0)
                $('td', row).css('background-color', 'color-mix(in srgb, #fff4f4, transparent 30%)')
                $('td', row).css('box-shadow', 'none')
                $('td', row).css('border', 'none')
        },
    });
});
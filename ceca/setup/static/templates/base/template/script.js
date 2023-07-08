$(document).ready(function () {
    $('select').each(function() {
        select = $(this)[0]

        if ("multiple" in select.attributes == false)
            return

        if ("data-multiplechoice" in select.attributes == true)
            $("#" + select.id).multiselect({
                includeSelectAllOption: true,
                enableFiltering: true,
                enableCaseInsensitiveFiltering: true,
                numberDisplayed: 1,
                maxHeight: 250
            })

            $("#" + select.id).multiselect('selectAll', false).multiselect('updateButtonText')
            return
    });
});
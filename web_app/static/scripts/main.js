jQuery(document).ready(function() {
    var max_links = 20

    $("#selectAll").click(function() {
        $('input:checkbox').not(this).prop('checked', this.checked);
    });

    $('input[name="daterange"]').daterangepicker({
        "locale": {
            "format": "DD/MM/YYYY",
            "separator": " - ",
            "applyLabel": "Aplicar",
            "cancelLabel": "Cancelar",
            "fromLabel": "Até",
            "toLabel": "De",
            "customRangeLabel": "Custom",
            "weekLabel": "S",
            "daysOfWeek": [
                "D",
                "S",
                "T",
                "Q",
                "Q",
                "S",
                "S"
            ],
            "monthNames": [
                "Janeiro",
                "Fevereiro",
                "Março",
                "Abril",
                "Maio",
                "Junho",
                "Julho",
                "Agosto",
                "Setembro",
                "Outubro",
                "Novembro",
                "Dezembro"
            ],
            "firstDay": 1
        },
        "startDate": moment(),
        "endDate": moment()
    });

    $('input[type=radio][name=frequency]').change(function() {
        if (this.value == 'monthly') {
            $("#monthlyFormGroup").show();
            $("#weeklyFormGroup").hide();
        } else {
            $("#monthlyFormGroup").hide();
            $("#weeklyFormGroup").show();
        }
    });

    $("#shouldHaveRepresentative").click(function() {
        var representativeFormIds = [
            'representativeName',
            'representativeCPF',
            'representativeEmail',
            'representativePhone',
            'representativeCell',
            'representativeStatus0',
            'representativeStatus1'
        ]

        for (var i = 0; i < representativeFormIds.length; i++) {
            $('#' + representativeFormIds[i]).prop('disabled', !this.checked);
            $('#' + representativeFormIds[i]).prop('required', this.checked);
        }
    });

    $("#addMoreLinkButton").click(function(e) {
        e.preventDefault();
        var linksList = $("#linksList");
        var num_links = linksList.children('input').length;

        if (num_links < max_links) {
            $(linksList).append(
                '<input type="text" name="link_'+(num_links+1)+'" maxlength="200" class="form-control mt-1" id="link" placeholder="URL do link" />'
            );
        }
    });

    $("#certificationInfo").hide()

    $("#show_hide_info").click(function(){
        $("#certificationInfo").toggle();
    });
});
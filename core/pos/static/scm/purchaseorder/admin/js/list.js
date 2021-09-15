var tblPurchaseOrder;
var input_daterange;

function getData(all) {
    var parameters = {
        'action': 'search',
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
    };

    if (all) {
        parameters['start_date'] = '';
        parameters['end_date'] = '';
    }

    tblPurchaseOrder = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: parameters,
            dataSrc: ""
        },
        columns: [
            { data: "id" },
            { data: "sucursal.name" },
            //{ data: "provider.name" },
            //{ data: "provider.ruc" },
            { data: "date_joined" },
            { data: "state" },
            //{ data: "subtotal" },
            //{ data: "state" },
            //{ data: "concepto" },
            { data: "id" },
        ],
        columnDefs: [{
                targets: [-2],
                class: 'text-center',
                render: function(data, type, row) {
                    if (row.state === 'Enviado') {
                        return '<span class="badge badge-warning">' + row.state + '</span>';
                    }
                    return '<span class="badge badge-success">' + row.state + '</span>';
                }
            },

            {
                targets: [-1],
                class: 'text-center',
                render: function(data, type, row) {
                    var buttons = '';
                    buttons += '<a class="btn btn-primary btn-xs btn-flat" rel="detail"><i class="fas fa-folder-open"></i></a> ';
                    buttons += '<a href="/pos/scm/purchaseorder/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                    buttons += '<a href="/pos/scm/purchaseorder/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" title= "Editar"><i class="fas fa-edit"></i></a> ';

                    return buttons;
                }
            },
        ],
        rowCallback: function(row, data, index) {

        },
        initComplete: function(settings, json) {

        }
    });
}

$(function() {

    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        });

    $('.drp-buttons').hide();

    getData(false);

    $('.btnSearch').on('click', function() {
        getData(false);
    });

    $('.btnSearchAll').on('click', function() {
        getData(true);
    });

    $('#data tbody').on('click', 'a[rel="detail"]', function() {
        $('.tooltip').remove();
        var tr = tblPurchaseOrder.cell($(this).closest('td, li')).index(),
            row = tblPurchaseOrder.row(tr.row).data();
        $('#tblInventory').DataTable({
            // responsive: true,
            // autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_detproducts',
                    'id': row.id
                },
                dataSrc: ""
            },
            scrollX: true,
            scrollCollapse: true,
            columns: [
                { data: "product.name" },
                { data: "product.category.name" },
                { data: "price" },
                { data: "cant" },
                { data: "subtotal" },
            ],
            columnDefs: [{
                    targets: [-1, -3],
                    class: 'text-center',
                    render: function(data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function(data, type, row) {
                        return data;
                    }
                }
            ]
        });
        $('#myModalDetails').modal('show');
    });
});
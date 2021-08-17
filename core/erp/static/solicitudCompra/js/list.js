$(function() {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            { "data": "position" },
            { "data": "referencia" },
            { "data": "referencia" },
            { "data": "referencia" },
            { "data": "referencia" },
            //{ "data": "referencia" },

        ],
        columnDefs: [{
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function(data, type, row) {
                var buttons = '<a href="/erp/solicitudCompra/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                buttons += '<a href="/erp/solicitudCompra/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                return buttons;
            }
        }, ],
        initComplete: function(settings, json) {

        }
    });
});
$('#data tbody')
    .on('click', 'a[rel="details"]', function() {
        var tr = tblSale.cell($(this).closest('td, li')).index();
        var data = tblSale.row(tr.row).data();
        console.log(data);

        $('#tblDet').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            //data: data.det,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_details_pedido',
                    'id': data.id
                },
                dataSrc: ""
            },
            columns: [
                { "data": "prod.name" },
                { "data": "prod.cat.name" },
                { "data": "price" },
                { "data": "cant" },
                { "data": "subtotal" },
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
                },
            ],
            initComplete: function(settings, json) {

            }
        });

        $('#myModelDet').modal('show');
    })
    .on('click', 'td.details-control', function() {
        var tr = $(this).closest('tr');
        var row = tblSale.row(tr);
        if (row.child.isShown()) {
            row.child.hide();
            tr.removeClass('shown');
        } else {
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
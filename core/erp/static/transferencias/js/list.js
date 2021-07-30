var tblSale;

function format(d) {
    console.log(d);
    var html = '<table class="table">';
    html += '<thead class="thead-dark">';
    html += '<tr><th scope="col">Producto</th>';
    html += '<th scope="col">Categoría</th>';
    html += '<th scope="col">Cantidad</th>';
    html += '</thead>';
    html += '<tbody>';
    $.each(d.det, function(key, value) {
        html += '<tr>'
        html += '<td>' + value.prod.name + '</td>'
        html += '<td>' + value.prod.cat.name + '</td>'
        html += '<td>' + value.cant + '</td>'
        html += '</tr>';
    });
    html += '</tbody>';
    return html;
}

$(function() {

    tblSale = $('#data').DataTable({
        //responsive: true,
        scrollX: true,
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
        columns: [{
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            },
            { "data": "Contacto" },
            { "data": "Operacion.name" },
            { "data": "sucorigen.name" },
            { "data": "fechaSalida" },
            { "data": "fechaPrevista" },
            { "data": "id" },
        ],
        columnDefs: [{
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function(data, type, row) {
                var buttons = '<a href="/erp/transfer/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                buttons += '<a href="/erp/transfer/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                buttons += '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                buttons += '<a href="/erp/transfer/invoice/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                return buttons;
            }
        }, ],
        initComplete: function(settings, json) {

        }
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
                        'action': 'search_details_prod',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    { "data": "prod.name" },
                    { "data": "prod.cat.name" },
                    { "data": "cant" },
                ],
                columnDefs: [{
                    targets: [-2],
                    class: 'text-center',
                    render: function(data, type, row) {
                        return data;
                    }
                }, ],
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

});
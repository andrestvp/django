//$(document).ready(() => {
//    $('tbody tr').hover(function() {
//        console.log('entralist');
//        $(this).find('td').addClass('resaltar');

//    }, function() {
//        $(this).find('td').removeClass('resaltar');
//    });
//});

//$(document).ready(function() {
//    $('#data').DataTable({
//        select: true,
//    });
//})

$(document).ready(function() {
    var table = $('#data').DataTable();

    $('#data tbody').on('click', 'tr', function() {
        //        //$(this).toggleClass('selected');
        if ($(this).hasClass('selected')) {
            //console.log('entra1');
            $(this).removeClass('selected');
            console.log('lo quita');
        } else {
            table.$('tr.selected').removeClass('selected');
            //console.log('entra4');
            $(this).addClass('selected');
            console.log('pointa');
        }
    });
});


//$(document).ready(() => {
//    $('#data tbody').hover(function() {
//        console.log('entralist');
//        $(this).find('td').addClass('resaltar');

//    }, function() {
//        $(this).find('td').removeClass('resaltar');
//    });
//});



var tblSale;

function format(d) {
    console.log(d);
    var html = '<table class="table">';
    html += '<thead class="thead-dark">';
    html += '<tr><th scope="col">Producto</th>';
    html += '<th scope="col">Categoría</th>';
    html += '<th scope="col">PVP</th>';
    html += '<th scope="col">Cantidad</th>';
    html += '<th scope="col">Subtotal</th></tr>';
    html += '</thead>';
    html += '<tbody>';
    $.each(d.det, function(key, value) {
        html += '<tr>'
        html += '<td>' + value.prod.name + '</td>'
        html += '<td>' + value.prod.cat.name + '</td>'
        html += '<td>' + value.price + '</td>'
        html += '<td>' + value.cant + '</td>'
        html += '<td>' + value.subtotal + '</td>'
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
            { "data": "cli.names" },
            { "data": "date_joined" },
            { "data": "tipo" },
            { "data": "estado" },

            { "data": "total" },
            { "data": "entrada" },
            { "data": "totalpagar" },
            { "data": "id" },
        ],
        columnDefs: [{
                targets: [-2, -3, -4],
                class: 'text-center',
                orderable: false,
                render: function(data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function(data, type, row) {
                    var buttons = '<a href="/erp/quotation/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat" title= "Eliminar"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a href="/erp/quotation/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" title= "Editar"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search" title= "Detalle de Pedido"></i></a> ';
                    buttons += '<a href="/erp/quotation/invoice/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat" title= "Cotización" ><i class="fas fa-file-pdf"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings, json) {

        }
    });


    tippy('#delete', {
        content: "I'm a Tippy tooltip!",
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

});
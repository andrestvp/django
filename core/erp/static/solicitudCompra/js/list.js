var tblSale;


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

        columns: [

            { "data": "referencia" },
            { "data": "date_joined" },
            { "data": "estadoSolicitud" },
            { "data": "sucursal" },

            { "data": "id" },
        ],
        columnDefs: [{
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function(data, type, row) {
                var buttons = '<a href="/erp/solicitudCompra/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                buttons += '<a href="/erp/solicitudCompra/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                return buttons;
            }
        }, ],
        initComplete: function(settings, json) {

        }
    });



});
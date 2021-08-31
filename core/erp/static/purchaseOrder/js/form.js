var tblProducts;
var tblSearchProducts;
var solicitud = {
    items: {
        cli: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        plazo: '',
        sucursal: '',
        referencia: '',
        centrocostos: '',
        concepto: '',


        tipo: '',
        abono: 0.00,
        totalpagar: 0.00,
        products: []
    },
    get_ids: function() {
        var ids = [];
        $.each(this.items.products, function(key, value) {
            ids.push(value.id);
        });
        return ids;
    },



    calculate_purchaseOrder: function() {
        var subtotal = 0.00;
        var totalpagar = 0.00;



        $.each(this.items.products, function(pos, dict) {
            dict.pos = pos;
            dict.subtotal = dict.cant * parseFloat(dict.standardcost);
            subtotal += dict.subtotal;
            dict.totalpagar = dict.subtotal * 0.12;


        });
        this.items.subtotal = subtotal;



    },
    add: function(item) {
        this.items.products.push(item);
        this.list();
    },
    list: function() {
        this.calculate_purchaseOrder();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                { "data": "id" },
                { "data": "full_name" },
                { "data": "stock" },
                { "data": "cant" },
                { "data": "standardcost" },
                { "data": "subtotal" },
                { "data": "totalpagar" },


            ],
            columnDefs: [{
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function(data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },


            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 100,
                    step: 1
                });

            },
            initComplete: function(settings, json) {

            }
        });
        console.clear();
        console.log(this.items);
        console.log(this.get_ids());
    },
};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    if (!Number.isInteger(repo.id)) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.full_name + '<br>' +
        '<b>Stock:</b> ' + repo.stock + '<br>' +
        '<b>Costo:</b> <span class="badge badge-warning">$' + repo.standardcost + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function() {

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#fechaPrevista').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });





    // search products
    /*$('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            console.log(vents.items);
            vents.add(ui.item);
            $(this).val('');
        }
    });*/

    $('.btnRemoveAll').on('click', function() {
        if (solicitud.items.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function() {
            solicitud.items.products = [];
            solicitud.list();
        }, function() {

        });
    });

    // event cant
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function() {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function() {
                    solicitud.items.products.splice(tr.row, 1);
                    solicitud.list();
                },
                function() {

                });
        })


    $('.btnClearSearch').on('click', function() {
        $('input[name="search"]').val('').focus();
    });

    $('.btnSearchProducts').on('click', function() {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'ids': JSON.stringify(solicitud.get_ids()),
                    'term': $('select[name="search"]').val()
                },
                dataSrc: ""
            },
            columns: [
                { "data": "full_name" },
                { "data": "image" },
                { "data": "stock" },
                { "data": "standardcost" },
                { "data": "id" },
            ],
            columnDefs: [{
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function(data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-0],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        var buttons = '<a rel="add" class="btn btn-success btn-xs btn-flat"><i class="fas fa-plus"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function(settings, json) {

            }
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody')
        .on('click', 'a[rel="add"]', function() {
            var tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            var product = tblSearchProducts.row(tr.row).data();
            product.cant = 1;
            product.subtotal = 0.00;
            solicitud.add(product);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    // event submit
    $('#frmSolicitud').on('submit', function(e) {
        e.preventDefault();

        if (solicitud.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }


        solicitud.items.date_joined = $('input[name="date_joined"]').val();
        solicitud.items.cli = $('input[name="cli"]').val();
        solicitud.items.plazo = $('select[name="plazo"]').val();
        solicitud.items.sucursal = $('select[name="sucursal"]').val();
        solicitud.items.abono = $('input[name="abono"]').val();
        solicitud.items.iva = strUser;



        console.log(solicitud.items.date_joined, 'date_joined');
        console.log(solicitud.items.referencia, 'referencia');
        console.log(solicitud.items.sucursal, 'sucursal');





        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('solicitud', JSON.stringify(solicitud.items));






        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters,
            function(response) {
                alert_action('Notificación', '¿Desea imprimir el comprobante?', function() {
                    window.open('/erp/SolicitudCompra/SolicitudCompra/pdf/' + response.id + '/', '_blank');
                    location.href = '/erp/solicitudCompra/list/';
                }, function() {
                    location.href = '/erp/solicitudCompra/list/';
                });
            });
    });

    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function(params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_autocomplete',
                    ids: JSON.stringify(solicitud.get_ids())
                }
                return queryParameters;
            },
            processResults: function(data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function(e) {
        var data = e.params.data;
        if (!Number.isInteger(data.id)) {
            return false;
        }
        data.cant = 1;
        data.subtotal = 0.00;
        solicitud.add(data);
        $(this).val('').trigger('change.select2');
    });

    // Esto se puso aqui para que funcione bien el editar y calcule bien los valores del iva. // sino tomaría el valor del iva de la base debe
    // coger el que pusimos al inicializarlo.
    solicitud.list();
});
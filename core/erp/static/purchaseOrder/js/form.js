var tblProducts;
var tblSearchProducts;
var vents = {
    items: {
        cli: '',
        plazo: '',
        date_joined: '',
        subtotal: 0.00,
        tax: '',
        total: 0.00,
        descuento: 0.00,
        tipo_pagos: '',
        products: []
    },
    get_ids: function() {
        var ids = [];
        $.each(this.items.products, function(key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    calculate_invoice: function() {
        var subtotal = 0.00;
        var descuento = $('input[name="descuento"]').val();
        var ivase = "";
        console.log("xxxx iva", ivase);
        $.each(this.items.products, function(pos, dict) {
            dict.pos = pos;
            dict.subtotal = dict.cant * parseFloat(dict.costo);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.descuento = (this.items.subtotal * (descuento / 100));
        this.items.total = this.items.subtotal - this.items.descuento;
        this.items.subtcalc = this.items.subtotal - this.items.descuento;
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="descalc"]').val(this.items.descuento.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
        $('input[name="subtcalc"]').val(this.items.subtcalc.toFixed(2));
        $('input[name="ivasel"]').val(this.items.tax);
        console.log("xxxx iva s", this.items.tax);

    },
    add: function(item) {
        this.items.products.push(item);
        this.list();
    },
    list: function() {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                { "data": "id" },
                { "data": "full_name" },
                { "data": "stock" },
                { "data": "currentcost" },
                { "data": "cant" },
                { "data": "subtotal" },
            ],
            columnDefs: [{
                    targets: [-4],
                    class: 'text-center',
                    render: function(data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
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
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
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
                    max: data.stock,
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
        '<b>PVP:</b> <span class="badge badge-warning">$' + repo.currentcost + '</span>' +
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

    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });

    $("input[name='descuento']").TouchSpin({
            min: 0,
            max: 100,
            step: 1,
            decimals: 2,
            boostat: 5,
            maxboostedstep: 10,
            postfix: '%'
        }).on('change', function() {
            vents.calculate_invoice();
            //vents.sel();
        })
        .val(0);

    // search clients


    var seleccion = function() {
        let tax = document.getElementById('tax').value;
        //let tax = document.getElementsByClassName('valor').value;

        console.log('filter changed 2', tax);
        console.log(typeof tax);
        console.log();


    }

    window.onload = function() {
        let filter = document.getElementById('tax');
        //console.log('filter changed 1', vents.items.filter);

        //filter.setAttribute('onchange', 'seleccion()');

        filter.addEventListener('change', seleccion);

    }

    //function selfuncion() {
    //    console.log('ennnn');

    //    var tax = document.getElementById("tax").value;

    //    console.log('bb', tax);
    //let tax = document.getElementById('tax');
    //let valortax = tax.value;
    //console.log('entraaa', valortax);
    // }


    $('select[name="cli"]').select2({
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
                    action: 'search_clients'
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
    });


    //$("select[name='tipo_pago']").select({
    //    min: 0,
    //    max: 100,
    //    step: 0.01,
    //    decimals: 2,
    //    boostat: 5,
    //    maxboostedstep: 10,
    //    postfix: '%'
    //}).on('change', function() {
    //    vents.calculate_invoice();
    //})
    //.val(0.12);



    //$('select[name="plazo"]').select2({
    //    theme: "bootstrap4",
    //    language: 'es',
    //    allowClear: true,
    //    ajax: {
    //        delay: 250,
    //        type: 'POST',
    //        url: window.location.pathname,
    //        data: function(params) {
    //            var queryParameters = {
    //                term: params.term,
    //                action: 'search_plazo'
    //            }
    //            return queryParameters;
    //        },
    //        processResults: function(data) {
    //            console.log(data, 'wqqw');

    //            return {
    //                results: data
    //            };
    //        },
    //    },
    //    placeholder: 'Ingrese una descripción',
    //    minimumInputLength: 1,
    //});






    $('.btnAddClient').on('click', function() {
        $('#myModalClient').modal('show');
    });

    $('#myModalClient').on('hidden.bs.modal', function(e) {
        $('#frmClient').trigger('reset');
    })

    $('#frmClient').on('submit', function(e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_client');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de crear al siguiente proveedor?', parameters,
            function(response) {
                //console.log(response);
                var newOption = new Option(response.full_name, response.id, false, true);
                $('select[name="cli"]').append(newOption).trigger('change');
                $('#myModalClient').modal('hide');
            });
    });






    $('#btnAddCorreo').click(function() {
        $('#myModalCorreo').modal('show');
    });

    $('#myModalCorreo').on('hidden.bs.modal', function(e) {
        $('#frmCorreo').trigger('reset');
    })


    $('#frmCorreo').on('submit', function(e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_correo');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de enviar el correo', parameters,
            function(response) {
                //console.log(response);
                //var newOption = new Option(response.full_name, response.id, false, true);
                //$('select[name="cli"]').append(newOption).trigger('change');
                $('#myModalCorreo').modal('hide');
            });
    });



    //changestateaaprobado
    $('#changestate1').click(function() {
        console.log('estdoooo');
        postestado();
    })

    function postestado() {
        console.log('entrados');

    };




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
        if (vents.items.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function() {
            vents.items.products = [];
            vents.list();
        }, function() {

        });
    });

    // event cant
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function() {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function() {
                    vents.items.products.splice(tr.row, 1);
                    vents.list();
                },
                function() {

                });
        })
        .on('change', 'input[name="cant"]', function() {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products[tr.row].cant = cant;
            vents.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
        });

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
                    'ids': JSON.stringify(vents.get_ids()),
                    'term': $('select[name="search"]').val()
                },
                dataSrc: ""
            },
            columns: [
                { "data": "full_name" },
                { "data": "image" },
                { "data": "stock" },
                { "data": "pvp" },
                { "data": "id" },
            ],
            columnDefs: [{
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-3],
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
                {
                    targets: [-1],
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
            vents.add(product);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    // event submit
    $('#frmSale').on('submit', function(e) {
        e.preventDefault();

        if (vents.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        vents.items.date_joined = $('input[name="date_joined"]').val();
        vents.items.plazo = $('select[name="plazo"]').val();
        console.log('entra plazo', vents.items.plazo);
        console.log('entra plazo', vents.items.tax);

        vents.items.cli = $('select[name="cli"]').val();
        console.log('entra id cli', vents.items.cli);
        vents.items.tipo_pagos = $('select[name="tipo_pagos"]').val();
        console.log('entra id tipo_pagos', vents.items.tipo_pagos);
        vents.items.tax = $('select[name="tax"]').val();
        console.log('entra id tax', vents.items.tax);





        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar esta acción?', parameters,
            function() {
                location.href = '/erp/purchase/list/';
            },
            //function(response) {
            //  alert_action('Notificación', '¿Desea imprimir el comprobante', function() {
            //    window.open('/erp/purchase/invoice/pdf/' + response.id + '/', '_blank');
            //  location.href = '/erp/purchase/list/';
            // }, function() {
            //   location.href = '/erp/purchase/list/';
            // });
            //}
        );
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
                    ids: JSON.stringify(vents.get_ids())
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
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });

    // Esto se puso aqui para que funcione bien el editar y calcule bien los valores del iva. // sino tomaría el valor del iva de la base debe
    // coger el que pusimos al inicializarlo.
    vents.list();
});
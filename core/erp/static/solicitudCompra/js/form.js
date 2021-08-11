const csrf = document.getElementById('csrfmiddlewaretoken')
var tblProducts;
var tblSearchProducts;
var solicitud = {
    items: {
        referencia: '',
        date_joined: '',
        sucursal: '',
        estado: '',
        cantidaditems: 0.00,
        products: []
    },
    get_ids: function() {
        var ids = [];
        $.each(this.items.products, function(key, value) {
            ids.push(value.id);
        });
        return ids;
    },



    /* calculate_invoice: function() {
         var subtotal = 0.00;
         //   //var iva = $('input[name="iva"]').val();
         var entrada = $('input[name="entrada"]').val();
         var asig = $('input[name="asig"]').val();
         var vapla = $('input[name="vapla"]').val();

         //var nomp = $('input[name="nomp"]').val();


         $.each(this.items.products, function(pos, dict) {
             dict.pos = pos;
             console.log('ent', dict.pos);
             dict.subtotal = dict.cant * parseFloat(dict.pvp);
             subtotal += dict.subtotal;
             console.log('sum por', subtotal);

             var temporal = 0.00;
             var sacpor = 0.00;

             temporal = dict.desc;
             console.log('valor por', temporal);
             if (temporal != 0) {
                 sacpor = parseFloat(subtotal) - parseFloat((subtotal * temporal) / 100);
                 console.log('valorconpor', sacpor);
                 dict.subtotal = parseFloat(sacpor);
                 console.log('valoasig', dict.subtotal);
                 subtotal = dict.subtotal;
                 console.log('valordelotrolado', subtotal);
             }
         });
         this.items.subtotal = subtotal;





         var e = document.getElementById("id_tax");
         var strUser = e.options[e.selectedIndex].text;
         console.log('entra fg', strUser);

         if (this.items.subtotal != 0) {
             var subt = 0.00
             var ivac = 0.00
             var nv = 0.00
             subt = this.items.subtotal;
             console.log('a s', subt);
             console.log('entra fg as', strUser);
             ivac = parseFloat((subt * strUser) / 100);
             console.log('entra i as', ivac);

             //this.items.iva = ivac;

             let input_iva = document.getElementById('ivacalc');
             input_iva.value = (ivac.toFixed(2));

             nv = parseFloat(subt) + parseFloat(ivac)
             console.log('suunv', nv);

             let input_sub = document.getElementById('id_total');
             input_sub.value = (nv.toFixed(2));
             //subt = parseFloat(valor) + parseFloat(ivac);
             //console.log('sssssuuu', subt);

             let input_tot = document.getElementById('id_totalpagar');
             input_tot.value = (nv.toFixed(2));

         }

         //let input_pvp = document.getElementById('id_subtotal');
         //let valor = input_pvp.value;
         //console.log('entra fgf', valor);

         //ivac = parseFloat((valor * strUser) / 100);
         //console.log('entra fgfg', ivac);





         // //this.items.iva = this.items.subtotal * iva;
         //console.log('ivvv', this.items.ivacalc);
         //this.items.total = this.items.subtotal + this.items.ivacalc;
         //this.items.totalpagar = this.items.total - entrada;
         //this.items.asig = 1 * entrada;
         //this.items.vapla = 1 * subtotal;

         //console.log('eeeent', this.items.cli.name);
         //console.log('eeeensantes', vents.items.cli.name);

         //this.items.nomp = this.items.cli;


         let input_pvp = document.getElementById('id_subtotal');
         let valor = input_pvp.value;
         console.log('entra fgf1', valor);

         //this.items.ent = entrada;
         //console.log('aaaasvl', this.items.totalpagar);

         //console.log('aaaasv', this.items.entrada);

         //console.log('aaaasv2', this.items.ent);



         $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
         // //$('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
         //$('input[name="total"]').val(this.items.total.toFixed(2));
         //$('input[name="totalpagar"]').val(this.items.totalpagar.toFixed(2));
         //$('input[name="ent"]').val(this.items.asig.toFixed(2));
         //$('input[name="periodo"]').val(this.items.vapla.toFixed(2));

         //$('input[name="nomp"]').val(this.items.nomp);


         //$('input[name="ent"]').val(this.items.entrada.toFixed(2));
         //console.log('eeennnn', this.items.entrada) 
















     },*/
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
                { "data": "cantidad" },
                { "data": "referencia" },
                { "data": "costo" },

            ],
            columnDefs: [{
                    //targets: [-5],
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
                    targets: [-3],
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
        '<b>Stock:</b> ' + repo.cantidad + '<br>' +
        '<b>PVP:</b> <span class="badge badge-warning">$' + repo.pvp + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}


//var el = document.getElementById('id_estado');
//var e = document.getElementById("id_tax");
//var strUser = el.options[el.selectedIndex].text;
//console.log('entra fg', strUser);
//console.log('x', strUser);
//let input_pvp = document.getElementById('id_subtotal');
//let valor = input_pvp.value;
//console.log('entra fgf', valor);
//if (el) {
//function makeReadonly() {
//if (document.getElementById('id_estado').value == 'Cancelada') {
//var e = document.getElementById('id_estado').value;
//console.log('x', e);
//document.getElementById('id_sucursal').readOnly = true;
//document.getElementById("id_sucursal").setAttribute("readonly", true);
//document.getElementById("date_joined").setAttribute("readonly", true);
// document.getElementById("id_vendedor").setAttribute("readonly", true);
//  document.getElementById("id_tipo").setAttribute("readonly", true);

//var c = document.getElementById('id_sucursal').value;
//console.log('c', c);
//} else if (document.getElementById('id_estado').value == 'Solicitud') {
//document.getElementById('id_sucursal').readOnly = false;
//      document.getElementById("id_sucursal").removeAttribute("readonly");
//    }
//}
//}
//document.getElementById('id_estado').addEventListener('change', makeReadonly);






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



    .on('change', 'input[name="cant"]', function() {
        console.clear();
        var cant = parseInt($(this).val());
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        solicitud.items.products[tr.row].cant = cant;


        $('td:eq(6)', tblProducts.row.node().html('$' + solicitud.items.products[tr.row]).subtotal.toFIxed(2))


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
                    'ids': JSON.stringify(solicitud.get_ids()),
                    'term': $('select[name="search"]').val()
                },
                dataSrc: ""
            },
            columns: [
                { "data": "full_name" },
                { "data": "image" },
                { "data": "costo" },
                { "data": "categoria" },
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

            vents.add(product);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    // event submit
    $('#frmSolicitud').on('submit', function(e) {
        e.preventDefault();

        if (solicitud.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle para su solcitud');
            return false;
        }

        solicitud.items.date_joined = $('input[name="date_joined"]').val();
        solicitud.items.referencia = $('input[name="referencia"]').val();
        solicitud.items.estado = $('select[name="estado"]').val();
        //console.log('eeeens', vents.items.cli);
        solicitud.items.sucursal = $('select[name="sucursal"]').val();
        //console.log('sucursal', solicitud.items.sucursal)



        //fd.append('suc', suc.value)
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('solicitud', JSON.stringify(solicitud.items));




        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters,
            function(response) {
                alert_action('Notificación', '¿Desea imprimir la Solicitud de Compra?', function() {
                    window.open('/erp/solicitudCompra/Solicitud/pdf/' + response.id + '/', '_blank');
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
        placeholder: 'Ingrese Nombre o Código',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function(e) {
        var data = e.params.data;
        if (!Number.isInteger(data.id)) {
            return false;
        }
        data.cant = 1;
        data.referencia = '';


        solicitud.add(data);
        $(this).val('').trigger('change.select2');
    });

    // Esto se puso aqui para que funcione bien el editar y calcule bien los valores del iva. // sino tomaría el valor del iva de la base debe
    // coger el que pusimos al inicializarlo.
    vents.list();
});


//const totalpagar = document.getElementById('totalpagar');
//const plazo = document.getElementById('plazo');
//var btnCalcularx = document.getElementById("btnCalcularx");
//const llenarTabla = document.querySelector('#tblAmort tbody');

//if (button) {
//button.onclick = function() {
//     console.log('entra funcion');
//   };
//}

//function prueba() {
//  console.log('entraaa');
//}


//if (btnCalcularx) {

//  btnCalcularx.addEventListener('click', prueba, true)
//  console.log('cuota4');

//btnCalcular.addEventListener("click", calcularCuota);

// btnCalcularx.addEventListener('click', () => {
//console.log('cuota5');

//calcularCuota(totalpagar.value, plazo.value);
//})
//}

//function calcularCuota(totalpagar, plazo) {
//  console.log('cuota7');

// let fecha = []
//let fechaActual = Date.now();
//let mes_actual = moment(fechaActual);

//let pagoCapital = 0,
//  cuota = 0;

//cuota = totalpagar * (Math.pow(1 + 1 / 100, plazo) * 1 / 100) / (Math.pow(1 + 1 / 100, plazo) - 1);

//console.log('cuota');

//console.log(cuota);

//}
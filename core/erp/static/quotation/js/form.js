const csrf = document.getElementById('csrfmiddlewaretoken')
var tblProducts;
var tblSearchProducts;
var vents = {
    items: {
        cli: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        plazo: '',
        sucursal: '',
        vendedor: '',

        tipo: '',
        entrada: 0.00,
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



    calculate_invoice: function() {
        var subtotal = 0.00;
        //   //var iva = $('input[name="iva"]').val();
        console.log('entra llamado');
        var entrada = $('input[name="entrada"]').val();
        var asig = $('input[name="asig"]').val();
        var vapla = $('input[name="vapla"]').val();

        //var nomp = $('input[name="nomp"]').val();


        $.each(this.items.products, function(pos, dict) {
            dict.pos = pos;
            console.log('ent', dict.pos);
            //document.getElementById('tval').value = 0;

            if (document.getElementById('tval').value == 0) {
                dict.pvpchange = dict.pvp;
                console.log('entraaaa111');
            } else if (document.getElementById('tval').value != 0) {
                dict.pvpchange = parseFloat(dict.pvp) - (parseFloat(dict.pvp) / 100);
                console.log('enntr22');
            }
            //dict.subtotal = dict.cant * parseFloat(dict.pvp);
            //subtotal += dict.subtotal;
            //console.log('sum por', subtotal);

            console.log('ppp', dict.full_name);
            let input_name = document.getElementById('nombprod');
            input_name.value = dict.full_name;
            console.log('tvalentran', input_name.value);

            var temporal = 0.00;
            var sacpor = 0.00;
            console.log('xxxxxxxxxx', dict.pvpchange);


            let input_tval = document.getElementById('tval');
            let aval = input_tval.value;
            console.log('tvalentra', aval);
            var dest = parseFloat(dict.pvp) - (parseFloat(dict.pvp) * (aval) / 100);
            console.log('xdesta', dict.pvp);
            console.log('xdest', dest);
            dict.pvpchange = parseFloat(dict.pvp) - (parseFloat(dict.pvp) * (aval) / 100);
            console.log('pvp', dict.pvpchange);
            dict.subtotal = dict.cant * parseFloat(dict.pvpchange);
            subtotal += dict.subtotal;
            console.log('entrasubtdict', dict.subtotal);
            console.log('entrasubnormal', subtotal);



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

            var resub = input_sub.value;
            let input_ent = document.getElementById('id_entrada');
            //input_ent.value = (nv.toFixed(2));
            var va_ent = input_ent.value

            var tent = parseFloat(resub) - parseFloat(va_ent)

            let input_tot = document.getElementById('id_totalpagar');
            input_tot.value = (tent.toFixed(2));

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



        //no seeeeee que hace aqui
        //let input_pvp = document.getElementById('id_subtotal');
        //let valor = input_pvp.value;
        //console.log('entra fgf1', valor);

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
                //{ "data": "pvp" },
                { "data": "pvpchange" },
                { "data": "cant" },
                { "data": "desc" },
                { "data": "subtotal" },
            ],
            columnDefs: [{
                    targets: [-5],
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
                // {
                //     targets: [-5],
                //     class: 'text-center',
                //     orderable: false,
                //     render: function(data, type, row) {
                //         return '$' + parseFloat(data).toFixed(2);
                //     }
                // },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return '<input type="text" name="pvpchange" class="form-control form-control-sm input-sm" autocomplete="off" value="' + '$' + (row.pvpchange).toFixed(2) + '">';
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
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return '<input type="text" name="desc" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.desc + '">';
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
                    //max: 100,
                    step: 1
                });

            },
            initComplete: function(settings, json) {

            }
        });
        //console.clear();
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

    //$("input[name='iva']").TouchSpin({
    //      min: 0,
    //      max: 100,
    //      step: 0.01,
    //      decimals: 2,
    //      boostat: 5,
    //      maxboostedstep: 10,
    //      postfix: '%'
    //  }).on('change', function() {
    //      vents.calculate_invoice();
    //      console.log('eeeens', vents.items.cli);
    //console.log('eeeent', this.items.cli);


    //})
    // .val(0.12);

    // search product


    //search vendor dependiendo de sucursal
    $('select[name="sucursal"]').on('change', function() {
        var id = $(this).val();
        var select_vendor = $('select[name="vendedor"]');
        var options = '<option value="">-----</option>';
        //alert(id);
        if (id === '') {
            select_vendor.html(options);
            return false;
        }

        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_vendor_id',
                'id': id
            },
            dataType: 'json',

        }).done(function(data) {
            console.log(data);
            if (!data.hasOwnProperty('error')) {
                //console.log(data);
                $.each(data, function(key, value) {
                    options += '<option value="' + value.id + '">' + value.name + '</option>';
                    console.log(options);
                });
                return false;
            }
            message_error(data.error);

        }).fail(function(jqHXR, textStatus, errorThrown) {
            alert(textStatus + ':' + errorThrown);

        }).always(function(data) {
            select_vendor.html(options);
            console.log(select_vendor.html(options));
        });

    });



    //pricelist

    //    $('#id_plazo').on('change', function() {

    //        console.log('entra a plazo');
    // var ivac = 0.00
    // var subt = 0.00
    // var tot = 0.00

    // var e = document.getElementById("id_tax");
    // var strUser = e.options[e.selectedIndex].text;
    // console.log('entra fg', strUser);

    // let input_pvp = document.getElementById('id_subtotal');
    // let valor = input_pvp.value;
    // console.log('entra fgf', valor);

    // ivac = parseFloat((valor * strUser) / 100);
    // console.log('entra fgfg', ivac);


    // subt = parseFloat(valor) + parseFloat(ivac);
    // console.log('sssssuuu', subt);



    // let input_iva = document.getElementById('ivacalc');
    // input_iva.value = (ivac.toFixed(2));

    // let input_sub = document.getElementById('id_total');
    // input_sub.value = (subt.toFixed(2));


    // let input_tot = document.getElementById('id_totalpagar');
    //input_tot.value = (subt.toFixed(2));



    // vents.calculate_invoice();

    //});


    //$(document).ready(function() {
    //    $('#tblAmort').DataTable({
    //        dom: 'Bfrtip',
    //        buttons: [{
    //            extend: 'pdfHtml5',
    //            download: 'open'
    //        }]
    //    });
    //});




    //search pricelist dependiendo de id_plazo
    $('select[name="plazo"]').on('change', function() {
        //vents.calculate_invoice();
        var id = $(this).val();
        //console.log('entra id', id);
        var select_vendor = $('input[name="tval"]');
        var options = '';
        var tempname = '';
        //vents.calculate_invoice();
        if (id == "" || id == null) {
            message_error('Por favor seleccione plazos de pago');
            return false;
        }
        //vents.calculate_invoice();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                //        csrfmiddlewaretoken: csrftoken,

                'action': 'search_valor',
                'id': id
            },
            dataType: 'json',
            //success: function(data) {
            //    $("#tval").html(data);
            //    console.log('entra js tval');
            //    console.log(data);
            //    console.log(tval);
            //    codigo = data.resultado;
            //    console.log('suuu', codigo);
            //    tarifa_data = data.desc[0];
            //    console.log('dataaa', tarifa_data);
            //    if (codigo == 'ok_select') {
            //        $("#tval").val(tarifa_data.desc);
            //    }
            //}
        }).done(function(data) {
            console.log(data);
            if (!data.hasOwnProperty('error')) {
                //console.log(data);
                $.each(data, function(key, value) {
                    vents.calculate_invoice();
                    options = value.desc;
                    tempname = value.name;
                    //console.log('jas', options);
                    vents.calculate_invoice();
                    vents.list();

                });
                return false;
            }
            message_error(data.error);
        }).fail(function(jqHXR, textStatus, errorThrown) {
            alert(textStatus + ':' + errorThrown);
        }).always(function(data) {
            //vents.calculate_invoice();
            let input_de = document.getElementById('tval');
            input_de.value = options;
            //let input_na = document.getElementById('tval');
            //input_na.value = tempname;
            var asigna = tempname;
            //document.getElementById('tval').value = options;
            console.log('asiiigg');
            vents.list();


            //valida texto
            console.log('lee', asigna);
            if ((asigna == "Tarjeta de Crédito en general") || (asigna == "Tarjeta de Crédito teléfonos, computación y el bosque") || (asigna == "Contado Teléfono, computación y el bosque") || (asigna == "Contado General") || (asigna == "Contado Especial 3 Meses(con entrada, clientes activos)")) {
                //if (asigna == "Tarjeta de Crédito en general") {
                console.log('entra val');
                //$('#pai').children('div').hide();
                $('#pao').children('div').hide();
                $('#pau').children('div').hide();
                $("#btnAddAmort").hide();
            } else if ((asigna != "Tarjeta de Crédito en general") || (asigna != "Tarjeta de Crédito teléfonos, computación y el bosque") || (asigna != "Contado Teléfono, computación y el bosque") || (asigna != "Contado General") || (asigna != "Contado Especial 3 Meses(con entrada, clientes activos)")) {
                $('#pao').children('div').show();
                $('#pau').children('div').show();
                $("#btnAddAmort").show();
            }


            //vents.calculate_invoice();
            //var rows = document.getElementById('tblProducts').rows;
            //console.log('x', rows);

            //$('#tblProducts tbody').on('change', 'input[name="cant"]', function() {
            //    console.log('xc');
            //    console.clear();
            //    var cant = parseInt($(this).val());
            //    var tr = tblProducts.cell($(this).closest('td, li')).index();
            //    vents.items.products[tr.row].cant = cant;

            //    vents.calculate_invoice();
            //    $('td:eq(7)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
            //$('td:eq(4)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));

            //});


        });
    });

    $('plazo').trigger('change');



    //$("#tval").trigger("change");
    //$('#tval').change(function() { alert('Do Stuff'); });

    //$('input[name="tval"]').on('change', function() {
    //$('#tval').change(function() {
    //$('#tval').change(function() {
    //    console.log('eeeen');
    //});
    //console.log('entra a otro');
    //aqui verificar
    //$.each(this.items.products, function(pos, dict) {
    //$('#tblProducts tbody').on('change', 'input[name="pvpchange"]', function() {
    //    console.log('entraaaa ooo');
    //    var cant = parseFloat($(this).val());
    //    console.log('www', cant);
    //    var tr = tblProducts.cell($(this).closest('td, li')).index();
    //    console.log('trrs', tr);
    //    var data = tblProducts.row(tr.row).data();
    //    console.log('entra d', data);
    //vents.items.products[tr.row].pvpchange = pvpchange;

    //vents.calculate_invoice();
    //$('td:eq(4)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].pvpchange.toFixed(2));
    //});

    //});







    // search clients

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
        placeholder: 'Ingrese Cédula o Nombre',
        minimumInputLength: 1,
    });


    // id_tax

    $('#id_tax').on('change', function() {
        //var select = $(this).val();
        //let input_pvp = document.getElementById('ivacalc');
        //var precio = 0.00
        //var sum = 0.00
        //console.log('entra ff', select);
        //precio = parseFloat((selectValor * 118) / 100);
        //dict.subtotal = dict.cant * parseFloat(dict.pvp);


        //this.items.total = this.items.subtotal + this.items.ivacalc;
        //$('input[name="total"]').val(this.items.total.toFixed(2));

        vents.calculate_invoice();

        var ivac = 0.00
        var subt = 0.00
        var tot = 0.00

        var e = document.getElementById("id_tax");
        var strUser = e.options[e.selectedIndex].text;
        console.log('entra fg', strUser);

        let input_pvp = document.getElementById('id_subtotal');
        let valor = input_pvp.value;
        console.log('entra fgf', valor);

        ivac = parseFloat((valor * strUser) / 100);
        console.log('entra fgfg', ivac);

        //this.items.iva = ivac;
        //$('input[name="iva"]').val(this.items.iva.toFixed(2));

        subt = parseFloat(valor) + parseFloat(ivac);
        console.log('sssssuuu', subt);



        let input_iva = document.getElementById('ivacalc');
        input_iva.value = (ivac.toFixed(2));

        let input_sub = document.getElementById('id_total');
        input_sub.value = (subt.toFixed(2));

        //var e = document.getElementById("id_entrada");
        //var strent = e.value;
        //console.log('entra fg', strent);

        //let input_tot = document.getElementById('id_totalpagar');

        //tot = parseFloat(subt) + parseFloat(strent);
        //console.log('entra tot', tot);

        //input_tot = (tot.toFixed(2));
        let input_tot = document.getElementById('id_totalpagar');
        input_tot.value = (subt.toFixed(2));




        //$('input[name="ent"]').val(this.items.asig.toFixed(2));

        //suma = parseFloat(precio) + parseFloat(selectValor);
        //console.log('valor', selectValor);

        //console.log('sacaporcentaje', precio);
        //console.log('sacaprecio', suma);
        //input_pvp.value = suma;
        //vents.calculate_invoice();

    });


    //id_entrada

    $('#id_entrada').on('change', function() {
        //var select = $(this).val();
        //let input_pvp = document.getElementById('ivacalc');
        //var precio = 0.00
        //var sum = 0.00
        //console.log('entra ff', select);
        //precio = parseFloat((selectValor * 118) / 100);
        //dict.subtotal = dict.cant * parseFloat(dict.pvp);

        var tot = 0.00


        var e = document.getElementById("id_entrada");
        var strent = e.value;
        console.log('entra fg', strent);

        let input_tot = document.getElementById('id_totalpagar');
        var e = document.getElementById("id_total");
        var strtot = e.value;
        console.log('entra tot', strtot);


        tot = parseFloat(strtot) - parseFloat(strent);
        console.log('entra tot', strtot);

        input_tot.value = (tot.toFixed(2));




        //$('input[name="ent"]').val(this.items.asig.toFixed(2));

        //suma = parseFloat(precio) + parseFloat(selectValor);
        //console.log('valor', selectValor);

        //console.log('sacaporcentaje', precio);
        //console.log('sacaprecio', suma);
        //input_pvp.value = suma;

    });





    //$('#id_estado').on('change', function() {

    // var selectValor = $(this).val();
    //  console.log('entra', selectValor);

    //    if (selectValor == "Solicitud") {
    //        console.log('entra al contado');


    //          $("#btnConfirmar").hide();


    //        } else {

    //    $("#btnConfirmar").show();


    //  }




    //});





















    // id_tipo

    $('#id_tipo').on('change', function() {
        var selectValor = $(this).val();
        console.log('entra', selectValor);
        if (selectValor == "Al Contado") {
            console.log('entra al contado');
            $('#pai').children('div').hide();
            $('#pao').children('div').hide();
            $('#pau').children('div').hide();
            $("#btnAddAmort").hide();
            //$.each(this.items.products, function(pos, dict) {
            //    dict.pos = pos;
            //    var tempsub = dict.pvp;
            //    console.log('ent', dict.pos);
            //    dict.subtotal = parseFloat(tempsub) - parseFloat((tempsub * 47) / 100);
            //    console.log('ent', dict.subtotal);
            //    dict.pvp = dict.subtotal;
            //    console.log('ent', dict.pvp);
            //});
            //$('#pai').children('#' + tax).show();
        } else {
            $('#pai').children('div').show();
            $('#pao').children('div').show();
            $('#pau').children('div').show();
            $("#btnAddAmort").show();
        }
    });





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



    //$("input[name='entrada']").TouchSpin({
    //min: 0,
    //max: 1000,
    //step: 0.01,
    //decimals: 2,
    //boostat: 5,
    //maxboostedstep: 10,
    //postfix: '$'
    // //}).on('change', function() {
    //vents.calculate_invoice();
    // // })
    //.val(50.00);



    $('#btnAddAmort').click(function() {
        //$('#enc').children('div').hide();
        //$(".ui-enc").hide();
        //$('#enc').toggleClass("hidden");
        //document.getElementById("#enc").hide();

        console.log('aqui');
        var e = document.getElementById("id_totalpagar");
        var strtt = e.value;
        console.log('entra mt', strtt);
        let totalpagar = document.getElementById('amtot');
        totalpagar.value = (strtt);
        console.log('enasig', totalpagar.value);



        var e = document.getElementById("id_plazo");
        var strq = e.options[e.selectedIndex].text;
        console.log('entra fgm', strq);
        let plaam = document.getElementById('ampla');
        plaam.value = strq;
        console.log('enasig', plaam.value);



        var fecham = document.getElementById("date_joined");
        var strfech = fecham.value;
        console.log('entra mtf', strfech);
        let fechat = document.getElementById('amfecha');
        fechat.value = strfech;
        console.log('enasig', fechat.value);




        var input_name = document.getElementById('nombprod');
        var strprod = input_name.value;
        console.log('tvalentran', strprod);
        let prodat = document.getElementById('amprod');
        prodat.value = strprod;
        console.log('enasig', prodat.value);



        var evend = document.getElementById("id_vendedor");
        var strqvend = evend.options[evend.selectedIndex].text;
        console.log('entra fgm', strq);
        let vendam = document.getElementById('amvend');
        vendam.value = strqvend;
        console.log('enasigv', vendam.value);

        //console.log('cliente', $('#first').find(':selected').val());
        //console.log('cliente', $('#id_cli').select2().val());
        //my_veriable = $('#id_cli').select2().val();
        //var my_last_veriable = my_veriable.toString();
        //console.log('cliente', my_last_veriable);

        //var ett = document.getElementById("id_cli");
        //var strUser = ett.options[e.selectedIndex].value;
        //console.log('entra cli', strUser);

        //$('id_cli').on("select2:select", function(e) {
        //    console.log("ID seleccionado: " + e.params.data.id);
        //});
        var arname = $('#id_cli').select2('data')[0];
        var val = (arname['text']);
        console.log('ent', val);



        let nameat = document.getElementById('amclient');
        nameat.value = val;
        console.log('ename', nameat.value);


        //console.log('entraaam', $('#id_cli').select2('data')[0]);
        //console.log('entramm'), $("#id_cli option:selected").text();;
        //['text']
        //$('#id_cli').select2().val()
        //var fecham = document.getElementById("date_joined");
        //var strfech = fecham.value;
        //console.log('entra mtf', strfech);
        //let fechat = document.getElementById('amfecha');
        //fechat.value = strfech;
        //console.log('enasig', fechat.value);




        const llenarTabla = document.querySelector('#tblAmort tbody');


        while (llenarTabla.firstChild) {
            llenarTabla.removeChild(llenarTabla.firstChild);
        }
        //faltacliente
        //var eclient = document.getElementById("id_cli");
        //var strcliente = eclient.options[e.selectedIndex].text;
        //console.log('entra fgmc', strcliente);
        //let plaam = document.getElementById('ampla');
        //plaam.value = strq;
        //console.log('enasig', plaam.value);



        $('#myModalAmort').modal('show');
    });


    $('#myModalAmort').on('hidden.bs.modal', function(e) {
        $('#frmAmort').trigger('reset');
    })



    $('#frmAmort').on('submit', function(e) {
        console.log("eeeentraaaa");
        //console.log("entraconvalor", totalpagar)
        e.preventDefault();
        var parameters = new FormData(this);


        //console.log("eeeentraaaa1", scant);
        //console.log("eeeentraaaa2", vents.items.cli);




        const llenarTabla = document.querySelector('#tblAmort tbody');


        while (llenarTabla.firstChild) {
            llenarTabla.removeChild(llenarTabla.firstChild);
        }




        var e = document.getElementById("id_totalpagar");
        var strtt = e.value;
        console.log('entra mt', strtt);
        let totalpagar = document.getElementById('amtot');
        totalpagar.value = (strtt);
        console.log('enasig', totalpagar.value);



        var e = document.getElementById("id_plazo");
        var strq = e.options[e.selectedIndex].text;
        console.log('entra fgm', strq);
        console.log('tipo');
        console.log('tipo', typeof(strq));

        //var arrpla = list(strq.split(" "));//  strq.split();
        let arrpla = (strq.split(' '));
        //var arrpla = list(strq);
        console.log('arrr', arrpla);
        console.log('arrpla', typeof(arrpla));



        //x = "Programa en Python"
        //lista = []
        //console.log('tt', x);
        //y = x.split();
        //lista.append(x)
        //console.log('transf', lista);

        var numes = arrpla[0];
        console.log('p', numes)
        let plaam = document.getElementById('ampla');
        plaam.value = strq;
        console.log('enasig', plaam.value);






        let fecha = []
        let fechaActual = Date.now();
        let mes_actual = moment(fechaActual);
        mes_actual.add(1, 'month');
        console.log('asdf', fechaActual);
        console.log('asdf', mes_actual);
        //console.log('asdfgggggg', totalpagar1);


        //let pagoCapital = 0,
        cuota = 0;
        cuota = (strtt / numes).toFixed(2);
        console.log('cuota a pagar', cuota);
        //cuota = totalpagar * (Math.pow(1 + 1 / 100, plazo) * 1 / 100) / (Math.pow(1 + 1 / 100, plazo) - 1);
        var forent = 0;
        var pago = 0;
        var pagoCapital = 0;
        var monto = 0;
        for (let i = 1; i <= numes; i++) {

            console.log('valor cuota', cuota);
            console.log('monto i', strtt);
            strtt = parseFloat(strtt - cuota);
            console.log('menos', strtt);
            //pago = menos - cuota;
            //pago = 0;
            //console.log('cantidad inicial', pago);
            //pagoCapital = pago - cuota;
            pagoCapital = 0;
            console.log('cantidad de cat', pagoCapital);
            //monto = parseFloat(pagoCapital - cuota);
            monto = 0;
            console.log('mmm', monto);



            fecha[i] = mes_actual.format('DD-MM-YYYY');
            mes_actual.add(1, 'month');

            forent = forent + 1;
            console.log('cuantas veces', forent);

            const row = document.createElement('tr');
            row.innerHTML = `
                    <td>${forent}</td>
                    <td>${fecha[i]}</td>
                    <td>${cuota}</td>
                    <td>${(strtt.toFixed(2))}</td>
                  
                `;
            llenarTabla.appendChild(row)

        }
        console.log('sale');
        //console.log('tttt', totalpagar);
        //console.log('xxxx', plazo);

        //console.log('cuota');
        //console.log(cuota);







        //parameters.append('action', 'create_client');
        //submit_with_ajax(window.location.pathname, 'Notificación',
        //  '¿Estas seguro de crear al siguiente cliente?', parameters,
        //  function(response) {
        //console.log(response);
        //var newOption = new Option(response.full_name, response.id, false, true);
        //$('select[name="cli"]').append(newOption).trigger('change');
        //$('#myModalAmort').modal('hide');
        // });
    });









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
            '¿Estas seguro de crear al siguiente cliente?', parameters,
            function(response) {
                //console.log(response);
                var newOption = new Option(response.full_name, response.id, false, true);
                $('select[name="cli"]').append(newOption).trigger('change');
                $('#myModalClient').modal('hide');
            });
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


    .on('change', 'input[name="desc"]', function() {
        //console.clear();
        var desc = parseInt($(this).val());
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        vents.items.products[tr.row].desc = desc;

        vents.calculate_invoice();
        $('td:eq(6)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
    })




    .on('change', 'input[name="cant"]', function() {
        console.clear();
        var cant = parseInt($(this).val());
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        vents.items.products[tr.row].cant = cant;

        vents.calculate_invoice();
        $('td:eq(6)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
        //$('td:eq(4)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));

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
            product.desc = 0.00;
            product.pvpchange = 0.00;


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
        vents.items.cli = $('select[name="cli"]').val();
        //console.log('eeeens', vents.items.cli);
        vents.items.plazo = $('select[name="plazo"]').val();
        console.log('plazo', vents.items.plazo)
        vents.items.sucursal = $('select[name="sucursal"]').val();
        console.log('sucursal', vents.items.sucursal)
        vents.items.vendedor = $('select[name="vendedor"]').val();
        console.log('vendedor', vents.items.vendedor)
        vents.items.entrada = $('input[name="entrada"]').val();
        console.log('ensjb', vents.items.entrada);

        //vents.items.total = $('input[name="total"]').val();
        //console.log('total', vents.items.total);

        //vents.items.totalpagar = $('input[name="totalpagar"]').val();
        //console.log('totalpagar', vents.items.totalpagar);

        //vents.items.iva = $('input[name="iva"]').val();
        //console.log('iva', vents.items.iva);

        vents.items.tipo = $('select[name="tipo"]').val();
        //console.log('tipo', vents.items.tipo)

        //vents.items.ent = $('input[name="ent"]').val();

        var e = document.getElementById("id_tax");
        var strUser = e.options[e.selectedIndex].text;
        console.log('entra fg', strUser);


        var parameters = new FormData();
        //parameters.append('id_totalpagar', id_totalpagar.value)
        //console.log('asiii', id_totalpagar.value);
        vents.items.totalpagar = id_totalpagar.value;
        console.log('asiii2', id_totalpagar.value);
        vents.items.iva = strUser;
        console.log('asiii3', strUser);
        vents.items.subtotal = id_subtotal.value;
        console.log('asiii4', id_subtotal.value);
        vents.items.total = id_total.value;
        console.log('asiii5', id_total.value);


        //fd.append('suc', suc.value)
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));




        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters,
            function(response) {
                alert_action('Notificación', '¿Desea imprimir la Cotización?', function() {
                    window.open('/erp/sale/invoice/pdf/' + response.id + '/', '_blank');
                    location.href = '/erp/quotation/list/';
                }, function() {
                    location.href = '/erp/quotation/list/';
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
        data.subtotal = 0.00;
        data.desc = 0.00;
        data.pvpchange = 0.00;

        vents.add(data);
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
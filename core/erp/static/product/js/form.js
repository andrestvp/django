var tblProducts;
var tblSearchProducts;
var vents = {
    items: {
        pvp: 0.00,
        costo: 0.00,

    },

    calculate_invoice: function() {
        var costo = 0.00;
        var costo = $('input[name="costo"]').val();


        this.items.pvp = (this.items.costo * 118) / 100;



        $('input[name="pvp"]').val(this.items.pvp.toFixed(2));


    },
    add: function(item) {
        this.calculate_invoice();

    },

};



$(function() {

    $("input[name='costo']").TouchSpin({
            min: 0,
            max: 1000,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            maxboostedstep: 10,
            postfix: '$'
        }).on('change', function() {
            vents.calculate_invoice();
        })
        //.val(50.00);





    // event submit
    $('#frmSale').on('submit', function(e) {
        e.preventDefault();


        vents.items.costo = $('input[name="costo"]').val();

        console.log('ensj', vents.items.entrada);


        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters,
            function() {
                location.href = '/erp/product/list/';
            },
        );
    });


    // Esto se puso aqui para que funcione bien el editar y calcule bien los valores del iva. // sino tomaría el valor del iva de la base debe
    // coger el que pusimos al inicializarlo.
});
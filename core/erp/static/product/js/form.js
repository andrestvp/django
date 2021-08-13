//function getImagePreview(event) {
//    var imagen = URL.createObjectURL(event.target.files[0]);
//    var imagendiv = document.getElementById('preview');
//    var newimg = document.createElement('img');
//    imagendiv.innerHTML = '';
//    newimg.src = imagen;
//    newimg.width = "100";
//    newimg.height = "100";
//    imagendiv.appendChild(newimg);
//}

const imag = document.getElementById('id_image')
imag.addEventListener('change', () => {

    var imagen = URL.createObjectURL(event.target.files[0]);
    var imagendiv = document.getElementById('preview');
    var newimg = document.createElement('img');
    imagendiv.innerHTML = '';
    newimg.src = imagen;
    newimg.width = "100";
    newimg.height = "100";
    imagendiv.appendChild(newimg);

})

//COSTO*118% ES PVP
$('#id_standardcost').on('change', function() {
    var selectValor = $(this).val();
    let input_pvp = document.getElementById('id_pvp');
    var precio = 0.00
    var sum = 0.00
        //console.log('entra', selectValor);
    precio = parseFloat((selectValor * 118) / 100);
    //dict.subtotal = dict.cant * parseFloat(dict.pvp);

    suma = parseFloat(precio) + parseFloat(selectValor);
    //console.log('valor', selectValor);

    //console.log('sacaporcentaje', precio);
    //console.log('sacaprecio', suma);
    input_pvp.value = suma;

});
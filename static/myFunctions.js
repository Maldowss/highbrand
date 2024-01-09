function addFavorite(prueba) {
    // Obtener los datos del formulario
    var idUser = $('.user_id'+prueba).attr('id');
    var id_clothe = $('.clothe_id'+prueba).attr('id');
    var name = $('.name'+prueba).attr('id');
    var brand = $('.brand'+prueba).attr('id');
    var price = $('.price'+prueba).attr('id');
    var image = $('.image'+prueba).attr('id');
    var url = $('.url'+prueba).attr('id');

    // Realizar la solicitud AJAX
    $.ajax({
        type: 'POST',
        url: '/addFavorite',
        data: { id_user: idUser,
                id_clothe: id_clothe,
                name: name,
                brand: brand,
                price: price,
                image: image,
                url: url},
        success: function (response) {
            // Manejar la respuesta del servidor (puede mostrar un mensaje de éxito, etc.)
            $('#action'+prueba).toggleClass('btn-success btn-danger');
            $('#action'+prueba).attr('onclick', `deleteFavorite('${prueba}')`);
            $('#action'+prueba).text('Eliminar');
            console.log(prueba);
        },
        error: function (error) {
            // Manejar errores si es necesario
            console.error(error);
        }
    });
}

function deleteFavorite(prueba) {
    // Obtener los datos del formulario
    var idUser = $('.user_id'+prueba).attr('id');
    var id_clothe = $('.clothe_id'+prueba).attr('id');

    // Realizar la solicitud AJAX
    $.ajax({
        type: 'POST',
        url: '/deleteFavorite',
        data: { id_user: idUser,
                id_clothe: id_clothe},
        success: function (response) {
            // Manejar la respuesta del servidor (puede mostrar un mensaje de éxito, etc.)
            $('#action'+prueba).toggleClass('btn-danger btn-success');
            $('#action'+prueba).attr('onclick', `addFavorite('${prueba}')`);
            $('#action'+prueba).text('Favoritos');
            console.log(prueba);
        },
        error: function (error) {
            // Manejar errores si es necesario
            console.error(error);
        }
    });
}

//Para el user info

function deleteFavoriteUser(prueba) {
    // Obtener los datos del formulario
    var idUser = $('.user_id'+prueba).attr('id');
    var id_clothe = $('.clothe_id'+prueba).attr('id');

    // Realizar la solicitud AJAX
    $.ajax({
        type: 'POST',
        url: '/admin/info/deleteFavoriteUser',
        data: { id_user: idUser,
                id_clothe: id_clothe},
        success: function (response) {
            // Manejar la respuesta del servidor (puede mostrar un mensaje de éxito, etc.)
            $('#action'+prueba).toggleClass('btn-danger btn-success');
            $('#action'+prueba).attr('onclick', `addFavorite('${prueba}')`);
            console.log(id_clothe)

            // Borrar el contenido y el elemento con id "drop2"
            $('#drop'+prueba).empty().remove();
            console.log(prueba);
        },
        error: function (error) {
            // Manejar errores si es necesario
            console.error(error);
        }
    });
}
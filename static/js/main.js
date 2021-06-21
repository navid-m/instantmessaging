var first = true

window.addEventListener('DOMContentLoaded', (event) => {
    if (first) {
        new WOW().init();
        Swal.fire({
            title: "Specify your username",
            html: "<input id='uname' class='swal2-input' autocomplete='off'>",
            focusConfirm: false,
            customClass: 'fast-animation',
            allowOutsideClick: false,
            allowEscapeKey: false,
            showClass: {
              popup: shclss,
            },
            hideClass: {
              popup: hclss
            }, 
            closeOnConfirm: true,
            closeOnCancel: false
          }).then(function() {
                post('/go', {uname: document.getElementById('uname').value})
                first = false;
        })
    }
})
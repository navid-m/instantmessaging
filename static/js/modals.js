function join() {
    Swal.fire({
        title: "Enter code",
        html: "<input id='code' class='swal2-input' autocomplete='off'>",
        focusConfirm: false,
        customClass: 'fast-animation',
        showClass: {
          popup: shclss
        },
        hideClass: {
          popup: hclss
        }, 
        closeOnConfirm: true
    }).then(function(result) {
        if (result.isConfirmed) {
            post('/join', {rcode: document.getElementById('code').value.replace(" ", "")})
        }
    })
}
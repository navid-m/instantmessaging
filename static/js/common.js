var shclss = 'animate__animated animate__fadeInDown'
var hclss = 'animate__animated animate__fadeOutUp'

function post(path, params, method='post') {
    const form = document.createElement('form');
    form.method = method; 
    form.action = path;
    for (const key in params) {
        if (params.hasOwnProperty(key)) {
            const hiddenField = document.createElement('input');
            hiddenField.type = 'hidden'; hiddenField.name = key; hiddenField.value = params[key];
            form.appendChild(hiddenField);
        }
    }
    document.body.appendChild(form);
    form.submit();
}
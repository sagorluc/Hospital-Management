
function showPassword() {
    // alert('reading form showPasswordLogin')
    var passwordField = document.getElementById('password');
    var showPasswordCheckbox = document.getElementById('showPasswordCheckbox');

    if (showPasswordCheckbox.checked) {
        passwordField.type = 'text';
    } else {
        passwordField.type = 'password';
    }
}


function showPasswordReset(){
    // alert('reading form showPasswordReset')
    var oldPass = document.getElementById('old_password')
    var newPass = document.getElementById('new_password')
    var conPass = document.getElementById('confirm_password')
    var passCheckbox = document.getElementById('showPasswordCheckBox')

    if(passCheckbox.checked){
        oldPass.type = 'text'
        newPass.type = 'text'
        conPass.type = 'text'
    }else{
        oldPass.type = 'password'
        newPass.type = 'password'
        conPass.type = 'password'
    }
}
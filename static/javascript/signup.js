$("span").on("click", "i", function() {
	$(this).toggleClass("fa-eye fa-eye-slash");
	var input = $("#password");
	if(input.attr("type") === "password") {
		input.attr("type", "text");
	} else {
		input.attr("type", "password");
	}
});

function validityMethodUname(){
	let input_name=$("#username").val();
	if (uname_array.includes(input_name)){
		$('#unamecheck').show();
	}
	else {
		$('#unamecheck').hide();
	}
}

function validityMethodEmail(){
	let input_mail=$("#email").val();
	if (email_array.includes(input_mail)){
		$('#emailcheck').show();
	}
	else {
		$('#emailcheck').hide();
	}
}

$(document).ready(function(){
// Validate Confirm Password 
$('#conpasscheck').hide(); 
$('#unamecheck').hide();
$('#emailcheck').hide();
let confirmPasswordError = true; 
$('#conpassword').keyup(function () { 
	validateConfirmPasswrd(); 

}); 
function validateConfirmPasswrd() { 
	let confirmPasswordValue =  
		$('#conpassword').val(); 
	let passwrdValue =  
		$('#password').val(); 
	if (passwrdValue != confirmPasswordValue) { 
		$('#conpasscheck').show(); 
		$('#conpasscheck').html( 
			"Password didn't Match"); 
		$('#conpasscheck').css( 
			"color", "red"); 
		confirmPasswordError = false; 
		return false; 
	} else { 
		$('#conpasscheck').hide(); 
	} 
} 

$("button").click(function(){
	$.getJSON($SCRIPT_ROOT + '/student-signup', {
		value:Stop
		},function(){
			return false;
		});
});
});
 
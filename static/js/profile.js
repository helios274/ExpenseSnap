jQuery(function(){
    $("#saveBtn").attr("disabled", true); 
    $('[name="first_name"]').attr("disabled", true); 
    $('[name="last_name"]').attr("disabled", true); 
    $('[name="username"]').attr("disabled", true); 
    $("#editBtn").on("click", function(e) {
        e.preventDefault();
        if ($("#saveBtn").attr("disabled")) {
            $("#saveBtn").attr("disabled", false); 
            $('[name="first_name"]').attr("disabled", false); 
            $('[name="last_name"]').attr("disabled", false); 
            $('[name="username"]').attr("disabled", false); 
        } else {
            $("#saveBtn").attr("disabled", true); 
            $('[name="first_name"]').attr("disabled", true); 
            $('[name="last_name"]').attr("disabled", true); 
            $('[name="username"]').attr("disabled", true); 
        }
    })
});
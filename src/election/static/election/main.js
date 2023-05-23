$(document).ready(function() {
    $("#add-report-btn").click(function(){
        $("#add-report-form").removeClass("d-none");
        $(this).addClass("d-none");
    });
    
    $('.captcha').click(function () {
        $.getJSON("/captcha/refresh/", function (result) {
            $('.captcha').attr('src', result['image_url']);
            $('#id_captcha_0').val(result['key'])
        });
    });
    
    // $("#add-report-btn").click(function(){
    //     $("#add-report-form").removeClass("d-none");
    //     $(this).addClass("d-none");
    // });

    // $("#add-report-form").submit(function(){
    //     console.log($(this).serialize());
    //     alert("submitted")
        // $.ajax({
        //     type: "POST",
        //     url: actionUrl,
        //     data: form.serialize(), // serializes the form's elements.
        //     success: function(data)
        //     {
        //       alert(data); // show response from the php script.
        //     }
        // });
    // });
});
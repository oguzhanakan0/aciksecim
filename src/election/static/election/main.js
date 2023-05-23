function runAjaxQuery(url_,data_,return_to_) {
    $.ajax({
        url: url_,
        data: data_,
        success: function (data) {
            console.log('query success')
            $(return_to_).html(data);
        }
    });
}

$(document).ready(function() {
    $("#add-report-btn").click(function(){
        $("#add-report-form").removeClass("d-none");
        $(this).addClass("d-none");
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
console.log("working fine")
$("#comment-form").submit(function(e){
    e.preventDefault();

    $.ajax({
        data:$(this).serialize(),
        method:$(this).attr("method"),
        url:$(this).attr("action"),
        datatype:"json",
        success:function(response){
            console.log("comment saved")
            if(response.bool==True){
                $("#review-response").html("Review Added Successfully!!")
            }
        }
    })
})
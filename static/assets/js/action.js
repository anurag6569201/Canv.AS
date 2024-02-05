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

// add to cart
$(".add-to-cart-button").on('click', function() {
    let this_val = $(this);
    let index_ = this_val.attr("data-index");

    let quantity = $(".product-quantity-" + index_).val();
    let product_title = $(".product-title-" + index_).val();
    let product_id = $(".product-id-" + index_).val();
    let product_pid = $(".product-pid-" + index_).val();
    let product_price = $(".current-product-price-" + index_).val();
    let btnadd = $(".btnadd");

    console.log(quantity);
    console.log(product_title);
    console.log(product_id);
    console.log(product_price);
    console.log(this_val);
    console.log(index_);
    console.log(product_pid);

    $.ajax({
        url:'/add-to-cart',
        data:{
            'id':product_id,
            'qty':quantity,
            'price':product_price,
            'title':product_title,
            'product_pid':product_pid,
        },
        datatype:'json',
        beforeSend:()=>{
            console.log("added product to cart");
        },
        success:(res)=>{
            this_val.html('<i class="fa-solid fa-check"></i>')
            console.log("added product to cart");
            $(".cart-items-count").text(res.totalcartitems)
        }
    })
})
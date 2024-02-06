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
$(document).ready(function(){
    $(".add-to-cart-button").on('click', function() {
        let this_val = $(this);
        let index_ = this_val.attr("data-index");
    
        let quantity = $(".product-quantity-" + index_).val();
        let product_title = $(".product-title-" + index_).val();
        let product_image = $(".product-image-" + index_).val();
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
        console.log(product_image);
    
        $.ajax({
            url:'/add-to-cart',
            data:{
                'id':product_id,
                'qty':quantity,
                'price':product_price,
                'title':product_title,
                'product_pid':product_pid,
                'product_image':product_image,
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
    
    $(".update-cart").on('click', function() {
        let product_id=$(this).attr("data-product");
        let this_val=$(this);
        let product_qty = $(".product-quantity-" + product_id).val();
        console.log(product_id);
        console.log(product_qty);
        console.log(this_val);
        $.ajax({
            url:'/update-cart',
            data:{
                'id':product_id,
                'qty':product_qty,
            },
            datatype:"json",
            beforeSend:function(){
                this_val.hide()
            },
            success:function(res){
                this_val.show()
                $(".cart-items-count").text(res.totalcartitems)
                $("#cart-list").html(res.data)
            }
        })
    })
})
// $(".product-card__get-price, .product-card-wide__get-price").click(function(event){
// 	event.preventDefault();
// 	console.log("price request");
// })


$(".product-card__remove").click(function(event){
	event.preventDefault();
	$(this).closest('.product-card').toggleClass('removed');
})

$('.extra-products-slider__slider-body').on('init', function(){
	$(".product-card__title").each(function(i, el){
		var item = $(el).dotdotdot({
			watch: "window",
		}).data( "dotdotdot" );
	})
});

function initProductDots(){
	$(".product-card__title, .product-card-wide__title").each(function(i, el){
		var item = $(el).dotdotdot({
			watch: "window",
		}).data( "dotdotdot" );
	})
}

$(window).ready(function(){
	initProductDots();
})

window.initProductDots = initProductDots;
$(".product-form__show-params").click(function(e){
	e.preventDefault();

	var headerHeight = $(window).width() > 1199 ? 50 : $(".header__mobile").height();
	var destination = $(".product__information").offset().top - headerHeight;
    $('html, body').animate({ scrollTop: destination }, 600);
});
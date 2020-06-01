$('.extra-products-slider__slider-body').each(function (i, e) {
	$parent = $(e).parents('.extra-products-slider');
	$parent.addClass('active');
	$(e).slick({
		centerMode: false,
		slidesToShow: 4,
		slidesToScroll: 4,
		dots: true,
		nextArrow: $parent.find('.extra-products-slider__nav-button_next'),
		prevArrow: $parent.find('.extra-products-slider__nav-button_prev'),
		responsive: [
			{
				breakpoint: 1200,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 3,
				}
			},
			{
				breakpoint: 992,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2,
				}
			},
			{
				breakpoint: 576,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
			},
		]
	});
})
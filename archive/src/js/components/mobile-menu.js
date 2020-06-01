$("body").on('click', '.header__mobile-burger', function(e){
	e.preventDefault();
	
	if ($(this).hasClass('opened')) {
		$("body, html").removeClass('opened');
		$("body, html").scrollTop($('body').data('scrolled'));
	} else {
		let scrollTop = $(window).scrollTop();
		$("body, html").addClass('opened');
		$("body, html").scrollTop(scrollTop);
		$('body').data('scrolled', scrollTop);
	}

	$(this).toggleClass('opened')
	$(".mobile-menu").toggleClass('opened');

    if (!$(this).hasClass("opened")){
        $(".mobile-menu-list__sub-menu.opened").removeClass('opened');
        $(".mobile-menu.no-scroll, .mobile-menu-list__sub-menu.no-scroll").removeClass('no-scroll');
    }
});



/*	Открытие мобильного подменю
---------------------------------------*/
$("body").on('click', '.mobile-menu .has-children > a', function(e){
	e.preventDefault();
	$(this).closest(".mobile-menu-list__sub-menu, .mobile-menu").toggleClass('no-scroll');
	$(this).closest(".has-children").find("> .mobile-menu-list__sub-menu").toggleClass('opened');
});

/*	Закрытие мобильного подменю
---------------------------------------*/
$("body").on('click', '.mobile-menu-list__step-back', function (e) {
	e.preventDefault();
	$(this).closest(".mobile-menu-list__sub-menu.no-scroll, .mobile-menu.no-scroll").toggleClass('no-scroll');
	$(this).closest(".mobile-menu-list__sub-menu.opened").toggleClass('opened');
});



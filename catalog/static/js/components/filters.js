$("body").on('click', '.filters__mobile-submit', function(){
	closeMobileFilters();
	catalogScrollTop();
})
$("body").on('click', '.filters__mobile-reset', function(){
	closeMobileFilters();
	catalogScrollTop();
})

$('body').on('click', '.filter-close', function(e){
	e.preventDefault();
	closeMobileFilters();
})

function openMobileFilters(){
	let scrollTop = $(window).scrollTop();
	$(".filters, .filter-close").addClass('opened');
	setTimeout(function(){
		$("body, html").addClass('opened');
		$("body, html").scrollTop(scrollTop);
		$('body').data('scrolled', scrollTop);
	}, 300)
	
}

function closeMobileFilters(){
	$(".filters, body, html, .filter-close").removeClass('opened');
	$("body, html").scrollTop($('body').data('scrolled'));
}

function catalogScrollTop(){
	$('html, body').animate({scrollTop: 0},500);
}

$('body').on('submit', 'form.filtering', catalogScrollTop);

window.openMobileFilters = openMobileFilters;
window.closeMobileFilters = closeMobileFilters;
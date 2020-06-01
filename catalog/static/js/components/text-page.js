function resizeContent(){

	$('.content img').each(function (i, e) {
		var w_post_img = $(e).width();
		var h_post_img = w_post_img * 32 / 64;
		$(e).css('height', h_post_img);
	});

	$('.gallery-item-thumbnail, .certificate-thumbnail').each(function(i, e) {
		var w_gallery_img = $(e).width();
		var h_gallery_img = w_gallery_img / 1.5;
		$(e).css('height', h_gallery_img);
	});
}
resizeContent();
$(window).resize( function(){ resizeContent(); } );

/*     Обертка таблицы на текстовых    */
$('.content-text > table').prev('h3').addClass('table-title');
$('.content-text > table').wrap('<div class="table"><div class="table-responsive"></div></div>');
$('.content-text > .table').each(function(){
	$(this).prev('h3.table-title').prependTo( $(this) );
});

$('img.lazy').each(function (index, el) {
	$(el).parent().addClass('lazy_wrap');
	$(el).lazy({
		afterLoad: function (element) {
			$(el).parent().removeClass('lazy_wrap');
		}
	});
});

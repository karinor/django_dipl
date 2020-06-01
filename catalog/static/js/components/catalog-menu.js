/*     Формирование столбцов в подменю     */
$(".catalog-menu__list > li > a").hover(function(i, e){
	let $subMenu = $(this).next();
	let maxHeight = $subMenu.parents(".catalog-menu__list").outerHeight(true);
	let sum = 24;

	$subMenu.append('<div class="row"><div class="col-4 catalog-menu__item-col"></div></div>');
	$subMenu.find('.catalog-menu__start-col a').each(function(index, elem){
		
		
		if (sum + $(elem).outerHeight(true) < maxHeight){
			sum += $(elem).outerHeight(true);
		}
		else{
			$subMenu.find('.row').append('<div class="col-4 catalog-menu__item-col"></div>');
			sum = $(elem).outerHeight(true) + 24;
		}

		$subMenu.find(".catalog-menu__item-col:last-child").append($(elem)[0].outerHTML);
		$(elem).remove();
	});
});
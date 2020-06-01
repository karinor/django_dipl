$(".seo-scroller").each(function () {
	var $wrapper = $(this).find(".seo-scroller__seo-images");
	var $images = $wrapper.find("img");

	if ($images.length === 1) {
		$images.each(function (i, e) {
			$wrapper.append("<div class='seo-scroller__seo-image seo-scroller__seo-image_large'>" + $(e)[0].outerHTML + "</div>");
			$(e).remove();
		})
	}
	else if ($images.length === 2) {
		var count = 0;
		$images.each(function (i, e) {
			if (!count) {
				$wrapper.append("<div class='seo-scroller__seo-image seo-scroller__seo-image_big'>" + $(e)[0].outerHTML + "</div>");
			}
			else {
				$wrapper.append("<div class='seo-scroller__seo-image seo-scroller__seo-image_big'>" + $(e)[0].outerHTML + "</div>");
			}

			$(e).remove();
			count++;
		});
	}
	else if ($images.length === 3) {
		var count = 0;
		$wrapper.append("<div class='seo-scroller__img-row'></div>");
		$images.each(function (i, e) {
			if (count !== 2) {
				$wrapper.find(".seo-scroller__img-row").append("<div class='seo-scroller__seo-image'>" + $(e)[0].outerHTML + "</div>");
			}
			else {
				$wrapper.append("<div class='seo-scroller__seo-image seo-scroller__seo-image_big'>" + $(e)[0].outerHTML + "</div>");
			}

			$(e).remove();
			count++;
		});
	}
	else {
		var count = 0;
		$wrapper.append("<div class='seo-scroller__img-row'></div>");
		$images.each(function (i, e) {
			if(count > 1){
				$wrapper.append("<div class='seo-scroller__img-row'></div>");
				count = 0;
			}
			else count++;

			$wrapper.find(".seo-scroller__img-row").last().append("<div class='seo-scroller__seo-image'>" + $(e)[0].outerHTML + "</div>");
			$(e).remove();
		})
	}
});

OverlayScrollbars(document.querySelectorAll(".seo-scroller__seo-text"), {
    autoUpdate: true,
    overflowBehavior: {
        x: "hidden",
        y: "scroll"
    }
})

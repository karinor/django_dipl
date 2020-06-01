import "overlayscrollbars"

setScrollbar( $(".filter-block__body.show .filter-block__scroll-content") );

$('.filter-block__body').on('shown.bs.collapse', function () {
	setScrollbar($(this).find(".filter-block__scroll-content"));
})

function setScrollbar(target){
	OverlayScrollbars(target, {
		autoUpdate: true,
		overflowBehavior: {
			x: "hidden",
			y: "scroll"
		}
	})
}
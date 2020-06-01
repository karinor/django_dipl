function recalculateCart(){
	var $cart = $(".cart");
	var userStatus = $cart.attr('data-mode');
	var totalPrice = 0;
	var newTotalPrice = 0;
	var maxTotalPrice = 0;
	var divider = 100;

	$cart.find('.cart-table-body .cart-table-row').each(function(i, el){
		totalPrice += $(el).find('.cart-item-price-value').data("vip-price") / 90 * 100 * $(el).find('input').val();
	});
	
	if(userStatus !== 'vip' && totalPrice < 2000)
		divider = 90;
	else if(userStatus !== 'vip' && totalPrice >= 2000 && totalPrice < 12000)
		divider = 95;
	
	
	$cart.find('.cart-table-body .cart-table-row').each(function(i, el){
		var $priceTag = $(el).find('.cart-item-price-value');
		var $oldPriceTag = $(el).find('.cart-item-old-price-value');
		
		var price = Math.floor($priceTag.data("vip-price") / divider * 100);
		var oldPrice = Math.floor($oldPriceTag.data("vip-price") / divider * 100);
		var total = price * $(el).find('input').val();
		
		
		$priceTag.html( convertPrice( price ) );
		$oldPriceTag.html( convertPrice( oldPrice ) );
		$(el).find('.cart-item-total').html(convertPrice(total));
		newTotalPrice += total;

		console.log($priceTag.data("vip-price"), $priceTag.data("vip-price") / 90 * 100, Math.floor($priceTag.data("vip-price") / 90 * 100))
		maxTotalPrice += Math.floor($priceTag.data("vip-price") / 90 * 100) * $(el).find('input').val();
	});
	$cart.find('.cart-total').html(convertPrice(newTotalPrice));
	console.log(maxTotalPrice - newTotalPrice, maxTotalPrice,  newTotalPrice)
	var priceDiff = maxTotalPrice - newTotalPrice;
	if(priceDiff > 0){
		$cart.find('.cart-text__sell').html(convertPrice(priceDiff)).css('display', 'block');
	}
	else{
		$cart.find('.cart-text__sell').css('display', 'none');
	}
}

function convertPrice(price){
	return price.toLocaleString();
}

$("body").on('change', '.product-amount input', recalculateCart)
$(window).ready(recalculateCart)
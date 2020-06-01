$('body').on('click', '.product-amount__button', function () {
	var $input = $(this).parents('.product-amount').find('input');
	var val = +$input.val();

	if ($(this).hasClass('product-amount__button_minus')) $input.val(val - 1);
	else $input.val(val + 1);

	$(this).parents('.product-amount').find('input').change();
});

$('body').on('change', '.product-amount input', function () {
	var val = +$(this).val();
	var min = $(this).attr('min');
	var max = $(this).attr('max');
	$(this).val((val > max) ? max : (val < min) ? min : val);
});
$(document).ready(function() {
    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var last_serialize = '';
    var last_sort = '';
    var last_data_view = '';

    $('[data-type]').on('click', function(e) {
        console.log('qq');
        var type = $(this).attr('data-type');
        var url = window.location.href;
        last_data_view = 'data_view=' + type;
        data = last_data_view + '&' + last_serialize + '&' + last_sort;
        $.ajax({
            method: 'get',
            url: url,
            data: data
        }).done(function(response){
            $('.col-12.col-xl-9').children('div.row').html(response['products'] + response['paginator']);
        });
    });
    
    $('form.filters__form').submit(function(e) {
        e.preventDefault();
        var url = window.location.href;
        data = $(this).serialize();
        $.ajax({
            method: 'get',
            url: url,
            data:  data + '&' + last_data_view + '&' + last_sort
        }).done(function(response){
            last_serialize = data;
            console.log(last_serialize);
            $('.col-12.col-xl-9').children('div.row').html(response['products'] + response['paginator']);
            $('.filters__footer-result').text('Подобрано ' + response['count'] + ' ед. товара');
            $('.filters__mobile-result').text('Подобрано ' + response['count'] + ' ед. товара');
            
        });
    });
    
    $('.filters__reset').on('click', function(e) {
        var url = window.location.href;
        type = $('[data-type].active').attr('data-type');
        $('form.filters__form')[0].reset()
        last_serialize = ''
        $.ajax({
            method: 'get',
            url: url,
            data: last_data_view + '&' + last_sort,
        }).done(function(response){
            $('.col-12.col-xl-9').children('div.row').html(response['products'] + response['paginator']);
            $('.filters__footer-result').text('');
            $('.filters__mobile-result').text('');
            
        }); 
    });

    $('select[name="sort"]').on('change', function(e) {
        var url = window.location.href;
        data = 'sort=' + this.value; 
        $.ajax({
            method: 'get',
            url: url,
            data: data + '&' + last_data_view + '&' + last_serialize,
        }).done(function(response){
            last_sort = data;
            $('.col-12.col-xl-9').children('div.row').html(response['products'] + response['paginator']);
            $('.filters__footer-result').text('');
            $('.filters__mobile-result').text('');
        }); 
    });

    $('body').on('click', '.product-card__add-to-compare, .product-form__button_compare', function(e){
        e.preventDefault();
        var url = window.location.href;
        data = $(this).attr('data-add');
        console.log(data)
        $.ajax({
            method: 'post',
            url: url,
            data: data,
        }).done(function(response){
            console.log(response['compare_count'])
            $('.shop-button__count.compare-button__count').text(response['compare_count']);
        }); 
    });


    $('body').on('click', '.product-card__add-to-cart', function(e){
        e.preventDefault();
        var url = window.location.href;
        data = "action=cart&add=" + $(this).attr('data-add');
        console.log(data)
        $.ajax({
            method: 'post',
            url: url,
            data: data,
        }).done(function(response){
            console.log(response['cart_count'])
            $('.shop-button__count.cart-button__count').text(response['cart_count']);
        }); 
    });

    $('body').on('click', '.product-form__add-button.add-to-cart', function(e){
        e.preventDefault();
        var url = window.location.href;
        data = $(this).attr('data-add');
        console.log(data)
        $.ajax({
            method: 'post',
            url: url,
            data: data,
        }).done(function(response){
            console.log(response['cart_count'])
            $('.shop-button__count.cart-button__count').text(response['cart_count']);
        }); 
    });
    

    $('body').on('click', '.product-card__add-to-favorites, .product-form__button_add-to-favorites', function(e){
        e.preventDefault();
        var url = window.location.href;
        data = $(this).attr('data-add');
        console.log(data)
        $.ajax({
            method: 'post',
            url: url,
            data: data,
        }).done(function(response){
            console.log(response['favorites_count'])
            console.log($('.shop-button__count.favorites-button__count'))
            $('.shop-button__count.favorites-button__count').text(response['favorites_count']);
        }); 
    });


    $('body').on('click', 'button.cart-item-delete', function(e){
        var url = window.location.href;
        data = "action=cart&remove=" + $(this).parent().parent().parent().attr('data-id');
        $.ajax({
            method: 'post',
            url: url,
            data: data,
        }).done(function(response){
            console.log(response['cart_count'])
            if (response['cart_count'] > 0){
                $('[data-id="' + response["id"] + '"').detach();
            }
            else{
                $('div.cart').detach();
                $('.isempty').html(response['empty']) 
            }
            $('.shop-button__count.cart-button__count').text(response['cart_count']);
        }); 
    });
    $('.product-form__add-button.add-to-cart').attr('data-add')
   

    $('body').on('click', '.product-amount__button_minus, .product-amount__button_plus', function(e){
        var url = window.location.href;
        if (url.indexOf('products') != -1){
            button_add = $('.product-form__add-button.add-to-cart')
            data_pk = button_add.attr('data-pk')
            console.log($('.product-amount__field').children().val())
            $('.product-form__add-button.add-to-cart').attr('data-add', 'action=cart&add='+data_pk + '&count=' +  $('.product-amount__field').children().val())
        }
        else{
            data = "action=cart&update=" + $(this).parent().parent().parent().parent().parent().attr('data-id');
            data = data + '&count=' + $(this).parent().children('.product-amount__field').children('input').val()
            console.log(data)
            $.ajax({
                method: 'post',
                url: url,
                data: data,
            }).done(function(response){
            }); 
        }
    });
 
    $('body').on('click', '.checkout-form__toggle-area-trigger', function(e) {
        checked = $(this).hasClass('collapsed')
        if (checked){
            $(this).next().children().children('.checkout-group').children('input').prop('required', false)
        }
        else{
            $(this).next().children().children('.checkout-group').children('input').prop('required', true)
        }
    });
    
    $('body').on('click', '#checkout-tab-1, #checkout-tab-2', function(e) {
        id = $(this).attr('id')
        if (id == 'checkout-tab-2'){
            $('#checkout-tab-pane-2').children().children().children().children('input:not([name=district], [name=text], [name=message])').prop('required', 'required');
            // for(var i = 0;i < elements.length; i++){
            //     console.log(elements.children('input'));
            // }
            
            
           // $(this).next().children().children('.checkout-group').children('input').prop('required', false)
        }
        else{
            $('#checkout-tab-pane-2').children().children().children().children('input').prop('required', false);
           // $(this).next().children().children('.checkout-group').children('input').prop('required', true)
        }
    });

    $('body').on('click', 'span.product-card__remove', function(e) {
        e.preventDefault()
        var url = window.location.href;
        data = $(this).attr('data-remove');
        $.ajax({
            method: 'post',
            url: url,
            data: data,
        }).done(function(response){
            var count_type = ''
            var COUNT = '_count'
            var compare_count = 'compare_count'
            var favorites_count = 'favorites_count'
            console.log(compare_count)
            if (compare_count in response){
                count_type = 'compare'
            }
            else{
                count_type = 'favorites'
            }

            if (response[count_type + COUNT] > 0){
                $('[data-pk="' + response["id"] + '"').detach();
            //    .each(function(index, element) {
            //         $
            //     });
            }
            else if ((count_type + COUNT) == compare_count) {
                $('[data-pk="' + response["id"] + '"').detach();
                $('div.compare-component').children('div.row').children('div.col-12').html(response['empty'])
            }
            else if ((count_type + COUNT) == favorites_count){
                $('.col-12.col-sm-6.col-lg-4.col-xl-3').detach();
                $('div.container').children('div.row').children('div.col-12.brd').after(response['empty'])
            }
            $('.shop-button__count.'+ count_type + '-button__count').text(response[count_type + COUNT]);
        }); 
    });


/*
    $('.pagination-item:not(.active)').on('click', function(e) {
        e.preventDefault();
        var url = window.location.href;
        data = $(this).attr('href');
        data =  data + '&' + last_data_view + '&' + last_serialize + '&' + last_sort;
        console.log(data);
        $.ajax({
            method: 'get',
            url: url,
            data: data,
        }).done(function(response){
            $('.col-12.col-xl-9').children('div.row').html(response['products'] + response['paginator']);
            if (last_serialize != ''){
                $('.filters__footer-result').text('Подобрано ' + response['count'] + ' ед. товара');
                $('.filters__mobile-result').text('Подобрано ' + response['count'] + ' ед. товара');
            }
        }); 
    });  
*/  

    $('form.search_form').submit(function(e) {
        console.log($(this).serialize())
    });

    function changePage (e){
        e.preventDefault();
        var url = window.location.pathname;
        search_input = $('.search-form__input.q_main')
        if (search_input.length > 0){
            data = $(this).attr('href').replace('?', '');
            data += '&q=' + search_input.val()
            $.ajax({
                method: 'post',
                url: url,
                data: data,
            }).done(function(response){
                $('div.catalog-container').children('div.row').html(response['products'] + response['paginator']);
            }); 
        }
        else{
            data = $(this).attr('href').replace('?', '');
            data =  data + '&' + last_data_view + '&' + last_serialize + '&' + last_sort;
            console.log(data);
            $.ajax({
                method: 'get',
                url: url,
                data: data,
            }).done(function(response){
                $('.col-12.col-xl-9').children('div.row').html(response['products'] + response['paginator']);
                if (last_serialize != ''){
                    $('.filters__footer-result').text('Подобрано ' + response['count'] + ' ед. товара');
                    $('.filters__mobile-result').text('Подобрано ' + response['count'] + ' ед. товара');
                }
            }); 
        }
       
}
    $('body').on('click', '.pagination div a', changePage);

});

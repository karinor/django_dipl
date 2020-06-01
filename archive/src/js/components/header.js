function checkHeaderState(){
    if ( $(document).scrollTop() > 400 ){
        $('.header__desktop').addClass('scrolled');
    }
    else{
        $('.header__desktop').removeClass('scrolled');
    }
}

window.addEventListener("scroll", function(){
	checkHeaderState();
});
document.addEventListener("DOMContentLoaded", function(){
    checkHeaderState();
});
$(window).scroll(function(){
    var scroll = $(window).scrollTop();
    if(scroll < 70){
        $('.sticky-top').removeClass("sticky")
    } else{
        $('.sticky-top').addClass("sticky")
    }
});
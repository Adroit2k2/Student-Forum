$(document).ready(function () {
                $("#sidebar").mCustomScrollbar({
                    theme: "minimal"
                });

                $('#dismiss, .overlay').on('click', function () {
                    $('#sidebar').removeClass('active');
                    $('.overlay').fadeOut();
                });

                $('#sidebarCollapse').on('click', function () {
                    $('#sidebar').addClass('active');
                    $('.overlay').fadeIn();
                    $('.collapse.in').toggleClass('in');
                    $('a[aria-expanded=true]').attr('aria-expanded', 'false');
                });
         
});
$(document).ready(function () {
    $(window).on('scroll',function () {
        if ($(window).scrollTop() > 20) {
            $('.navbar').addClass('compressed');
        } else {
            $('.navbar').removeClass('compressed');
        }
    });
});
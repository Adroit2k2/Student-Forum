$(document).ready(function () {
                $("#sidebar").mCustomScrollbar({
                    theme: "minimal"
                });

                $('#dismiss,.overlay2').on('click', function () {
                    $('#sidebar').removeClass('active');
                    $('.overlay2').removeClass('active');

                });

                $('#sidebarCollapse').on('click', function () {
                    $('#sidebar').addClass('active');
                    $('.overlay2').addClass('active');
                    $('.collapse.in').toggleClass('in');
                    $('a[aria-expanded=true]').attr('aria-expanded', 'false');
                });


                // $("#login").on('click',function(){
                //     $('.wrapper').addClass('overlay');
                //     $('.login').css('display',"");
                //     console.log("hello");

                // });
                // $(".overlay").on('click',function(){

                //     $('.wrapper').removeClass('overlay');
                //     $('.login').css('display',"none");
                //     console.log("hello");
                // });

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

$(document).ready(function () {
       var url=window.location.href.split('/');
       var Links=document.getElementsByClassName('list-unstyled components')[0].getElementsByClassName('click');
       var i=0;
       var current=url[url.length-1];
       for(i=0;i<Links.length;i++){
        var ln=Links[i].href.split('/');
        if(ln[ln.length-1]==current){

            Links[i].className+=(' active');
        }
       }


});

// src="~/assets/js/bootstrap-select.min.js"
// $(document).ready(function () {



// });
// $(function () {
//       console.log("hello")
//         $('.selectpicker').selectpicker('render');
//         console.log("hello")
//         $('.selectpicker').change(function () {
// 		$('.output').html($(this).val());
// 	});

        // $(document).ready(function () {


//       $('.form-control').('keyup',function(e){
//           if(e.keyCode == 13){
//               $('.form-control').value=''
//           }
//         });
// });







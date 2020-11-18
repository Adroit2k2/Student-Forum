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
       var current=url[url.length-2];

       for(i=0;i<Links.length;i++){
            var ln=Links[i].href.split('/');

            if( ln[ln.length-2]==current ){

            Links[i].className+=(' active');
            }
        }


});
function Copytext(link)
    {
        var url = document.createElement("textarea");
        url.innerHTML = link;
        console.log(link);
        console.log(url.value);
        document.body.appendChild(url);
        url.select();
        var copy =document.execCommand("copy");
        var msg = copy ? 'successful' : 'unsuccessful';
        document.body.removeChild(url);
        alert("Link Copied");

    }
const copyToClipboard = str => {
  const el = document.createElement('textarea');
  el.value = str;
  console.log(el.value);
  document.body.appendChild(el);
  var t=el.select();
  console.log(t);
  var b=document.execCommand('copy');
  console.log(b);
  document.body.removeChild(el);
};








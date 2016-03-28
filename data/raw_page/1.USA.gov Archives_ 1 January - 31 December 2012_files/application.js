!function ($) {
  $(function(){
    // -- start animation -- //
    if (window.initialize) {
      window.initialize();
    }

    // -- Back buttons -- //
    $('.back-button').on('click', function (e) {
      e.preventDefault();
      window.history.go(-1);
    })

    // -- Navigation Scroll -- //
    // fix sub nav on scroll
    var $win = $(window)
      , $nav = $('.subnav')
      , navTop = $('.subnav').length && $('.subnav').offset().top
      , isFixed = 0;

    processScroll();

    // hack
    $nav.on('click', function () {
      if (!isFixed) setTimeout(function () {  $win.scrollTop($win.scrollTop() - 7) }, 10);
    })

    $win.on('scroll', processScroll);

    function processScroll() {
      var i, scrollTop = $win.scrollTop()
      if (scrollTop >= navTop && !isFixed) {
        isFixed = 1;
        $nav.addClass('subnav-fixed');
      } else if (scrollTop <= navTop && isFixed) {
        isFixed = 0;
        $nav.removeClass('subnav-fixed');
      }
    }
  })
}(window.jQuery)

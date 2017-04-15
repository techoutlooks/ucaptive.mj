(function ($) {
"use strict";
$(document).ready(function($){
/*--
	Mobile Menu
------------------------*/
$('.mobile-menu nav').meanmenu({
	meanScreenWidth: "990",
	meanMenuContainer: ".mobile-menu",
});
/*--
	DropDown On Click
-----------------------------------*/
$('.dropdown-btn').on('click', function(){
  if($(this).hasClass('active')){
	  $(this).removeClass('active');
	  $(this).siblings('.dropdown').slideUp( 500 );
  } else {
	  $('.dropdown-btn').removeClass('active');
	  $(this).addClass('active');
	  $( ".dropdown" ).slideUp( 500 );
	  $(this).siblings('.dropdown').slideDown( 500 );
  }
});
$('.shop-menu-item .wrap h3').on('click', function(){
  if($(this).parent('.wrap').hasClass('active')){
	  $(this).parent('.wrap').removeClass('active');
	  $(this).siblings('ul').slideUp( 500 );
  } else {
	  $('.shop-menu-item .wrap h3').parent('.wrap').removeClass('active');
	  $(this).parent('.wrap').addClass('active');
	  $('.shop-menu-item .wrap ul').slideUp( 500 );
	  $(this).siblings('ul').slideDown( 500 );
  }
});
$('#login-box .login-close').on('click', function(){
  $('.dropdown-btn.login-btn').removeClass('active');
  $('#login-box').slideToggle(500);
});
$( ".bookmark-dropdown li .close-btn" ).on('click', function(){
  $(this).parent( "li" ).remove();
});
$( ".shop-filter-btn" ).on("click", function(){
  $(this).toggleClass( "active" );
  $(this).siblings( ".shop-sidebar" ).slideToggle(500);
});
/*--
	One Page Nav
-----------------------------------*/
$('#onePage-nav ul li a').on('click', function(e) {
	e.preventDefault();
	var link = this;
	$.smoothScroll({
	  scrollTarget: link.hash
	});
});	
/*--
	Home Carousel
-----------------------------------*/
$(".home-slider").owlCarousel({
    animateOut: 'fadeOut',
    animateIn: 'fadeIn',
    items:1,
	autoplay: false,
    loop: true,
    nav: true,
	navText: ['<i class="mi-arrow-left"></i>', '<i class="mi-arrow-right"></i>'] 
});
/*--
	Relative Carousel
-----------------------------------*/
$(".relative-pro-slider").owlCarousel({
    items:4,
	autoplay: false,
    loop: true,
    nav: true,
	margin: 0,
	navText: ['<i class="mi-arrow-left"></i>', '<i class="mi-arrow-right"></i>'],
	responsive : {
		0 : {
			items : 1,
		},
		480 : {
			items : 2,
		},
		768 : {
			items : 2,
		},
		992 : {
			items : 3,
		},
		1050 : {
			items : 4,
		}
	}
});
/*--
	Cliuents Carousel
-----------------------------------*/
$(".clients-slider").owlCarousel({
    items:3,
	autoplay: false,
    loop: true,
    nav: false,
	responsive : {
		0 : {
			items : 1,
		},
		480 : {
			items : 2,
		},
		768 : {
			items : 3,
		}
	}
});
/*--
	Set Product Image Border on Hover
------------------------*/
$( ".sin-set-product .pro-contnet ul li" ).mouseover(function() {
    var setProImg = $(this).attr('class');
    $('.sin-set-product .img-box a.' + setProImg).addClass( 'active' );
  })
  .mouseout(function() {
	var setProImg = $(this).attr('class');
    $('.sin-set-product .img-box a.' + setProImg).removeClass( 'active' );
  });
/*--
	Price Range Slider
------------------------*/
 $( "#slider-range" ).slider({
	range: true,
	min: 0,
	max: 3000,
	values: [ 20, 1560 ],
	slide: function( event, ui ) {
		$( "#amount" ).val( "$" + ui.values[ 0 ] + " - "+ "$" + ui.values[ 1 ] );
		$('input[name="first_price"]').val(ui.values[0]);
		$('input[name="last_price"]').val(ui.values[1]);
	},
});
$( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
	" - "+"$" + $( "#slider-range" ).slider( "values", 1 ) );
$('input[name="first_price"]').val($( "#slider-range" ).slider( "values", 0 ));
$('input[name="last_price"]').val($( "#slider-range" ).slider( "values", 1 )); 
/*--
	Blog Image Slider
------------------------*/
$('.blog-image-slider').on('initialized.owl.carousel changed.owl.carousel', function(e) {
	if (!e.namespace) return;
	var carousel = e.relatedTarget;
	$(this).siblings('.slide-number').text(carousel.relative(carousel.current()) + 1 + '/' + carousel.items().length);
}).owlCarousel({
	items:1,
	loop:true,
	margin:0,
	nav:true,
	navText: ['<i class="mi-chevron-left"></i>', '<i class="mi-chevron-right"></i>'] 
});
/*--
	Map Sidebar Head Slider
------------------------*/
$('.map-sidebar-slider').on('initialized.owl.carousel changed.owl.carousel', function(e) {
	if (!e.namespace) return;
	var carousel = e.relatedTarget;
	$('.slide-number').text(carousel.relative(carousel.current()) + 1 + '/' + carousel.items().length);
}).owlCarousel({
	items:1,
	loop:true,
	margin:0,
	nav:true,
	navText: ['<i class="mi-chevron-left"></i>', '<i class="mi-chevron-right"></i>'] 
});
/*--
	Tooltip
------------------------*/
$('[data-toggle="tooltip"]').tooltip()
/*--
	Map Open Hide
------------------------*/
$('.btn-map-open').on('click', function(){
  $('.map-sidebar').animate({right: "0px",});
});
$('.map-sidebar .btn-close').on('click', function(){
  $('.map-sidebar').animate({right: "-430px",});
});
/*--
	Scroll Up
------------------------*/
$.scrollUp({
	scrollText: '<i class="mi-arrow-left"></i>',
	easingType: 'linear',
	scrollSpeed: 900,
	animation: 'fade'
});

	
});
})(jQuery);	
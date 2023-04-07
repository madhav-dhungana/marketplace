/*
Author       : Roshan Pathak
Template Name: Batuwa Ventures
Version      : 1.0
*/

(function($) {
    "use strict";
	
	// Stick Sidebar
	
	if ($(window).width() > 767) {
		if($('.theiaStickySidebar').length > 0) {
			$('.theiaStickySidebar').theiaStickySidebar({
			  // Settings
			  additionalMarginTop: 70
			});
		}
	}
	  
	// Search Bar

	$(document).on('click', '.searchbar .fa-search', function() {
		$(".togglesearch").toggle();
		$(".top-search").focus();
	});
	
	// Sidebar
	
	if($(window).width() <= 991){
	var Sidemenu = function() {
		this.$menuItem = $('.main-nav a');
	};
	
	function init() {
		var $this = Sidemenu;
		$('.main-nav a').on('click', function(e) {
			if($(this).parent().hasClass('has-submenu')) {
				e.preventDefault();
			}
			if(!$(this).hasClass('submenu')) {
				$('ul', $(this).parents('ul:first')).slideUp(350);
				$('a', $(this).parents('ul:first')).removeClass('submenu');
				$(this).next('ul').slideDown(350);
				$(this).addClass('submenu');
			} else if($(this).hasClass('submenu')) {
				$(this).removeClass('submenu');
				$(this).next('ul').slideUp(350);
			}
		});
	}

	// Sidebar Initiate
	init();
	}
	
	// Textarea Text Count
	
	var maxLength = 100;
	$('#review_desc').on('keyup change', function () {
		var length = $(this).val().length;
		 length = maxLength-length;
		$('#chars').text(length);
	});
	
	// Select 2
	
	if($('.select').length > 0) {
		$('.select').select2({
			minimumResultsForSearch: -1,
			width: '100%'
		});
	}
	
	// Date Time Picker
	
	// if($('.datetimepicker').length > 0) {
	// 	$('.datetimepicker').datetimepicker({
	// 		format: 'DD/MM/YYYY',
	// 		icons: {
	// 			up: "fas fa-chevron-up",
	// 			down: "fas fa-chevron-down",
	// 			next: 'fas fa-chevron-right',
	// 			previous: 'fas fa-chevron-left'
	// 		}
	// 	});
	// }
	
	// Floating Label

	if($('.floating').length > 0 ){
		$('.floating').on('focus blur', function (e) {
		$(this).parents('.form-focus').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
		}).trigger('blur');
	}
	
	// Mobile menu sidebar overlay
	
	$('body').append('<div class="sidebar-overlay"></div>');
	$(document).on('click', '#mobile_btn', function() {
		$('main-wrapper').toggleClass('slide-nav');
		$('.sidebar-overlay').toggleClass('opened');
		$('html').addClass('menu-opened');
		return false;
	});
	
	$(document).on('click', '.sidebar-overlay', function() {
		$('html').removeClass('menu-opened');
		$(this).removeClass('opened');
		$('main-wrapper').removeClass('slide-nav');
	});
	
	$(document).on('click', '#menu_close', function() {
		$('html').removeClass('menu-opened');
		$('.sidebar-overlay').removeClass('opened');
		$('main-wrapper').removeClass('slide-nav');
	});
	
	// Tooltip
	
	var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
	var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
	  return new bootstrap.Tooltip(tooltipTriggerEl)
	})
	
	// Add More Hours
	
    $(".hours-info").on('click','.trash', function () {
		$(this).closest('.hours-cont').remove();
		return false;
    });

    $(".add-hours").on('click', function () {
		
		var hourscontent = '<div class="row form-row hours-cont">' +
			'<div class="col-12 col-md-10">' +
				'<div class="row form-row">' +
					'<div class="col-12 col-md-6">' +
						'<div class="form-group">' +
							'<label>Start Time</label>' +
							'<select class="form-control">' +
								'<option>-</option>' +
								'<option>12.00 am</option>' +
								'<option>12.30 am</option>' + 
								'<option>1.00 am</option>' +
								'<option>1.30 am</option>' +
							'</select>' +
						'</div>' +
					'</div>' +
					'<div class="col-12 col-md-6">' +
						'<div class="form-group">' +
							'<label>End Time</label>' +
							'<select class="form-control">' +
								'<option>-</option>' +
								'<option>12.00 am</option>' +
								'<option>12.30 am</option>' +
								'<option>1.00 am</option>' +
								'<option>1.30 am</option>' +
							'</select>' +
						'</div>' +
					'</div>' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
		'</div>';
		
        $(".hours-info").append(hourscontent);
        return false;
    });
	
	// Content div min height set
	
	function resizeInnerDiv() {
		var height = $(window).height();	
		var header_height = $(".header").height();
		var footer_height = $(".footer").height();
		var setheight = height - header_height;
		var trueheight = setheight - footer_height;
		$(".content").css("min-height", trueheight);
	}
	
	if($('.content').length > 0 ){
		resizeInnerDiv();
	}

	$(window).on('resize', function(){
		if($('.content').length > 0 ){
			resizeInnerDiv();
		}
	});
	
	// Slick Slider
	if($('.developer-slider').length > 0) {
	$('.developer-slider').slick({
		infinite: true,
		slidesToShow: 4,
		slidesToScroll: 1,
		responsive: [
			{
				breakpoint: 1200,
				settings: {
					slidesToShow: 3
				}
			},
			{
			  breakpoint: 800,
			  settings: {
					slidesToShow: 2
				}
			},
			{
				breakpoint: 500,
				settings: {
					slidesToShow: 1
				}
			}		  
			]
		});
	}
	
	if($('.review-slider').length > 0) {
		$('.review-slider').slick({
			infinite: true,
			slidesToShow: 3,
			speed: 500,
			autoplay:false,
			responsive: [
				{
					breakpoint: 1200,
					settings: {
						slidesToShow: 2
					}
				},
				{
					breakpoint: 768,
					settings: {
						slidesToShow: 1
					}
				}
			]
		});
	}
	
	if($('.job-slider').length > 0) {
		$('.job-slider').slick({
			infinite: true,
			dots: true,
			prevArrow: false,
			nextArrow: false,
			slidesToShow: 1,
			speed: 500,
			autoplay:false,
			responsive: [
				{
					breakpoint: 1200,
					settings: {
						slidesToShow: 1
					}
				},
				{
					breakpoint: 800,
					settings: {
						slidesToShow: 1
					}
				}
			]
		});
	}
	
	if($('.reproject-slider').length > 0) {
		$('.reproject-slider').slick({
			infinite: true,
			slidesToShow: 2,
			speed: 500,
			arrows:false,
			dots: true,
			autoplay:false,
			responsive: [
				{
					breakpoint: 1400,
					settings: {
						slidesToShow: 2
					}
				},
				{
					breakpoint: 1300,
					settings: {
						slidesToShow: 1
					}
				}
			]
		});
	}
	
	// Date Range Picker
	if($('.bookingrange').length > 0) {
		var start = moment().subtract(6, 'days');
		var end = moment();

		function booking_range(start, end) {
			$('.bookingrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
		}

		$('.bookingrange').daterangepicker({
			startDate: start,
			endDate: end,
			ranges: {
				'Today': [moment(), moment()],
				'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
				'Last 7 Days': [moment().subtract(6, 'days'), moment()],
				'Last 30 Days': [moment().subtract(29, 'days'), moment()],
				'This Month': [moment().startOf('month'), moment().endOf('month')],
				'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
			}
		}, booking_range);

		booking_range(start, end);
	}
	// Chat

	var chatAppTarget = $('.chat-window');
	(function() {
		if ($(window).width() > 991)
			chatAppTarget.removeClass('chat-slide');
		
		$(document).on("click",".chat-window .chat-users-list a.media",function () {
			if ($(window).width() <= 991) {
				chatAppTarget.addClass('chat-slide');
			}
			return false;
		});
		$(document).on("click","#back_user_list",function () {
			if ($(window).width() <= 991) {
				chatAppTarget.removeClass('chat-slide');
			}	
			return false;
		});
	})();
	

	
	// select Box
	$(document).on('click', '.select-group .select-item .service-item', function() {
		$('.selected .service-item .fa').removeClass('fa-check');
		$('.select-item .service-item').removeClass('selected');
		$(this).addClass('selected');
	});
	
	// Preloader
	
	$(window).on('load', function () {
		if($('#loader').length > 0) {
			$('#loader').delay(350).fadeOut('slow');
			$('body').delay(350).css({ 'overflow': 'visible' });
		}
	})
	
	// readmore
	
	$(document).on('click', '.readmore', function() {
		var dots = document.getElementById("dots");
		var moreText = document.getElementById("more");
		var btnText = document.getElementById("myBtn");

		if (dots.style.display === "none") {
			dots.style.display = "inline";
			btnText.innerHTML = "Read more";
			moreText.style.display = "none";
		} else {
			dots.style.display = "none";
			btnText.innerHTML = "Read less";
			moreText.style.display = "inline";
		}
	});
	
	// Range slider
	
	if($('.slidercontainer').length > 0) {
		var slider = document.getElementById("myRange");
		var output = document.getElementById("demo");
		output.innerHTML = slider.value;

		slider.oninput = function() {
		  output.innerHTML = this.value;
		}
	}
	
	// Summernote
	
	if($('.summernote').length > 0) {
		$('.summernote').summernote({
			height: 200,                 // set editor height
			minHeight: null,             // set minimum height of editor
			maxHeight: null,             // set maximum height of editor
			focus: false ,
			toolbar: [
				// [groupName, [list of button]]
				['style', ['bold', 'italic', 'underline', 'clear']],
				['font', ['strikethrough', 'superscript', 'subscript']],
				['fontsize', ['fontsize']],
				['color', ['color']],
				['para', ['ul', 'ol', 'paragraph']],
				['height', ['height']]
			]			// set focus to editable area after initializing summernote
		});
	}
	
	// custom seleaction
	
	if($('#store').length > 0) {
		document.getElementById('store').storeID.onchange = function() {
			var newaction = this.value;
			document.getElementById('store').action = newaction;
		}
	};
	
	if($('#developers-slider').length > 0 ){
		$('#developers-slider').owlCarousel({
			items: 5,
	        margin: 30,
	        dots : false,
			nav: true,
			navText: [
				'<i class="fas fa-chevron-left"></i>',
				'<i class="fas fa-chevron-right"></i>'
			],
			loop: true,
			responsiveClass:true,
	        responsive: {
	          	0: {
	            	items: 1
	          	},
	          	768 : {
	            	items: 3
	          	},
	          	1170: {
	            	items: 4
	          	}
	        }
	    });
    }
	
	if($('#testimonial-slider').length > 0 ){
		$('#testimonial-slider').owlCarousel({
			items: 5,
	        margin: 30,
	        dots : false,
			nav: true,
			navText: [
				'<i class="fas fa-chevron-left"></i>',
				'<i class="fas fa-chevron-right"></i>'
			],
			loop: true,
			responsiveClass:true,
	        responsive: {
	          	0: {
	            	items: 1
	          	},
	          	768 : {
	            	items: 3
	          	},
	          	1170: {
	            	items: 3
	          	}
	        }
	    });
    }
	
	$(window).on('scroll', function () {
		var scroll = $(window).scrollTop();
		if (scroll < 100) {
			$(".header").removeClass("sticky");
		} else {
			$(".header").addClass("sticky");
		}
	});

	// Edit Experiance

	$('#edit_experiance').on('click',function(){
        $('.pro-new').css('display','block');
        $('.pro-text').css('display','none');
    });

	$('.profile-cancel-btn').on('click',function(){
       $('.pro-new').css('display','none');
       $('.pro-text').css('display','block');
   	});
   
   	// Overview
	$('#edit_overview').on('click',function(){
       $('.pro-new1').css('display','block');
       $('.pro-text1').css('display','none');
   	});

	$('.profile-cancel-btn').on('click',function(){
       $('.pro-new1').css('display','none');
       $('.pro-text1').css('display','block');
   	});
   
   	// Overview

   	$('#edit_education').on('click',function(){
	   $('.pro-new2').css('display','block');
	   $('.pro-text2').css('display','none');
    });

	$('.profile-cancel-btn').on('click',function(){
       $('.pro-new2').css('display','none');
       $('.pro-text2').css('display','block');
   	});

	$('#edit_name').on('click',function(){
        $('.pro-new3').css('display','block');
        $('.pro-text3').css('display','none');
    });

	$('.profile-cancel-btn').on('click',function(){
        $('.pro-new3').css('display','none');
        $('.pro-text3').css('display','block');
    });
	
})(jQuery);
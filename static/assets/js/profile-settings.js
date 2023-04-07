
(function($) {
    "use strict";
	
	// Looking Member Options Show 
	
	$('#member_id input[name="member"]').on('click', function() {
		if ($(this).val() == 'individual'){
			$('#member_no').hide();
		}
		if ($(this).val() == 'company') {
			$('#member_no').hide();
		}		
		if ($(this).val() == 'developers') {
			$('#member_no').show();
		}
		else {
		}
	});
	
	
	$('#work_type input[name="work"]').on('click', function() {
		if ($(this).val() == 'distant') {
			$('#distant').show();
			$('#local').hide();
		}
		if ($(this).val() == 'local') {
			$('#distant').hide();
			$('#local').show();
		}		
		if ($(this).val() == 'upload') {
			$('#distant').hide();
			$('#local').hide();
		}
		else {
		}
	});
	
	$('#job_type input[name="job"]').on('change', function() {
		if ((this.checked == true) && ($(this).val() == 'job_2')) {
			$('#job_date').show();
		}
		else if ((this.checked == false) && ($(this).val() == 'job_2')){
			$('#job_date').hide();
		}
	});
	
	$('#price_type').on('change', function() {
		if ($(".price-cont select option:selected").val() == '1') {
			$('#price_id').show();
			$('#hour_id').hide();
		}
		else if ($(".price-cont select option:selected").val() == '2') {
			$('#price_id').hide();
			$('#hour_id').show();
		}		
		else if ($(".price-cont select option:selected").val() == '3') {
			$('#price_id').hide();
			$('#hour_id').hide();
		}		
		else if ($("select option:selected").val() == '0') {
			$('#price_id').hide();
			$('#hour_id').hide();
		}
	});
	
	$('#pro_period input[name="period"]').on('click', function() {
		if ($(this).val() == 'period') {
			$('#period_date').hide();
		}
		else if ($(this).val() == 'job') {
			$('#period_date').show();
		}	
	});
	
	// Education Add More
	
    $(".billing-method").on('click','.trash', function () {
		$(this).closest('.education-cont').remove();
		return false;
    });

    $(".add-bill").on('click', function () {
		
		var billingcontent = '<div class="row form-row education-cont">' +
			'<div class="col-12 col-md-10 col-lg-11">' +
				'<div class="row form-row">' +
					'<div class="col-12 col-md-12">' +
						'<div class="form-group">' +
							'<label class="d-md-block d-sm-none d-none">&nbsp;</label>' +
							'<input type="text" class="form-control">' +
						'</div>' +
					'</div>' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2 col-lg-1"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
		'</div>';
		
        $(".billing-method").append(billingcontent);
        return false;
    });
	
	// Experience Add More
	
    $(".links-info").on('click','.trash', function () {
		$(this).closest('.links-cont').remove();
		return false;
    });

    $(".add-links").on('click', function () {
		
		var experiencecontent = '<div class="row form-row links-cont">' +
			'<div class="col-12 col-md-11 col-lg-11">' +
				'<div class="form-group">' +
					'<label>Add</label>' +
					'<input type="text" class="form-control">' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-1 col-lg-1"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
		'</div>';
		
        $(".links-info").append(experiencecontent);
        return false;
    });
	
	// Award Add 
	
    $(".award-info").on('click','.trash-icon', function () {
		$(this).closest('.award-cont').remove();
		return false;
    });

    $(".add-award").on('click', function () {
		
		var awardcontent = '<div class="form-row align-items-center award-cont">' +
	
		'<div class="form-group col-md-5">' +
				'<input type="text" name="awards_name[]" class="form-control">' +
			'</div>' +
			'<div class="form-group col-md-3">' +
				'<input type="date" name="awards_date[]" class="form-control">' +
			'</div>' +
			'<div class="form-group col-md-2"><a href="#" class="btn trash-icon"><i class="far fa-trash-alt"></i></a></div>' +
		'</div>';
		
        $(".award-info").append(awardcontent);
        return false;
    });
	
	// Add Language 
	
    $(".lang-info").on('click','.trash-icon', function () {
		$(this).closest('.lang-cont').remove();
		return false;
    });

    $(".add-lang").on('click', function () {
		
		var langcontent = '<div class="form-row align-items-center lang-cont">' +
			'<div class="form-group col-md-7">' +
				'<input placeholder="language name" type="text" name="lang[]" class="form-control">' +
			'</div>' +
			'<div class="form-group col-md-3">' +
				'<input placeholder="fluency" name="fluency[]" type="number" min="1" max="100" class="form-control">' +
			'</div>' +
			'<div class="form-group col-md-2"><a href="#" class="btn trash-icon"><i class="far fa-trash-alt"></i></a></div>' +
		'</div>';
		
        $(".lang-info").append(langcontent);
        return false;
    });
	
	// Add skill 
	
    $(".skill-info").on('click','.trash-icon', function () {
		$(this).closest('.skill-cont').remove();
		return false;
    });

    $(".skill-add").on('click', function () {
		
		var skillcontent = '<div class="form-row align-items-center skill-cont">' +
			'<div class="form-group col-md-10">' +
				'<input type="text" name="user_skills[]" class="form-control">' +
			'</div>' +
			'<div class="form-group col-md-2"><a href="#" class="btn trash-icon"><i class="far fa-trash-alt"></i></a></div>' +
		'</div>';
		
        $(".skill-info").append(skillcontent);
        return false;
    });
	
	// Add Experience 
	
    $(".exp-info").on('click','.trash-icon', function () {
		$(this).closest('.exp-cont').remove();
		return false;
    });

    $(".add-exp").on('click', function () {
		
		var expcontent = '<div class="form-row align-items-center exp-cont">' +
			'<div class="form-group col-md-6">' +				
				'<label>Title</label>' +
				'<input type="text" class="form-control">' +
			'</div>' +
			'<div class="form-group col-md-6">' +				
				'<label>Company name</label>' +
				'<input type="text" class="form-control">' +
			'</div>' +
			'<div class="form-group col-md-6">' +			
				'<label>Start date</label>' +
				'<input type="text" class="form-control datetimepicker">' +
			'</div>' +
			'<div class="form-group col-md-6">' +			
				'<label>End date</label>' +
				'<input type="text" class="form-control datetimepicker">' +
			'</div>' +
			'<div class="form-group col-md-12">' +			
				'<label class="custom_check">' +
				'<input type="checkbox" name="rem_password">' +
				'<span class="checkmark"></span> Im currently working here' +
				'</label>' +
			'</div>' +
			'<div class="form-group col-md-12">' +			
				'<label>Summary</label>' +
				'<textarea class="form-control" rows="5"></textarea>' +
			'</div>' +
			'<div class="form-group col-md-2"><a href="#" class="btn trash-icon"><i class="far fa-trash-alt"></i></a></div>' +
		'</div>';
		
        $(".exp-info").append(expcontent);
        return false;
    });
	
	// Tax Add More
	
    $(".tax-info").on('click','.trash', function () {
		$(this).closest('.tax-cont').remove();
		return false;
    });

    $(".add-tax").on('click', function () {
	
		var taxcontent = '<div class="form-row tax-cont">' +
			'<div class="col-12 col-md-3 col-lg-3">' +
				'<div class="form-group">' +
					'<input type="text" class="form-control">' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-4 col-lg-4">' +
				'<div class="form-group">' +
					'<input type="text" class="form-control">' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-4 col-lg-4">' +
				'<div class="form-group">' +
					'<input type="text" class="form-control">' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-1 col-lg-1"><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
		'</div>';
		
        $(".tax-info").append(taxcontent);
        return false;
    });
	
	// Awards Add More
	
    $(".awards-info").on('click','.trash', function () {
		$(this).closest('.awards-cont').remove();
		console.log('clicked')
		return false;
    });

    $(".add-award").on('click', function () {

        var regcontent = '<div class="row form-row awards-cont">' +
			'<div class="col-12 col-md-5">' +
				'<div class="form-group">' +
					'<label>Awards</label>' +
					'<input type="text" class="form-control">' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-5">' +
				'<div class="form-group">' +
					'<label>Year</label>' +
					'<input type="text" class="form-control">' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2">' +
				'<label class="d-md-block d-sm-none d-none">&nbsp;</label>' +
				'<a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a>' +
			'</div>' +
		'</div>';
		
        $(".awards-info").append(regcontent);
        return false;
    });
	
	// Membership Add More
	
    $(".membership-info").on('click','.trash', function () {
		$(this).closest('.membership-cont').remove();
		return false;
    });

    $(".add-membership").on('click', function () {

        var membershipcontent = '<div class="row form-row membership-cont">' +
			'<div class="col-12 col-md-10 col-lg-5">' +
				'<div class="form-group">' +
					'<label>Memberships</label>' +
					'<input type="text" class="form-control">' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2 col-lg-2">' +
				'<label class="d-md-block d-sm-none d-none">&nbsp;</label>' +
				'<a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a>' +
			'</div>' +
		'</div>';
		
        $(".membership-info").append(membershipcontent);
        return false;
    });
	
	// Registration Add More
	
    $(".registrations-info").on('click','.trash', function () {
		$(this).closest('.reg-cont').remove();
		return false;
    });

    $(".add-reg").on('click', function () {

        var regcontent = '<div class="row form-row reg-cont">' +
			'<div class="col-12 col-md-5">' +
				'<div class="form-group">' +
					'<label>Registrations</label>' +
					'<input type="text" class="form-control">' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-5">' +
				'<div class="form-group">' +
					'<label>Year</label>' +
					'<input type="text" class="form-control">' +
				'</div>' +
			'</div>' +
			'<div class="col-12 col-md-2">' +
				'<label class="d-md-block d-sm-none d-none">&nbsp;</label>' +
				'<a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a>' +
			'</div>' +
		'</div>';
		
        $(".registrations-info").append(regcontent);
        return false;
    });
	
	$(".badge").on('click','[data-role=remove]', function () {
		$(this).closest('.badge').remove();
		return false;
    });

	
})(jQuery);
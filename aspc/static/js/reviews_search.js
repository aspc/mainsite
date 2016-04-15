var ASPC = ASPC || {};
ASPC.ReviewsSearch = ASPC.ReviewsSearch || {};

$(document).ready(function () {
	ASPC.ReviewsSearch.dropdown = $('#object_type_dropdown');

	if (ASPC.ReviewsSearch.dropdown[0].value == 'course') {
		$('#review_search_form-professorname').toggleClass('hidden');
	}
	else if (ASPC.ReviewsSearch.dropdown[0].value == 'professor') {
		$('#review_search_form-coursename').toggleClass('hidden');
	}

	ASPC.ReviewsSearch.dropdown.on('change', function () {
		$('#review_search_form-coursename').toggleClass('hidden');
		$('#review_search_form-professorname').toggleClass('hidden');

		if (ASPC.ReviewsSearch.dropdown[0].value == 'course') {
			$('#review_search_form-professorname input')[0].value = '';
		}
		else if (ASPC.ReviewsSearch.dropdown[0].value == 'professor') {
			$('#review_search_form-coursename input')[0].value = '';
		}
	});
});
var ASPC = ASPC || {};
ASPC.ReviewsSearch = ASPC.ReviewsSearch || {};

$(document).ready(function () {
	ASPC.ReviewsSearch.dropdown = $('#object_type_dropdown');

	ASPC.ReviewsSearch.dropdown.on('change', function () {
		$('#review_search_form-campus').toggleClass('hidden');
		$('#review_search_form-coursename').toggleClass('hidden');
		$('#review_search_form-professorname').toggleClass('hidden');
	});
});
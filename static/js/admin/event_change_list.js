// Styles the moderation table once the DOM loads for easy viewing of what needs to be approved
window.onload = function () {
	var elements = $('[name^=form-][name$=-status]');
	$.each(elements, function (index, element) {
		element = $(element);
		switch (element.children('option[selected=selected]').val()) {
			case 'approved':
				element.parent().addClass('approved');
				break;
			case 'denied':
				element.parent().addClass('denied');
				break;
			case 'pending':
				element.parent().addClass('pending');
				break;
		}
	});
};
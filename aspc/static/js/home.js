/*
	JS for the homepage
*/

// Set up namespacing
var ASPC = ASPC || {};
ASPC.Home = ASPC.Home || {};


ASPC.Home.update_event_description = function (event) {
	// Declares a reference to the event_info div that was clicked
	var event_info = $(event.currentTarget).children('aside');

	// Updates the events_description panel with the appropriate information
	if ($('.event_info').length < 2) {
		$('#events_description_title').html(event_info.children('h3').html());
		$('#events_description_host').html('');
		$('#events_description_location').html('');
		$('#events_description_description').html(event_info.children('p.description').html().slice(0, 50) + '... ' + event_info.children('p.more_link').html());
	}
	else {
		$('#events_description_title').html(event_info.children('h3').html());
		$('#events_description_host').html('<b>Host:</b> ' + event_info.children('p.host').html());
		$('#events_description_location').html('<b>Location:</b> ' + event_info.children('p.location').html());
		$('#events_description_more_link').html(event_info.children('p.more_link').html());

		// Checks the number of events today so as to know how much space is available to display long descriptions
		var description_text = event_info.children('p.description').html();
		switch ($('.event_info').length) {
			case 2:
				if (description_text.length > 150) {
					$('#events_description_description').html(description_text.slice(0, 150) + '...');
				}
				else {
					$('#events_description_description').html(description_text);
				}
				break;
			case 3:
				if (description_text.length > 300) {
					$('#events_description_description').html(description_text.slice(0, 300) + '...');
				}
				else {
					$('#events_description_description').html(description_text);
				}
				break;
			case 4:
				if (description_text.length > 450) {
					$('#events_description_description').html(description_text.slice(0, 450) + '...');
				}
				else {
					$('#events_description_description').html(description_text);
				}
				break
			default:
				$('#events_description_description').html(description_text);
				break;
		}
	}

	// Removes the active marker from the old event
	$('#events_list').find('li').removeClass('active');

	// Sets the new event as active
	event_info.parents('li').addClass('active');
};

window.onload = function () {
	// Bind listeners to the event_info elements to update the event description div when clicked
	$('.event_info').on('click', ASPC.Home.update_event_description);

	// Initializes the events_description panel
	$($('.event_info')[0]).trigger('click');
};
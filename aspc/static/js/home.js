/*
	JS for the homepage
*/

// Set up namespacing
var ASPC = ASPC || {};
ASPC.Home = ASPC.Home || {};


ASPC.Home.update_event_description = function (event) {
	// Declares a reference to the event_info div that was clicked
	var event_info = $(event.currentTarget).children('aside');

	// Updates teh events_description panel with the appropriate information
	$('#events_description_title').html(event_info.children('h3').html());
	$('#events_description_host').html(event_info.children('p.host').html());
	$('#events_description_location').html(event_info.children('p.location').html());
	$('#events_description_description').html(event_info.children('p.description').html());

	// Removes the active marker from the old event
	$('#events_list').find('li').removeClass('active');

	// Sets the new event as active
	event_info.parents('li').addClass('active');
};

window.onload = function () {
	$(".event_info").on('click', ASPC.Home.update_event_description);
};
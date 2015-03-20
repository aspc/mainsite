// ASPC namespace
var ASPC = ASPC || {};

/**
 * @module
 * @description Methods for the homepage widgets
 */
ASPC.home = function () {
	/**
	 * @private
	 */
	var my = {
		self: this
	};

	/**
	 * @public
	 * @description Aggregates the initialization for all the homepage widgets
	 */
	my.self.init = function () {
		ASPC.Events.init();
	};

	return my.self;
};

/**
 * @module
 * @description Methods for the Today's Events widget
 */
ASPC.events = function () {
	/**
	 * @private
	 */
	var my = {
		self: this
	};

	/**
	 * @public
	 * @description Binds the appropriate event handlers based on whether using desktop or mobile
	 */
	my.self.init = function () {
		// Bind listeners to the event_info elements to update the event description div when clicked
		if ($(window).width() > 767) { // Using the desktop site...
			$('.event_info').on('click', my.self.update_event_description);

			// Initializes the events_description panel
			$($('.event_info')[0]).trigger('click');
		}
		else { // Using the mobile site
			$('.event_info').on('click', my.self.go_to_event);
		}
	};

	/**
	 * @public
	 * @description Updates the event description with the deatils of the event that is active
	 */
	my.self.update_event_description = function (event) {
		// The event_info div that was clicked
		var event_info = $(event.currentTarget).children('aside'),
			events_list_length = $('#events_list').find('li').length;

		// Updates the events_description panel with the appropriate information
		if (events_list_length === 1) {
			// If there is only one event showing, present nothing except the shortened description div
			$('#events_description_title').html(event_info.children('h3').html());
			$('#events_description_host').html('');
			$('#events_description_location').html('');
			$('#events_description_more_link').html('');
			$('#events_description_description').html('');

			// Calculate how much description we have space to show
			// Check the number of events today so as to know how much space is available to display long descriptions
			var description_text = event_info.children('p.description').html(),
				events_description_max_height = 95, // Each li element is 95px high
				i = 0;

			// Subtract the height (including margins) of the title div
			events_description_max_height -= $('#events_description_title').outerHeight(true);

			// Slowly add text to the div element, making sure not to add too much
			while ($('#events_description_description').outerHeight(true) < events_description_max_height && i <= description_text.length) {
				$('#events_description_description').html(description_text.slice(0, ++i));
			}

			// Append an ellipsis and the more link
			$('#events_description_description').html($('#events_description_description').html() + '&hellip;' + event_info.children('p.more_link').html());
		}
		else {
			// Set up the default text for all the elements except the description element
			$('#events_description_title').html(event_info.children('h3').html());
			$('#events_description_host').html('<b>Host:</b> ' + event_info.children('p.host').html());
			$('#events_description_location').html('<b>Location:</b> ' + event_info.children('p.location').html());
			$('#events_description_more_link').html(event_info.children('p.more_link').html());
			$('#events_description_description').html('');

			// Calculate how much description we have space to show
			// Check the number of events today so as to know how much space is available to display long descriptions
			var description_text = event_info.children('p.description').html(),
				events_description_max_height = events_list_length * 95, // Each li element is 95px high
				i = 0;

			// Subtract the height (including margins) of the non-description divs
			events_description_max_height -=
				$('#events_description_title').outerHeight(true) +
				$('#events_description_host').outerHeight(true) +
				$('#events_description_location').outerHeight(true) +
				$('#events_description_description').outerHeight(true) +
				$('#events_description_more_link').outerHeight(true);

			// Slowly add text to the div element, making sure not to add too much
			while ($('#events_description_description').outerHeight(true) < events_description_max_height && i <= description_text.length) {
				$('#events_description_description').html(description_text.slice(0, ++i));
			}

			// Append an ellipsis if the description was truncated
			if (i < description_text.length) {
				$('#events_description_description').html($('#events_description_description').html() + '&hellip;');
			}
		}

		// Removes the active marker from the old event
		$('#events_list').find('li').removeClass('active');

		// Sets the new event as active
		event_info.parents('li').addClass('active');
	};

	/**
	 * @public
	 * @description Opens the full event page when an event is clicked (only on mobile)
	 */
	my.self.go_to_event = function (event) {
		// The event_info div that was clicked
		var event_info = $(event.currentTarget).children('aside');

		window.location.href = event_info.find('a').attr('href');
	};

	return my.self;
};

ASPC.Events = new ASPC.events();
ASPC.Home = new ASPC.home();

$('document').ready(ASPC.Home.init);
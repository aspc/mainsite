// ASPC namespace
var ASPC = ASPC || {};

/**
 * @module
 * @description Methods to handle the submission and validation of Facebook events, Facebook pages, and manual events
 */
ASPC.events = function () {
	/**
	 * @private
	 */
	var my = {
		self: this,
		init_calendar: function () {
			$('#calendar').fullCalendar({
				header: {
					left: 'prev,next today',
					center: 'title',
					right: 'month,agendaWeek,agendaDay'
				},
				minTime: my.self.calendar_data.earliest_event_time,
				maxTime: my.self.calendar_data.latest_event_time + 3,
				allDaySlot: false,
				editable: false,
				events: my.self.calendar_data.events
			});
		},
		init_datepicker: function () {
			$('#manual_event_start').datetimepicker({
				controlType: 'select',
				timeFormat: 'hh:mm tt',
				dateFormat: 'yy-mm-dd'
			});
			$('#manual_event_end').datetimepicker({
				controlType: 'select',
				timeFormat: 'hh:mm tt',
				dateFormat: 'yy-mm-dd'
			});
		},
		init_html5_datepicker: function () {
			$('#manual_event_start').attr('type', 'datetime-local');
			$('#manual_event_end').attr('type', 'datetime-local');
		}
	};

	/**
	 * @public
	 * @description Configures the page for desktop or mobile and inits the app
	 */
	my.self.init = function () {
		// Grabs the csrf_token from the DOM (something we pass along to the server to authenticate requests)
		ASPC.csrf_token = $('input[name=csrfmiddlewaretoken]').val();

		// Init the jQuery calendar on the page for events display, and the datepicker for manual event submission
		my.init_calendar();

		if (ASPC.Settings.is_mobile) {
			my.init_html5_datepicker();
		}
		else {
			my.init_datepicker();
		}
	};

	/**
	 * @public
	 * @description Holds the data for the calendar that is loaded by Django when the template is compiled
	 */
	my.self.calendar_data = {};

	/**
	 * @public
	 * @description Submits a Facebook event
	 */
	my.self.submit_facebook_event = function () {
		var url = $('#facebook_event_url').val() || '';

		if (!url.match(/https?:\/\/(?:www\.)?facebook\.com\/events\/\d+(?:\/\S+)?/)) {
			alert('You must enter a valid Facebook event URL!');
			return false;
		}

		// Give indication of async request to the user
		$('#facebook_event_submit_button').attr('disabled', true);
		$('#facebook_event_submit_loading').show();

		$.ajax({
			url: 'event/',
			type: 'POST',
			beforeSend: function (request) {
				request.setRequestHeader('X-CSRFToken', ASPC.csrf_token);
			},
			data: {
				event_source: 'facebook',
				event_url: url
			},
			timeout: 10000,
			success: function (data) {
				console.log('success');
				$('#facebook_event_submit_button').attr('disabled', false);
				$('#facebook_event_submit_loading').hide();
				new_event = JSON.parse(data)[0].fields;
				alert('Thank you. Your event "' + new_event.name + '" has been added to the queue for approval. It will appear shortly.');
				$('#facebook_event_url').val('');
				return false;
			},
			error: function (jqXHR, t, e) {
				console.log('error');
				$('#facebook_event_submit_button').attr('disabled', false);
				$('#facebook_event_submit_loading').hide();
				alert('Something went wrong! Are you sure your Facebook event is public? Error:\n' + (jqXHR.responseText || e));
				return false;
			}
		});
	};

	/**
	 * @public
	 * @description Submits a manual event
	 */
	my.self.submit_manual_event = function () {
		var manual_event = {
			event_source: 'manual',
			name: $('#manual_event_name').val(),
			start: $('#manual_event_start').val(),
			end: $('#manual_event_end').val(),
			location: $('#manual_event_location').val(),
			description: $('#manual_event_description').val(),
			host: $('#manual_event_host').val(),
			url: $('#manual_event_url').val()
		};

		// Validate that all the appropriate event information has been added correctly
		if (manual_event.name.length === 0) {
			alert('You must enter an event name!');
			return false;
		} else if (manual_event.start.length === 0) {
			alert('You must enter a start time!');
			return false;
		} else if (manual_event.location.length === 0) {
			alert('You must enter a location!');
			return false;
		} else if (manual_event.description.length === 0) {
			alert('You must enter a description!');
			return false;
		} else if (manual_event.host.length === 0) {
			alert('You must enter a host name!');
			return false;
		} else if (manual_event.url.length && !manual_event.url.match(/((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/)) {
			alert('You must enter a valid URL!');
			return false;
		}

		// Checks and reformats the times, depending on which datepicker was used to enter them (desktop widget or native mobile HTML5 one)
		// All times should be sent to the server in the format YYYY-MM-DDTHH:MM
		if (!ASPC.Settings.is_mobile) {
			if (!(start_time = manual_event.start.match(/^(\d{4})-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01]) ((?:0\d)|(?:1[0-2])):([0-5]\d) ((?:a|p)m)$/))) {
				alert('You must enter a start time in the format MM/DD/YYYY HH:MM tt!');
				return false;
			}
			else { // Reformat the time string
				if (start_time[6] === 'pm') {
					start_time[5] = parseInt(start_time[5], 10) + 12;
				}
				manual_event.start = start_time[1] + '-' + start_time[2] + '-' + start_time[3] + 'T' + start_time[4] + ':' + start_time[5];
			}
			if (manual_event.end) {
				if (!(end_time = manual_event.end.match(/^(\d{4})-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01]) ((?:0\d)|(?:1[0-2])):([0-5]\d) ((?:a|p)m)$/))) {
					alert('You must enter an end time in the format MM/DD/YYYY HH:MM tt!');
					return false;
				}
				else { // Reformat the time string
					if (end_time[6] === 'pm') {
						end_time[5] = parseInt(end_time[5], 10) + 12;
					}
					manual_event.end = end_time[1] + '-' + end_time[2] + '-' + end_time[3] + 'T' + end_time[4] + ':' + end_time[5];
				}
			}
		}
		else {
			if (!manual_event.start.match(/^(\d{4})-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])T([01]\d|2[0-3]):([0-5]\d)$/)) {
				// Good faith belief that modern browsers implement the HTML5 spec consistently (this error message should never appear)
				alert('You must enter a start time in the format YYYY-MM-DDTHH:MM!');
				return false;
			}
			if (manual_event.end) {
				if (!manual_event.end.match(/^(\d{4})-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])T([01]\d|2[0-3]):([0-5]\d)$/)) {
					// Good faith belief that modern browsers implement the HTML5 spec consistently (this error message should never appear)
					alert('You must enter an end time in the format YYYY-MM-DDTHH:MM!');
					return false;
				}
			}
		}

		// Reformat the URL if necessary (ensure it begins with http:// so the browser doesn't think it's a relative URL)
		if (manual_event.url.length && !/^https?:\/\//i.test(manual_event.url)) {
			manual_event.url = 'http://' + manual_event.url;
		}

		// Give indication of async request to the user
		$('#manual_submit_button').attr('disabled', true);
		$('#manual_submit_loading').show();

		$.ajax({
			url: 'event/',
			type: 'POST',
			beforeSend: function (request) {
				request.setRequestHeader('X-CSRFToken', ASPC.csrf_token);
			},
			data: manual_event,
			timeout: 10000,
			success: function (data) {
				console.log('success');
				$('#manual_submit_button').attr('disabled', false);
				$('#manual_submit_loading').hide();
				new_event = JSON.parse(data)[0].fields;
				alert('Thank you. Your event "' + new_event.name + '" has been added to the queue for approval. It will appear shortly.');
				$('#manual_event_name').val('');
				$('#manual_event_start').val('');
				$('#manual_event_end').val('');
				$('#manual_event_location').val('');
				$('#manual_event_description').val('');
				$('#manual_event_host').val('');
				$('#manual_event_url').val('');
				return false;
			},
			error: function (jqXHR, t, e) {
				console.log('error');
				$('#manual_submit_button').attr('disabled', false);
				$('#manual_submit_loading').hide();
				alert('Something went wrong! Error:\n' + (jqXHR.responseText || e));
				return false;
			}
		});
	};

	/**
	 * @public
	 * @description Submits a Facebook page
	 */
	my.self.submit_facebook_page = function () {
		var url = $('#facebook_page_url').val() || '';

		if (!url.match(/(?:https?:\/\/(?:www\.)?)?facebook\.com\/\w+(?:\/\S+)?/)) {
			alert('You must enter a valid Facebook page URL!');
			return false;
		}

		// Give indication of async request to the user
		$('#facebook_page_submit_button').attr('disabled', true);
		$('#facebook_page_submit_loading').show();

		$.ajax({
			url: 'facebook_page/',
			type: 'POST',
			beforeSend: function (request) {
				request.setRequestHeader('X-CSRFToken', ASPC.csrf_token);
			},
			data: {
				page_url: url
			},
			timeout: 10000,
			success: function (data) {
				console.log('success');
				$('#facebook_page_submit_button').attr('disabled', false);
				$('#facebook_page_submit_loading').hide();
				new_page = JSON.parse(data)[0].fields;
				alert('Thank you. Your page "' + new_page.name + '" has been added to the watchlist. Its events will appear automatically.');
				$('#facebook_page_url').val('');
				return false;
			},
			error: function (jqXHR, t, e) {
				console.log('error');
				$('#facebook_page_submit_button').attr('disabled', false);
				$('#facebook_page_submit_loading').hide();
				alert('Something went wrong! Are you sure your Facebook page is public? Error:\n' + (jqXHR.responseText || e));
				return false;
			}
		});
	};

	return my.self;
};


ASPC.Events = new ASPC.events();

$('document').ready(ASPC.Events.init);
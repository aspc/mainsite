/*
	JS for the events app
*/

// Set up namespacing
var ASPC = ASPC || {};
ASPC.Events = ASPC.Events || {};

window.onload = function () {
	// Grabs the csrf_token from the DOM (something we pass along to the server to authenticate requests)
	ASPC.csrf_token = $('input[name=csrfmiddlewaretoken]').val();

	// Init the jQuery calendar on the page for events display
	ASPC.Events.init_calendar();
};

ASPC.Events.init_calendar = function () {
	$('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay'
		},
		minTime: ASPC.Events.calendar_data.earliest_event_time,
		maxTime: ASPC.Events.calendar_data.latest_event_time + 3,
		allDaySlot: false,
		editable: false,
		events: ASPC.Events.calendar_data.events
	});
};

ASPC.Events.submit_facebook_event = function () {
	var url = $('#facebook_event_url').val() || '';

	if (!url.match(/https?:\/\/(?:www\.)?facebook\.com\/events\/\d+(?:\/\S+)?/)) {
		alert('You must enter a valid Facebook URL!');
		return false;
	}

	$.ajax({
		url: 'event/',
		type: 'POST',
		beforeSend: function (request) {
			request.setRequestHeader("X-CSRFToken", ASPC.csrf_token);
		},
		data: {
			event_source: 'facebook',
			event_url: url
		},
		timeout: 10000,
		success: function (data) {
			console.log('success');
			new_event = JSON.parse(data)[0].fields;
			alert('Thank you. Your event "' + new_event.name + '" has been added to the queue for approval. It will appear shortly.');
			$('#facebook_event_url').val('');
			return false;
		},
		error: function (jqXHR, t, e) {
			console.log('error');
			alert('Something went wrong! Error:\n' + (jqXHR.responseText || e));
			return false;
		}
	});
};

ASPC.Events.submit_manual_event = function () {
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

	// Validate the all the appropriate event information has been added correctly
	if (manual_event.name.length === 0) {
		alert('You must enter an event name!');
		return false;
	} else if (manual_event.start.length === 0) {
		alert('You must enter a start time!');
		return false;
	} else if (!manual_event.start.match(/^(\d{4})[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01]) ([01]\d|2[0-3]):([0-5]\d)$/)) {
		alert('You must enter a start time in the format YYYY-MM-DD HH:MM!');
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

	// Reformat the times if necessary
	var start_time = manual_event.start.match(/^(\d{4})[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01]) ([01]\d|2[0-3]):([0-5]\d)$/);
	manual_event.start = start_time[1] + '-' + start_time[2] + '-' + start_time[3] + 'T' + start_time[4] + ':' + start_time[5];
	if (end_time = manual_event.end.match(/^(\d{4})[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01]) ([01]\d|2[0-3]):([0-5]\d)$/)) {
		manual_event.end = end_time[1] + '-' + end_time[2] + '-' + end_time[3] + 'T' + end_time[4] + ':' + end_time[5];
	}
	else {
		alert('You must enter an end time in the format YYYY-MM-DD HH:MM!');
		return false;
	}

	$.ajax({
		url: 'event/',
		type: 'POST',
		beforeSend: function (request) {
			request.setRequestHeader("X-CSRFToken", ASPC.csrf_token);
		},
		data: manual_event,
		timeout: 10000,
		success: function (data) {
			console.log('success');
			new_event = JSON.parse(data)[0].fields;
			alert('Thank you. Your event "' + new_event.name + '" has been added to the queue for approval. It will appear shortly.');
			return false;
		},
		error: function (jqXHR, t, e) {
			console.log('error');
			alert('Something went wrong! Error:\n' + (jqXHR.responseText || e));
			return false;
		}
	});
};

ASPC.Events.submit_facebook_page = function () {
	var url = $('#facebook_page_url').val() || '';

	if (!url.match(/(?:https?:\/\/(?:www\.)?)?facebook\.com\/\w+(?:\/\S+)?/)) {
		alert('You must enter a valid Facebook Page URL!');
		return false;
	}

	$.ajax({
		url: 'facebook_page/',
		type: 'POST',
		beforeSend: function (request) {
			request.setRequestHeader("X-CSRFToken", ASPC.csrf_token);
		},
		data: {
			page_url: url
		},
		timeout: 10000,
		success: function (data) {
			console.log('success');
			new_page = JSON.parse(data)[0].fields;
			alert('Thank you. Your page "' + new_page.name + '" has been added to the watchlist. Its events will appear automatically.');
			$('#facebook_page_url').val('');
			return false;
		},
		error: function (jqXHR, t, e) {
			console.log('error');
			alert('Something went wrong! Error:\n' + (jqXHR.responseText || e));
			return false;
		}
	});
};
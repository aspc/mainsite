/*
	JS for the events app
*/

// Set up namespacing
var ASPC = ASPC || {};
ASPC.Events = ASPC.Events || {};

// Grabs the csrf_token from the DOM (something we pass along to authenticate the request)
window.onload = function () {
	ASPC.csrf_token = $('input[name=csrfmiddlewaretoken]').val();

	ASPC.Events.init_calendar();
};

ASPC.Events.init_calendar = function () {
	$('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay'
		},
		minTime: 8,
		maxTime: 24,
		allDaySlot: false,
		editable: false,
		events: ASPC.Events.calendar_data
	});
};

ASPC.Events.submit_facebook_event = function () {
	var url = $('#facebook_event_url').val() || '';

	if (url.length === 0) {
		alert('You must enter a valid Facebook URL!');
		return false;
	}

	$.ajax({
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
			$('#facebook_event_submit_status').html('Thank you. Your event "' + new_event.name + '" has been added to the queue for approval. It will appear shortly.');
			$('#facebook_event_url').val('');
			return false;
		},
		error: function (jqXHR, t, e) {
			console.log('error');
			$('#facebook_event_submit_status').html('Something went wrong! Are you sure the event you submitted is public?');
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
	}

	$.ajax({
		type: 'POST',
		beforeSend: function (request) {
			request.setRequestHeader("X-CSRFToken", ASPC.csrf_token);
		},
		data: manual_event,
		timeout: 10000,
		success: function (data) {
			console.log('success');
			new_event = JSON.parse(data)[0].fields;
			$('#manual_event_submit_status').html('Thank you. Your event "' + new_event.name + '" has been added to the queue for approval. It will appear shortly.');
			return false;
		},
		error: function (jqXHR, t, e) {
			console.log('error');
			$('#manual_event_submit_status').html('Something went wrong! Please try again.');
			return false;
		}
	});
};

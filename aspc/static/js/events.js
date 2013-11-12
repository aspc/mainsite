/*
	JS for the events app
*/

// Set up namespacing
var ASPC = ASPC || {};
ASPC.Events = ASPC.Events || {};

// Grabs the csrf_token from the DOM (something we pass along to authenticate the request)
window.onload = function () {
	ASPC.csrf_token = $('input[name=csrfmiddlewaretoken]').val();
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
		event_name: $('#manual_event_name').val(),
		event_start: $('#manual_event_start').val(),
		event_end: $('#manual_event_end').val(),
		event_location: $('#manual_event_location').val(),
		event_description: $('#manual_event_description').val(),
		event_host: $('#manual_event_host').val(),
		event_url: $('#manual_event_url').val()
	};

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
			$('#manual_event_submit_status').html('Something went wrong! Are you sure the event you submitted is public?');
			return false;
		}
	});
};

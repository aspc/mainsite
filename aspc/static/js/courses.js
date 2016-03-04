// ASPC namespace
var ASPC = ASPC || {};

/**
* @module
* @description The course calendar
*/
ASPC.courses = function () {
	/**
	* @private
	*/
	var my = {
		self: this,
		CURRENT_PAGE: ASPC.Settings.pathname,
		ADD_TO: '+ add to schedule',
		REMOVE_FROM: '- remove from schedule',
		calendarElement: $('#calendar'),
		loadingMessageElement: $('#loading_message'),
		errorMessageElement: $('#error_message'),
		initCalendar: function () {
			my.calendarElement.weekCalendar({
				businessHours: {
					start: 8,
					end: 24,
					limitDisplay: true
				},
				timeslotsPerHour: 2,
				daysToShow: 5,
				timeSeparator: '&ndash;',
				readonly: true,
				allowCalEventOverlap: true,
				overlapEventsSeparate: true,
				height: function (calendar) {
					return $('table.wc-time-slots').height() + my.calendarElement.find(".wc-toolbar").outerHeight() + my.calendarElement.find(".wc-header").outerHeight();
				},
				eventHeader: function (calEvent, calendar) {
					return calEvent.title;
				},
				eventBody: function (calEvent, calendar) {
					var options = calendar.weekCalendar('option'),
					one_hour = 3600000,
					displayTitleWithTime = calEvent.end.getTime() - calEvent.start.getTime() <= (2 * (one_hour / options.timeslotsPerHour));
					if (displayTitleWithTime) {
						return '';
					}
					else {
						return calendar.weekCalendar('formatTime', calEvent.start, options.timeFormat) + options.timeSeparator + calendar.weekCalendar('formatTime', calEvent.end, options.timeFormat);
					}
				},
				eventAfterRender: function (calEvent, event) {
					event.addClass('campus_' + calEvent.campus);
				},
				getHeaderDate: function (date, calendar) {
					var options = calendar.weekCalendar('option');
					var dayName = options.useShortDayNames ? options.shortDays[date.getDay()] : options.longDays[date.getDay()];
					return dayName;
				}
			});

			// Fake the date so the calendar displays events visibly
			my.calendarElement.weekCalendar('gotoDate', new Date(2012, 8, 3, 0, 0, 0, 0));
		},
		loadCalendar: function () {
			$.get(my.CURRENT_PAGE + 'load/')
				.done(function (events) {
					$.each(events, function (index, event_data) {
						my.addCourseDataToCalendar(event_data, false);
					});
				});
		},
		loadSavedCalendar: function (events) {
			$.each(events, function (index, event_data) {
				my.addCourseDataToCalendar(event_data, true);
			});
		},
		/**
		 * Only ever invoked by toggleCourse() with a click on a search result
		 */
		addCourse: function (course_slug) {
			my.loadingMessageElement.show();

			$.get(my.CURRENT_PAGE + course_slug + '/add/')
				.done(function (event_data) {
					my.loadingMessageElement.hide();

					my.addCourseDataToCalendar(event_data, false);
				})
				.fail(my.failedRequestCallback);
		},
		/**
		 * Only ever invoked by toggleCourse(), either with a click on a search result or a click on the course label 'x'
		 */
		removeCourse: function (course_slug) {
			my.loadingMessageElement.show();

			$.get(my.CURRENT_PAGE + course_slug + '/remove/')
				.done(function (event_ids) {
					my.loadingMessageElement.hide();

					$.each(event_ids, function (index, event_id) {
						my.calendarElement.weekCalendar('removeEvent', event_id);
					});

					// Remove the indicator label
					$('li#indicator_' + course_slug).remove();
				})
				.fail(my.failedRequestCallback);
		},
		addCourseDataToCalendar: function (course_data, is_frozen) {
			var events = course_data.events,
				info = course_data.info;

			// Add each event meeting time to the calendar
			$.each(events, function (index, calendar_event) {
				my.calendarElement.weekCalendar('updateEvent', {
					start: Date.parse(calendar_event.start),
					end: Date.parse(calendar_event.end),
					title: calendar_event.title,
					id: calendar_event.id,
					campus: info.campus_code,
				});
			});

			var course_label_list = $('ol#schedule_courses'),
				li = $(document.createElement('li'))
					.addClass('campus_' + info.campus_code)
					.attr('id', 'indicator_' + info.course_code_slug),
				a = $(document.createElement('a'))
					.attr('href', info.detail_url)
					.addClass('course_detail')
					.text(info.course_code),
				a2 = $(document.createElement('a'))
					.addClass('course_delete')
					.text('x')
					.on('click', function (event) {
						// If the course to be removed is currently visible as a search result too,
						// we need to call toggleCourse() too to take care of updating that
						if ($("div[data-course_slug='" + info.course_code_slug + "']")) {
							my.self.toggleCourse(info.course_code_slug);
						}
						// Otherwise, only remove the course itself without worrying about updating
						// anything else
						else {
							my.removeCourse(info.course_code_slug);
						}
					});

			if (is_frozen) {
				// Build the course label with the <li> element and the course link <a> element
				a.appendTo(li);
				course_label_list.append(li);
			}
			else {
				// Build the course label with the <li> element, the course link <a> element, and the course delete <a> element
				a.appendTo(li);
				a2.appendTo(li);
				course_label_list.append(li);
			}
		},
		failedRequestCallback: function () {
			my.errorMessageElement.show();
			window.setTimeout(function () {
				my.errorMessageElement.hide();
			}, 5000);
		}
	};

	/**
	 * @public
	 * @description Inits the module
	 */
	my.self.init = function () {
		if (jQuery.browser.msie && jQuery.browser.version <= 7) {
			return;
		}

		// Remove the loading and error message
		my.loadingMessageElement.hide();
        my.errorMessageElement.hide();

		// Init the calendar widget
		my.initCalendar();

		// If we're on a saved calendar page, load the saved calendar data in the DOM into the calendar
		if (my.CURRENT_PAGE.match(/\/courses\/schedule\/\d+(\/)?/) && my.saved_calendar_data) {
			my.loadSavedCalendar(my.saved_calendar_data);
		}
		else {
			// Otherwise, just load a blank calendar like normal
			my.loadCalendar();
		}
	};

	/**
	 * @public
	 * @description Handler for toggling between "add"ing and "remove"ing a course in the search result list
	 */
	my.self.toggleCourse = function (course_slug) {
		var search_result_div = $("div[data-course_slug='" + course_slug + "']");

		// If the toggled course has already been added...
		if (search_result_div.data('is_added')) {
			// Then remove the course
			my.removeCourse(course_slug);

			// Toggle the display text back to ADD_TO
			search_result_div.find('a.add_course').text(my.ADD_TO);

			// Toggle the is_added attribute
			search_result_div.data('is_added', false);
		}
		else {
			// Otherwise add the course
			my.addCourse(course_slug);

			// Toggle the display text to REMOVE_FROM
			search_result_div.find('a.add_course').text(my.REMOVE_FROM);

			// Toggle the is_added attribute
			search_result_div.data('is_added', true);
		}
	};

	/**
	 * @public
	 * @description Clears the calendar of all added courses
	 */
	my.self.clearCalendar = function () {
		my.loadingMessageElement.show();

		$.get(my.CURRENT_PAGE + 'clear/')
			.done(function (data) {
				my.loadingMessageElement.hide();
				my.calendarElement.weekCalendar('clear');
				window.location.replace(my.CURRENT_PAGE);
			})
			.fail(my.failedRequestCallback);
	};

	return my.self;
};

$('document').ready(function () {
	ASPC.Courses = new ASPC.courses();
	ASPC.Courses.init();
});
var year = new Date().getFullYear();
var month = new Date().getMonth();
var day = new Date().getDate();
var CURRENT_PAGE = window.location.pathname;
var add_to = '+ add to schedule'
var remove_from = '- remove from schedule';

//jQuery(document).ready();

function init() {
	$('#calendar').weekCalendar({
		businessHours: {start: 8, end: 24, limitDisplay : true},
		timeslotsPerHour: 2	,
		daysToShow: 5,
		timeSeparator: '&ndash;',
		readonly: true,
		allowCalEventOverlap: true,
		overlapEventsSeparate: true,
		height: function($calendar){
			return $('table.wc-time-slots').height() + $('#calendar').find(".wc-toolbar").outerHeight() + $('#calendar').find(".wc-header").outerHeight();
		},
		/*draggable : function(calEvent, $event) {
	         return false;
      },
      	resizable : function(calEvent, $event) {
         return false;
      },*/
		eventHeader : function(calEvent, calendar) {
           var options = calendar.weekCalendar('option');
           var one_hour = 3600000;
           var displayTitleWithTime = calEvent.end.getTime()-calEvent.start.getTime() <= (2*(one_hour/options.timeslotsPerHour));
           if (displayTitleWithTime){
             return calEvent.title;
           }
           else {
             return calendar.weekCalendar('formatDate', calEvent.start, options.timeFormat) + options.timeSeparator + calendar.weekCalendar('formatDate', calEvent.end, options.timeFormat);
           }
         },
		eventBody : function(calEvent, calendar) { 
			var options = calendar.weekCalendar('option');
			var one_hour = 3600000;
           var displayTitleWithTime = calEvent.end.getTime()-calEvent.start.getTime() <= (2*(one_hour/options.timeslotsPerHour));
		   if (displayTitleWithTime) {
			return '';
		}
		else {
			return calEvent.title;
		}
         },
		eventRender : function(calEvent, $event) {
			if(calEvent.end.getTime() < new Date().getTime()) {
				$event.css("backgroundColor", "#aaa");
				$event.find(".time").css({"backgroundColor": "#999", "border":"1px solid #888"});
			}
		},
		eventNew : function(calEvent, $event) {
			//displayMessage("<strong>Added event</strong><br/>Start: " + calEvent.start + "<br/>End: " + calEvent.end);
			//alert("You've added a new event. You would capture this event, add the logic for creating a new event with your own fields, data and whatever backend persistence you require.");
		},
		eventDrop : function(calEvent, $event) {
			//displayMessage("<strong>Moved Event</strong><br/>Start: " + calEvent.start + "<br/>End: " + calEvent.end);
		},
		eventResize : function(calEvent, $event) {
			//displayMessage("<strong>Resized Event</strong><br/>Start: " + calEvent.start + "<br/>End: " + calEvent.end);
		},
		eventClick : function(calEvent, $event) {
			//displayMessage("<strong>Clicked Event</strong><br/>Start: " + calEvent.start + "<br/>End: " + calEvent.end);
			return false;
		},
		eventMouseover : function(calEvent, $event) {
			//displayMessage("<strong>Mouseover Event</strong><br/>Start: " + calEvent.start + "<br/>End: " + calEvent.end);
		},
		eventAfterRender : function(calEvent, $event) {
			$event.addClass('campus_' + calEvent.campus);
			//console.log(calEvent);
		},
		noEvents : function() {
			//displayMessage("There are no events for this week");
		},
		getHeaderDate: function(date, $calendar){
			var options = $calendar.weekCalendar('option');
			var dayName = options.useShortDayNames ? options.shortDays[date.getDay()] : options.longDays[date.getDay()];
			return dayName;
		},
	});
	
	gotodate = $('#calendar').weekCalendar('gotoDate', new Date(2012, 8, 3, 0, 0, 0, 0));
	//$('#calendar').weekCalendar('updateEvent',{"start": new Date(2011, 0, 19, 12), "end": new Date(2011, 0, 19, 15, 55),"title":"ARBC 0011 JP-01", course_id: 8,} );
	//$('#calendar').weekCalendar('updateEvent',{"start": new Date(2011, 0, 19, 12), "end": new Date(2011, 0, 19, 12, 55),"title":"AISS002BLJS-01"} );

	//function displayMessage(message) {
	//	$("#message").html(message).fadeIn();
	//}
	
	//addCourse('HIST', 'HIST132E-CM-01');

	//$("<div id=\"message\" class=\"ui-corner-all\"></div>").prependTo($("body"));
	//loadCalendar();
}

function addCourseData(course_data, frozen) {
	var events = course_data.events;
	var info = course_data.info;
	for (var evid in events ) {
		var cevent = events[evid];
		var translated_event = {"start": Date.parse(cevent.start), "end": Date.parse(cevent.end), "title": cevent.title, "id": cevent.id, "campus": info.campus_code,};
		$('#calendar').weekCalendar('updateEvent', translated_event);
	}
	
	var $c_c_list = $('ol#schedule_courses');
	if (frozen === true) {
	    $c_c_list.append('<li class="campus_' + info.campus_code + 
    		'" id="indicator_' + info.course_code_slug + '"><a href="' + info.detail_url + '" class="course_detail">' + 
    		info.course_code + '</li>');
	} else {
	    $c_c_list.append('<li class="campus_' + info.campus_code + 
    		'" id="indicator_' + info.course_code_slug + '"><a href="' + info.detail_url + '" class="course_detail">' + 
    		info.course_code + '<a class="course_delete">x</a></li>');
		$('li#indicator_' + info.course_code_slug + ' a.course_delete').click(function (event) {
    		removeCourse(info.course_code_slug);
    	});
    	
    	var $result_entry = $('h3#course_' + info.course_code_slug);
    	if ($result_entry.length != 0) {
    	    $result_entry.data('added', true);
    	    $result_entry.prev().text(remove_from);
    	}
	}
}

function addCourse(course_slug) {
	$.get(CURRENT_PAGE + course_slug + '/add/', addCourseData);
}

function toggleCourse(course_slug) {
    var $c = $('h3#course_' + course_slug);
    var added = $c.data('added');
    if (added == true || added == "True") {
        removeCourseData(course_slug);
        $c.prev().text(add_to);
        $('li#indicator_' + course_slug).remove();
        $c.data('added', false);
    } else {
        $c.prev().text(remove_from);
        addCourse(course_slug);
        $c.data('added', true);
    }
}

function removeCourse(course_slug) {
    var $c = $('h3#course_' + course_slug);
    if ($c.length != 0) {
        toggleCourse(course_slug);
    } else {
        removeCourseData(course_slug);
        $('li#indicator_' + course_slug).remove();
    }
}

function removeCourseData(course_slug) {
	$.get(CURRENT_PAGE + course_slug + '/remove/', function (data) { 
		for (var idid in data) {
			var event_id = data[idid];
			$('#calendar').weekCalendar('removeEvent', event_id);
		}
	});
}

function loadSavedCalendar(all_data) {
	for (var cid in all_data) {
		var course_data = all_data[cid];
		addCourseData(course_data, true);
	}
}

function loadCalendar() {
	$.get(CURRENT_PAGE + 'load/', function (data) {
		for (var cid in data) {
			var course_data = data[cid];
			addCourseData(course_data, false);
		}
		
		$('ol.course_list > li > h3').each(function (idx, elem) {
    	    var course_code_slug = $(elem).data('code');
    	    var already_in_calendar = $(elem).data('added');
    	    if (already_in_calendar){
    	        var new_link = $('<a class="add_course" id="indicator2_' + course_code_slug + '">' + remove_from + '</a>');
    	    } else {
    	        var new_link = $('<a class="add_course" id="indicator2_' + course_code_slug + '">' + add_to + '</a>');
    	    }
            

    	    new_link.bind('click', function (event) {
    	        //if ($(this).data('added') != true) {
    	            toggleCourse(course_code_slug);
        	        //$(this).text('added.');
        	      //  $(this).data('added', true);
    	        //}
    	    });
    	    $(elem).before(new_link);
    	});
    	
    	$('h4#share_clear a#clear_schedule').click(function (e){
    	    clearCalendar();
    	});
	});
}

function clearCalendar() {
    $.get(CURRENT_PAGE + 'clear/', function (data) {
        $('#calendar').weekCalendar('clear');
        window.location.replace(CURRENT_PAGE);
	});
}

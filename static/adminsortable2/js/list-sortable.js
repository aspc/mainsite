"use strict";

// make list view sortable
jQuery(function($) {
	var startindex, startorder, endindex, endorder;
	var csrfvalue = $('form').find('input[name="csrfmiddlewaretoken"]').val();
	var getQueryParams = function() {
		var vars = [], hash, i;
		var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
		for (i = 0; i < hashes.length; i++) {
			hash = hashes[i].split('=');
			vars.push(hash[0]);
			vars[hash[0]] = hash[1];
		}
		return vars;
	};
	var ordering = getQueryParams()['o'];

	if (window.admin_sortable2 === undefined)
		return;  // global variables not initialized by change_list.html
	if (ordering === undefined) {
		ordering = '1';
	}

	$('#result_list').sortable({
		handle: 'div.drag',
		items: 'tr',
		axis: 'y',
		scroll: true,
		cursor: 'ns-resize',
		containment: $('#result_list tbody'),
		tolerance: 'pointer',
		start: function(event, dragged_rows) {
			$(this).find('thead tr th').each(function(index) {
				$(dragged_rows.item.context.childNodes[index]).width($(this).width() - 10);
			});
			startindex = dragged_rows.item.index();
		},
		stop: function(event, dragged_rows) {
			var $result_list = $(this);
			$result_list.find('tbody tr').each(function(index) {
				$(this).removeClass('row1 row2').addClass(index % 2 ? 'row2' : 'row1');
			});
			endindex = dragged_rows.item.index()

			if (startindex == endindex) return;
			else if (endindex == 0) {
				if (ordering.split('.')[0] === '-1')
					endorder = parseInt($(dragged_rows.item.context.nextElementSibling).find('div.drag').attr('order')) + 1;
				else
					endorder = parseInt($(dragged_rows.item.context.nextElementSibling).find('div.drag').attr('order')) - 1;
			} else {
				endorder = $(dragged_rows.item.context.previousElementSibling).find('div.drag').attr('order');
			}
			startorder = $(dragged_rows.item.context).find('div.drag').attr('order');

			$.ajax({
				url: window.admin_sortable2.update_url,
				type: 'POST',
				data: {
					o: ordering,
					startorder: startorder,
					endorder: endorder,
					csrfmiddlewaretoken: csrfvalue
				},
				success: function(moved_items) {
					$.each(moved_items, function(index, item) {
						$result_list.find('tbody tr input.action-select[value=' + item.pk + ']').parents('tr').each(function() {
							$(this).find('div.drag').attr('order', item.order);
						});
					});
				},
				error: function(response) {
					console.error('The server responded: ' + response.responseText);
				}
			});
		}
	});
	$('#result_list, tbody, tr, td, th').disableSelection();
});

// Show and hide the step input field
jQuery(function($) {
	var $step_field = $('#changelist-form-step');
	var $page_field = $('#changelist-form-page');
	if (window.admin_sortable2 === undefined)
		return;  // global variables not initialized by change_list.html

	if (window.admin_sortable2.current_page === window.admin_sortable2.total_pages) {
		$page_field.attr('max', window.admin_sortable2.total_pages - 1);
		$page_field.val(window.admin_sortable2.current_page - 1);
	} else {
		$page_field.attr('max', window.admin_sortable2.total_pages);
		$page_field.val(window.admin_sortable2.current_page + 1)
	}
	if (window.admin_sortable2.current_page === 1) {
		$page_field.attr('min', 2);
	} else {
		$page_field.attr('min', 1);
	}

	$step_field.attr('min', 1);

	$('#changelist-form').find('select[name="action"]').change(function() {
		if (['move_to_back_page', 'move_to_forward_page'].indexOf($(this).val()) != -1) {
			if ($(this).val() === 'move_to_forward_page') {
				$step_field.attr('max', window.admin_sortable2.total_pages - window.admin_sortable2.current_page);
			} else {
				$step_field.attr('max', window.admin_sortable2.current_page - 1);
			}
			$step_field.show();
		} else {
			$step_field.hide();
		}
		if ($(this).val() === 'move_to_exact_page') {
			$page_field.show();
		} else {
			$page_field.hide();
		}
	});
});

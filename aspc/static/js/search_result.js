function add_listener(){
	$('.pagi-btn').click(function(){
		var path = $(this).attr('path');
		$(this).hide();
		$.ajax({
			url : path,
			success : function(data){
				$('.course_list').replaceWith(data);
				window.history.pushState("new page", "Course Planner", path);
				add_listener();
			},
			error: function(error){
				$(this).show()
			}
		})
	})
}

$('document').ready(function () {
	add_listener();
});
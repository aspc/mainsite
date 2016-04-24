function add_listener() {
    $('.pagi-btn').click(function () {
        var path = $(this).attr('path');
        if (pagination_request_not_already_sent.call(this)) {
            $(this).html('<img src="' + ASPC.Settings.static_url + '/images/loading.gif" width="13" />');
            $.ajax({
                       url: path,
                       success: function (data) {
                           $('.course_list').replaceWith(data);
                           window.history.pushState("new page", "Course Planner", path);
                           add_listener();
                       },
                       error: function (error) {
                           $(this).show()
                       }
                   });
        }
        function pagination_request_not_already_sent() {
            return $(this).html().indexOf("img") == -1;
        }
    })
}

$('document').ready(function () {
    add_listener();
});
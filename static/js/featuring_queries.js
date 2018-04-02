$('#lucky').click(function(){
    $(this).fadeOut("slow", function() {
        $('.featuring_query').fadeIn();
    });
});

var odd = true;

$('.featuring_query').click(function(){
    var feeling = $(this).attr('feeling');
    $.ajax('/courses/schedule/query/'+feeling,{
        success: function(data){
            if (odd){
              $("<li class='odd'>"+data+"</li>").hide().prependTo(".course_list").fadeIn(1000);
                odd = false;
            }else{
               $("<li class='even'>"+data+"</li>").hide().prependTo(".course_list").fadeIn(1000);
                odd = true;
            }
        },
        error: function(err){
            console.log(err);
        }
    })
})

tooltip = function () {
	var my = {
		self: this,
		bind_qtip: function () {
			var item_element = $(this);
			var helper_text = item_element.attr('helper_text');

			if (helper_text != '') {
				item_element.qtip({
					content: '<p>'+helper_text+'</p>',
					position: {
						at: 'bottom center'
					},
					show: {
						event: 'mouseover',
						solo: true,
						ready: true
					},
					hide: {
						event: 'mouseout'
					},
					style: {
						classes: 'qtip-bootstrap',
						tip: {
							width: 16,
							height: 8
						}
					}
				});
			}
		}
	};

	/**
	 * @public
	 * @description Binds a mouseover event on all item elements that assigns the qtip
	 */
	my.self.init = function () {
		// .one() makes the qtip assignment happen only once
		$('.featuring_query').one('mouseover', my.bind_qtip);
	};

	return my.self;
};

tt = new tooltip();

$('document').ready(tt.init);


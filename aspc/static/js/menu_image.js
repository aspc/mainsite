$('#menu_table tr td ul li').hover(function(){
        var item = $(this);
        var image_url = item.attr('image_url');
        if (image_url != "None"){
            item.qtip({content: '<img width="100px" height="100px" src="'+image_url+'">',
                position: {
                    at: 'bottom center'
                },
                show: {
                    event: "mouseover",
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
            },event)
        }
    }
    ,function(){
        $('.image_link').remove();
    }
)


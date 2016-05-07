$('#menu_table tr td ul li').hover(function(){
        var item = $(this);
        var name = item.text();
        $(this).append("<a href='javascript:void(0)' class='image_link'></a>");
        $('.image_link').click(function(event){
            $.ajax({
                url : 'image',
                data: {name: name},
                success : function(data){
                    console.log(data);
                    item.qtip({content: '<img width="100px" height="100px" src="'+data+'">',
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
                },
                error: function(error){
                    console.log('error');
                }
            })
        })
    }
    ,function(){
        $('.image_link').remove();
    }
)


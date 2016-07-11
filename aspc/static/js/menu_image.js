// ASPC namespace
var ASPC = ASPC || {};

/**
 * @module
 * @description Methods for the menu
 */
ASPC.menu = function () {
	/**
	 * @private
	 */
	var my = {
		self: this,
		bind_qtip: function () {
			var item_element = $(this);
			var image_url = item_element.attr('image_url');

			if (!!image_url && image_url != 'None') {
				item_element.qtip({
					content: '<img width="100px" height="100px" src="' + image_url + '">',
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
		$('#menu_table tr td ul li').one('mouseover', my.bind_qtip);
	};

	return my.self;
};

ASPC.Menu = new ASPC.menu();

$('document').ready(ASPC.Menu.init);

/* gloabl $, Dashboard */
var dashboard = new Dashboard();

dashboard.addWidget('clock_widget', 'Clock');
dashboard.addWidget('nbr_video_widget', 'Number', {
	getdata: function () {
		var self = this;
		Dashing.utils.get('nbr_video_widget', function (scope) {
			$.extend(self.scope, scope);
		});
	},
	interval 5000
});

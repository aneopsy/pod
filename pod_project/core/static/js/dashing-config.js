/* global Dashboard */

var dashboard = new Dashboard();

dashboard.addWidget('clock_widget', 'Clock');

dashboard.addWidget('videos_widget', 'Number', {
    getData: function () {
        var self = this;
        Dashing.utils.get('videos_widget', function(scope) {
            $.extend(self.scope, scope);
        });
    },
    interval: 5000
});

dashboard.addWidget('server_widget', 'Number', {
    getData: function () {
        var self = this;
        Dashing.utils.get('server_widget', function(scope) {
            $.extend(self.scope, scope);
        });

        $.extend(this.scope, {
            title: 'Server',
            value: 'Off'
            });
    },
    interval: 5000
});

dashboard.addWidget('users_widget', 'List', {
    getData: function () {
        var self = this;
        Dashing.utils.get('users_widget', function(scope) {
            $.extend(self.scope, scope);
        });
    },
    interval: 5000
});

dashboard.addWidget('channels_widget', 'List', {
    getData: function () {
        var self = this;
        Dashing.utils.get('channels_widget', function(scope) {
            $.extend(self.scope, scope);
        });
    },
    interval: 5000
});

dashboard.addWidget('disciplines_widget', 'List', {
    getData: function () {
        var self = this;
        Dashing.utils.get('disciplines_widget', function(scope) {
            $.extend(self.scope, scope);
        });
    },
    interval: 5000
});

/* global Dashboard */

var dashboard = new Dashboard();

dashboard.addWidget('clock_widget', 'Clock');

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

dashboard.addWidget('videos_widget', 'Number', {
    getData: function () {
        var self = this;
        Dashing.utils.get('videos_widget', function(scope) {
            $.extend(self.scope, scope);
        });
    },
    interval: 60000
});

dashboard.addWidget('processor_widget', 'Knob', {
    getData: function () {
        var self = this;
        Dashing.utils.get('processor_widget', function(scope) {
            $.extend(self.scope, scope);
        });
    },
    interval: 1000
});

dashboard.addWidget('memory_widget', 'Knob', {
    getData: function () {
        var self = this;
        Dashing.utils.get('memory_widget', function(scope) {
            $.extend(self.scope, scope);
        });
    },
    interval: 1000
});

dashboard.addWidget('space_widget', 'Knob', {
    getData: function () {
        var self = this;
        Dashing.utils.get('space_widget', function(scope) {
            $.extend(self.scope, scope);
        });
    },
    interval: 60000
});

dashboard.addWidget('users_widget', 'List', {
    getData: function () {
        var self = this;
        Dashing.utils.get('users_widget', function(scope) {
            $.extend(self.scope, scope);
        });
    },
    interval: 60000
});

dashboard.addWidget('channels_widget', 'List', {
    getData: function () {
        var self = this;
        Dashing.utils.get('channels_widget', function(scope) {
            $.extend(self.scope, scope);
        });
    },
    interval: 60000
});

dashboard.addWidget('disciplines_widget', 'List', {
    getData: function () {
        var self = this;
        Dashing.utils.get('disciplines_widget', function(scope) {
            $.extend(self.scope, scope);
        });
    },
    interval: 60000
});

(function (jQuery) {
    var DiscussionTopic = Backbone.Model.extend({
        urlRoot: '/nutrition/api/v1/discussion_topic/'
    });

    var DiscussionTopicList = Backbone.Collection.extend({
        model: DiscussionTopic,
        parse: function(response) {
            return response;
        }
    });

    var CounselingSession = Backbone.Model.extend({
        defaults: {
            topics: null
        },
        urlRoot: '/nutrition/api/v1/counseling_session/',
        parse: function(response) {
            response.topics = new DiscussionTopicList(response.topics);
            return response;
        }
    });

    var CounselingSessionState = Backbone.Model.extend({
        defaults: {
            answered: new DiscussionTopicList(),
            elapsed_time: 0
        },
        urlRoot: '/nutrition/api/v1/counseling_session_state/',
        parse: function(response) {
            if (response) {
                response.answered = new DiscussionTopicList(response.answered);
            }
            return response;
        }
    });

    var CounselingSessionView = Backbone.View.extend({
        initialize: function(options) {
            _.bindAll(this, 'initialRender', 'render', 'onDiscussion');
            this.template = _.template(jQuery("#session-template").html());
            this.state = options.state;

            this.model.bind('change', this.initialRender);
            this.model.fetch();
        },
        initialRender: function() {
            this.el.innerHTML = this.template(this.model.toJSON());

            // bind events now that the template is rendered
            jQuery(".collapse").collapse({ 'toggle': false }).on('show', this.onDiscussion);

            // pickup the user's state
            this.state.bind('change', this.render);
            this.state.fetch();
        },
        render: function () {
            var self = this;
            if (this.countdown !== undefined && this.countdown > 0) {
                var current = parseInt(jQuery("#display_time_text").html(), 10);
                current -= 1; self.countdown -= 1;
                jQuery("#display_time_text").html(current);

                jQuery("#display_time").effect("highlight", { color: '#FF0000' }, 1100, function() {
                    if (self.countdown > 0) {
                        setTimeout(self.render, 0);
                    } else {
                        jQuery(self.button_complete).show();
                        self.button_complete = undefined;
                        self.countdown = undefined;

                        jQuery('div.accordion-group').removeClass('highlight');
                        self.enableTopics();
                    }
                });
            } else {
                var display_time = this.model.get('available_time') - this.state.get('elapsed_time');
                jQuery('#display_time_text').html(display_time);
                self.enableTopics();
            }
        },
        enableTopics: function() {
            var self = this;
            this.model.get('topics').forEach(function (topic) {
                if (self.state.get('answered').get(topic.id)) {
                    jQuery('#' + topic.get('id')).find('.btn.discuss').attr('disabled', 'disabled');
                } else {
                    jQuery('#' + topic.get('id')).find('.btn.discuss').removeAttr('disabled');
                }
            });
        },
        onDiscussion: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery('.btn.discuss').attr('disabled', 'disabled');
            jQuery(srcElement).parents('div.accordion-group').addClass('highlight');

            var data_id = jQuery(srcElement).data("id");
            var topic = this.model.get('topics').get(data_id);

            this.countdown = topic.get('actual_time');
            this.button_complete = jQuery(srcElement).find('button.btn.complete');

            var elapsed = this.state.get('elapsed_time') + topic.get('actual_time');
            this.state.set('elapsed_time', elapsed);
            this.state.get('answered').add(topic);
            this.state.save();
        }
    });

    jQuery(document).ready(function () {
        // pickup state if it exists, otherwise, create a new object
        // to hold the user's session data
        var state = new CounselingSessionState();
        if (SESSION_STATE_ID) {
            state.set('id', SESSION_STATE_ID);
        }

        // Counseling Session View
        var view = new CounselingSessionView({
            model: new CounselingSession({ id: SESSION_ID }),
            state: state,
            el: 'div.counseling_session'
        });
    });
}(jQuery));

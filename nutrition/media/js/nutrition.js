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
            elapsed_time: null,
            current_topic: null
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
            _.bindAll(this, 'renderTopics', 'renderState', 'renderTime', 'renderCountdown', 'onDiscussion', 'onCloseDiscussion');
            this.template = _.template(jQuery("#session-template").html());
            this.state = options.state;

            this.model.bind('change', this.renderTopics);
            this.model.fetch();
        },
        renderTopics: function() {
            this.el.innerHTML = this.template(this.model.toJSON());

            // bind events now that the template is rendered
            jQuery(".collapse").collapse({ 'toggle': false }).on('show', this.onDiscussion).on('hide', this.onCloseDiscussion);

            // pickup the user's state
            this.state.bind('change:elapsed_time', this.renderTime);
            this.state.bind('change:user', this.renderState);
            this.state.bind('change:countdown', this.renderCountdown);
            this.state.fetch();
        },
        renderState: function () {
            var self = this;
            var available_time = this.model.get('available_time') - this.state.get('elapsed_time');
            var enabled = 0;

            jQuery('#patient-chart-text').html(this.model.get('patient_chart'));

            this.model.get('topics').forEach(function (topic) {
                if (self.state.get('answered').get(topic.id)) {
                    jQuery('#' + topic.get('id')).find('.btn.discuss').attr('disabled', 'disabled');
                    jQuery('#' + topic.get('id')).find('div.reason').html("discussed");

                    jQuery('#patient-chart-text').append('<div class="patient-chart-item">' + topic.get('summary_text') + '<br />' + topic.get('summary_reply') + '</div>');

                } else if (topic.get('estimated_time') > available_time) {
                    jQuery('#' + topic.get('id')).find('.btn.discuss').attr('disabled', 'disabled');
                    jQuery('#' + topic.get('id')).find('div.reason').html("not enough time left");
                } else {
                    jQuery('#' + topic.get('id')).find('.btn.discuss').removeAttr('disabled');
                    enabled++;
                }
            });

            // Show the "next" icon if
            // 1. The available time <= 0
            // 2. All topics are discussed
            // 3. Remaining topics estimated_time > available_time
            if (available_time <= 0 || enabled === 0) {
                jQuery("#next").show();
                jQuery("#complete-overlay").show();
            } else {
                jQuery("#next").hide();
                jQuery("#complete-overlay").hide();
            }

        },
        renderCountdown: function () {
            var self = this;
            var countdown = this.state.get('countdown');
            if (countdown !== undefined ) {
                // unbind for the moment, the timer will take care of this
                this.state.unbind('change:countdown', this.renderCountdown);

                // Decrement the counter, Increment elapsed time >> triggers display time update
                countdown -= 1;
                self.state.set('countdown', countdown);
                self.state.set('elapsed_time', self.state.get('elapsed_time') + 1);

                // All discussion buttons are disabled, the class gets a selected icon
                jQuery('.btn.discuss').attr('disabled', 'disabled');

                // Make the background div blink
                jQuery("#display_time").effect("highlight", { color: '#FF0000' }, 1100, function() {
                    if (countdown > 0) {
                        setTimeout(self.renderCountdown, 0);
                    } else {
                        jQuery(self.state.get('current_topic_el')).find('.btn.complete').show();
                        self.state.set('countdown', undefined);
                        self.state.set('current_topic_el', undefined);
                        self.state.bind('change:countdown', self.renderCountdown);
                        self.state.save();
                    }
                });
            }
        },
        renderTime: function() {
            jQuery('#display_time_text').html(this.model.get('available_time') - this.state.get('elapsed_time'));
        },
        onDiscussion: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).parents('div.accordion-group').addClass('selected');

            var data_id = jQuery(srcElement).data("id");
            var topic = this.model.get('topics').get(data_id);
            this.state.get('answered').add(topic);
            this.state.save();
            this.state.set({
                'countdown': topic.get('actual_time'),
                'current_topic_el': srcElement
            });

        },
        onCloseDiscussion: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).parents('div.accordion-group').removeClass('selected');

            this.renderState();
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

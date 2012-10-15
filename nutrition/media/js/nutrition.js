(function (jQuery) {

    var DiscussionTopic = Backbone.Model.extend({
        urlRoot: '/nutrition/api/v1/discussion_topic/'
    });

    var DiscussionTopicList = Backbone.Collection.extend({
        model: DiscussionTopic,
        urlRoot: '/nutrition/api/v1/discussion_topic/',
        getByDataId: function(id) {
            var internalId = this.urlRoot + id + '/';
            return this.get(internalId);
        }
    });

    var CounselingSession = Backbone.Model.extend({
        urlRoot: '/nutrition/api/v1/counseling_session/',
        initialize: function(attrs) {
            if (attrs) {
                this.set('topics', new DiscussionTopicList(attrs.topics));
            }
        }
    });


    var CounselingSessionState = Backbone.Model.extend({
        defaults: {
            answered: new DiscussionTopicList(),
            session: new CounselingSession(),
            elapsed_time: null,
            current_topic: null
        },
        urlRoot: '/nutrition/api/v1/counseling_session_state/',
        parse: function(response) {
            if (response) {
                response.session = new CounselingSession(response.session);
                response.answered = new DiscussionTopicList(response.answered);
            }
            return response;

        }
    });

    var CounselingSessionStateList = Backbone.Collection.extend({
        model: CounselingSessionState,
        urlRoot: '/nutrition/api/v1/counseling_session_state/',
        initialize: function(attrs) {
            if (attrs) {
                this.current_session_state_id = attrs.current_session_state_id;
            }
        },
        getCurrentSession: function() {
            return this.getCurrentState().get('session');
        },
        getCurrentState: function() {
            return this.get(this.urlRoot + this.current_session_state_id + "/");
        }

    });

    CounselingSessionView = Backbone.View.extend({
        initialize: function(options) {
            _.bindAll(this, 'initialRender', 'renderState', 'renderTime', 'renderCountdown', 'onDiscussion', 'onCloseDiscussion');
            this.template = _.template(jQuery("#session-template").html());
            this.chartTemplate = _.template(jQuery("#patient-chart-template").html());

            this.states = new CounselingSessionStateList(options);
            this.states.bind('reset', this.initialRender);
            this.states.fetch();
        },
        initialRender: function() {
            // Only invoked once when the session model is instantiated
            var session = this.states.getCurrentSession();
            this.el.innerHTML = this.template(session.toJSON());

            // bind events now that the template is rendered
            jQuery(".collapse").collapse({ 'toggle': false }).on('show', this.onDiscussion).on('hide', this.onCloseDiscussion);

            var state = this.states.getCurrentState();
            state.bind('change:elapsed_time', this.renderTime);
            state.bind('change:countdown', this.renderCountdown);
            this.renderTime(); // explicit

            this.renderState(); // explicit
        },
        renderState: function () {
            var self = this;

            // patient chart
            jQuery("#patient-chart-text").html('');
            this.states.forEach(function(state) {
                jQuery("#patient-chart-text").append(self.chartTemplate(state.toJSON()));
            });


            var session = this.states.getCurrentSession();
            var state = this.states.getCurrentState();

            var available_time = session.get('available_time') - state.get('elapsed_time');
            var enabled = 0;

            session.get('topics').forEach(function (topic) {
                if (state.get('answered').get(topic.id)) {
                    jQuery('#' + topic.get('id')).find('.btn.discuss').attr('disabled', 'disabled').html("<div class='alert-success topic_discussed'>Discussed. </div>");
                } else if (topic.get('estimated_time') > available_time) {
                    jQuery('#' + topic.get('id')).find('.btn.discuss').attr('disabled', 'disabled').html("<div class='alert-danger topic_no_time'>No time left!</div>");
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
                var anchor = jQuery("a#next");
                if (anchor.length < 1) {
                    // construct an anchor link
                    var label = jQuery("#next").html();
                    var url = jQuery("#next_url").attr("value");
                    jQuery("#next").replaceWith('<a id="next" href="' + url + '">' + label + '</a>');

                    // enable the subnav link too
                    var elts = jQuery('#secondary_navigation ul li div.disabled');
                    for (var i = 0; i < elts.length; i++) {
                        var text = jQuery(elts[i]).html().replace(/(\r\n|\n|\r)/gm,"").trim();
                        if (label.search(text) === 0) {
                            jQuery(elts[i]).replaceWith('<div class="regular"><a href="' + url + '">' + text + '</a></div>');
                        }
                    }
                }

                jQuery("#next").show();

                if (available_time > 0 && enabled === 0) {
                    jQuery("#complete-overlay h1").html("You've completed your session!");
                } else {
                    jQuery("#complete-overlay h1").html("You've run out of time!");
                }
                jQuery("#complete-overlay").show();
            } else {
                jQuery("#next").hide();
                jQuery("#complete-overlay").hide();
            }

        },
        renderCountdown: function () {
            var self = this;
            var state = this.states.getCurrentState();

            var countdown = state.get('countdown');
            if (countdown !== undefined ) {
                // unbind for the moment, the timer will take care of this
                state.unbind('change:countdown', this.renderCountdown);

                // Decrement the counter, Increment elapsed time >> triggers display time update
                countdown -= 1;
                state.set('countdown', countdown);
                state.set('elapsed_time', state.get('elapsed_time') + 1);
                jQuery(state.get('current_topic_el')).find('.btn.complete').effect("highlight", { color: '#ff9900' });

                // All discussion buttons are disabled, the class gets a selected icon
                jQuery('.btn.discuss').attr('disabled', 'disabled');

                // Make the background div blink
                jQuery("#display_time").effect("highlight", { color: '#ff9900' }, 1000, function() {
                    if (countdown > 0) {
                        setTimeout(self.renderCountdown, 0);
                    } else {
                        jQuery(state.get('current_topic_el')).find('.btn.complete').removeAttr('disabled').html("Close");
                        state.set('countdown', undefined);
                        state.set('current_topic_el', undefined);
                        state.bind('change:countdown', self.renderCountdown);
                        state.save();
                    }
                });
            }
        },
        renderTime: function() {
            var session = this.states.getCurrentSession();
            var state = this.states.getCurrentState();
            jQuery('.display_time_text').html(session.get('available_time') - state.get('elapsed_time'));
        },
        onDiscussion: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).parents('div.accordion-group').addClass('selected');

            var session = this.states.getCurrentSession();
            var data_id = jQuery(srcElement).data("id");
            var topic = session.get('topics').getByDataId(data_id);

            var state = this.states.getCurrentState();
            state.get('answered').add(topic);
            state.save();
            state.set({
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


    CounselingReferralView = Backbone.View.extend({
        initialize: function(options) {
            _.bindAll(this, 'renderPatientChart');
            this.chartTemplate = _.template(jQuery("#patient-chart-template").html());

            this.states = new CounselingSessionStateList();
            this.states.bind('reset', this.renderPatientChart);
            this.states.fetch();
        },
        renderPatientChart: function() {
            var self = this;

            // patient chart
            jQuery("#patient-chart-text").html('');
            this.states.forEach(function(state) {
                jQuery("#patient-chart-text").append(self.chartTemplate(state.toJSON()));
            });
        }
    });


}(jQuery));

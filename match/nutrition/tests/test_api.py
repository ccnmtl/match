#pylint: disable-msg=R0904
#pylint: disable-msg=E1103
from django.contrib.auth.models import User
from match.nutrition.models import DiscussionTopic, CounselingSession, \
    CounselingSessionState
from tastypie.test import ResourceTestCase


class CounselingSessionResourceTest(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.

    def setUp(self):
        super(CounselingSessionResourceTest, self).setUp()

        self.topic1 = DiscussionTopic.objects.create(
            id=5,
            text='discussion topic 1',
            estimated_time=5,
            reply='discussion topic 1 reply',
            actual_time=6,
            summary_text='discussion topic 1 summary',
            summary_reply='discussion topic 1 summary reply')

        self.session = CounselingSession(available_time=8)
        self.session.save()
        self.session.topics.add(self.topic1)
        self.session.save()

        self.topic2 = DiscussionTopic.objects.create(
            id=6,
            text='discussion topic 2',
            estimated_time=8,
            reply='discussion topic 2 reply',
            actual_time=2,
            summary_text='discussion topic 2 summary',
            summary_reply='discussion topic 2 summary reply')

        self.session2 = CounselingSession(available_time=2)
        self.session2.save()
        self.session2.topics.add(self.topic2)
        self.session2.save()

        self.user = User.objects.create_user('test_student',
                                             'test@ccnmtl.com',
                                             'test')
        self.user.save()

        self.user2 = User.objects.create_user('test_student_two',
                                              'test@ccnmtl.com',
                                              'test')
        self.user2.save()

    def test_session_get(self):
        self.assertTrue(
            self.api_client.client.login(username='test_student',
                                         password='test'))

        url = '/nutrition/api/v1/counseling_session/%s/' % (self.session.id)
        response = self.api_client.get(url, format='json')

        self.assertValidJSONResponse(response)

        json = self.deserialize(response)

        self.assertEquals(json['available_time'], 8)
        self.assertEquals(len(json['topics']), 1)
        self.assertEquals(json['topics'][0]['text'], 'discussion topic 1')

    def test_session_put(self):
        self.assertTrue(
            self.api_client.client.login(username='test_student',
                                         password='test'))

        url = '/nutrition/api/v1/counseling_session/%s/' % (self.session.id)
        self.assertHttpMethodNotAllowed(self.api_client.put(url,
                                                            format='json',
                                                            data={}))

    def test_state_getlist(self):
        state = CounselingSessionState(user=self.user, session=self.session)
        state.save()

        state2 = CounselingSessionState(user=self.user, session=self.session2)
        state2.save()

        alt = CounselingSessionState(user=self.user2, session=self.session)
        alt.save()

        self.assertTrue(
            self.api_client.client.login(username='test_student',
                                         password='test'))

        url = '/nutrition/api/v1/counseling_session_state/'
        response = self.api_client.get(url, format='json')
        self.assertValidJSONResponse(response)

        json = self.deserialize(response)
        self.assertEquals(len(json['objects']), 2)

        session1 = json['objects'][0]
        self.assertEquals(len(session1['answered']), 0)
        self.assertEquals(session1['elapsed_time'], 0)
        self.assertEquals(session1['session']['available_time'], 8)

        session2 = json['objects'][1]
        self.assertEquals(len(session2['answered']), 0)
        self.assertEquals(session2['elapsed_time'], 0)
        self.assertEquals(session2['session']['available_time'], 2)

        state.answered.add(self.topic1)
        state.save()

        response = self.api_client.get(url, format='json')
        self.assertValidJSONResponse(response)
        json = self.deserialize(response)
        self.assertEquals(len(json['objects']), 2)

        session1 = json['objects'][0]
        self.assertEquals(len(session1['answered']), 1)
        self.assertEquals(session1['answered'][0],
                          '/nutrition/api/v1/discussion_topic/5/')

    def test_state_put(self):
        self.assertTrue(self.api_client.client.login(username='test_student',
                                                     password='test'))

        state = CounselingSessionState(user=self.user, session=self.session)
        state.save()
        state_uri = '/nutrition/api/v1/counseling_session_state/%s/' % state.id

        topic_uri = '/nutrition/api/v1/discussion_topic/%s/' % self.topic1.id

        data = {
            'answered': [topic_uri],
            'elapsed_time': 0,
            'resource_uri': state_uri}

        response = self.api_client.put(state_uri, format='json', data=data)
        self.assertEquals(response.status_code, 204)
        self.assertEquals(state.answered.all().count(), 1)
        self.assertEquals(state.answered.all()[0].id, self.topic1.id)

    def test_state_put_fulltopicresource(self):
        self.assertTrue(self.api_client.client.login(username='test_student',
                                                     password='test'))

        state = CounselingSessionState(user=self.user, session=self.session)
        state.save()
        state_uri = '/nutrition/api/v1/counseling_session_state/%s/' % state.id

        topic_uri = '/nutrition/api/v1/discussion_topic/%s/' % self.topic1.id

        data = {
            'answered': [{
                'id': 5,
                'resource_uri': topic_uri,
                'text': 'discussion topic 1 change',
                'estimated_time': 6,
                'reply': 'discussion topic 1 reply',
                'actual_time': 6,
                'summary_text': '',
                'summary_reply': ''}],
            'elapsed_time': 0,
            'resource_uri': state_uri}

        response = self.api_client.put(state_uri, format='json', data=data)
        self.assertEquals(response.status_code, 401)
        self.assertEquals(state.answered.all().count(), 0)

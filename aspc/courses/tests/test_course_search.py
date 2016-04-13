from django.core.urlresolvers import reverse
from django_webtest import WebTest

class CourseSearchTests(WebTest):

    fixtures = ['fixtures/users.json', 'fixtures/courses.json']

    # Username should appear in top right corner
    def testUserLoggedIn(self):
        index = self.app.get('/', user='sustainability@pomona.edu')
        index.mustcontain('sustainability@pomona.edu')

    # Clicking 'Course Search' navigation tab should bring up page with title Course Search
    def testCourseSearchLink(self):
        index = self.app.get('/', user='sustainability@pomona.edu')
        course_search_index = index.click('Course Planner')
        assert 'Course Planner' in course_search_index

    def testSharingEmptySchedule(self):
        url = reverse("course_planner")
        schedule_page = self.app.get(url, user='sustainability@pomona.edu')
        share_page_with_warning = schedule_page.click('share')
        assert 'There don\'t seem to be any courses in your schedule.' in share_page_with_warning

    def testSearchingForCourses(self):
        url = reverse("course_planner")
        schedule_page = self.app.get(url, user='sustainability@pomona.edu')
        schedule_page.form['department'] = '1' # AISS department
        schedule_page_with_results = schedule_page.form.submit() # Go button
        assert 'AISS002ALKS-01' in schedule_page_with_results
        assert 'AISS002BLKS-01' in schedule_page_with_results

    def testFrozenPage(self):
        url = reverse("view_schedule", kwargs={'schedule_id': 1})
        frozen_schedule = self.app.get(url, user='sustainability@pomona.edu')
        assert 'ART 021' in frozen_schedule

    def testLoadForEditingOnFrozenPage(self):
        url = reverse("view_schedule", kwargs={'schedule_id': 1})
        frozen_schedule = self.app.get(url, user='sustainability@pomona.edu')
        unfrozen_schedule = frozen_schedule.form.submit().follow() # Load for editing button
        assert 'export as .ics' in unfrozen_schedule
        assert 'clear' in unfrozen_schedule
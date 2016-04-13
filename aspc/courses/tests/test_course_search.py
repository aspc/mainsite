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

    def testSearchAndAddReview(self):
        url = reverse("search_reviews")
        review_courses_page = self.app.get(url, user='sustainability@pomona.edu')
        review_courses_page.form['query'] = 'astronomy'
        review_courses_page_with_results = review_courses_page.form.submit()
        add_review_page = review_courses_page_with_results.click('Add a review!', index=1)
        assert 'Add a New Review' in add_review_page

    def testSearchAndAddReview(self):
        url = reverse("write_review",  kwargs={'course_code': 'ASTR051-PO'})
        add_new_review_page = self.app.get(url, user='sustainability@pomona.edu')
        add_new_review_page.form['overall_rating'] = 3
        add_new_review_page.form['work_per_week'] = 20
        add_new_review_page.form['comments'] = "This is a comment!"
        add_new_review_page.form['professor'].select(text="Choi, Philip I.")
        astro_51_detail_page = add_new_review_page.form.submit().follow()
        assert 'Advanced Introductory Astronomy' in astro_51_detail_page
        assert '3.00' in astro_51_detail_page
        assert 'average rating' in astro_51_detail_page
        assert 'This is a comment!' in astro_51_detail_page
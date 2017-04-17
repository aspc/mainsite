from django.conf.urls import patterns, url, include
from aspc.api import views
from aspc.api.views import (MenuList, MenuDiningHallDetail, MenuDayDetail, MenuDiningHallDayDetail, MenuDiningHallDayMealDetail,
    InstructorList, InstructorName, CourseList, DepartmentList, CourseInstructor, CourseDepartment, SectionList)

urlpatterns = [
    url(r'menu/dining_hall/(?P<dining_hall>[^/]+)/day/(?P<day>[^/]+)/meal/(?P<meal>[^/]+)/?$', MenuDiningHallDayMealDetail.as_view()),
    url(r'menu/dining_hall/(?P<dining_hall>[^/]+)/day/(?P<day>[^/]+)/?$', MenuDiningHallDayDetail.as_view()),
    url(r'menu/day/(?P<day>[^/]+)/?$', MenuDayDetail.as_view()),
    url(r'menu/dining_hall/(?P<dining_hall>[^/]+)/?$', MenuDiningHallDetail.as_view()),
    url(r'menu/?$', MenuList.as_view()),

    url(r'departments/?$', DepartmentList.as_view()),

    url(r'instructors/?$', InstructorList.as_view()),
    url(r'instructors/(?P<name>[^/]+)/?$', InstructorName.as_view()),

    url(r'courses/instructor/(?P<instructor_id>\d+)/?$', CourseInstructor.as_view()),
    url(r'courses/department/(?P<department_id>\d+)/?$', CourseDepartment.as_view()),
    url(r'courses/?$', CourseList.as_view()),

    url(r'sections/term/(?P<term_key>[^/]+)?', SectionList.as_view()),

    url(r'^$', views.api_home, name="api_home"),
]
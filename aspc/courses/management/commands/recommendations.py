from django.core.management.base import BaseCommand
from numpy import array, int32, float32, amax, argsort, full, append
from scipy import sparse
from pandas import unique, get_dummies
from pandas import DataFrame
from scipy.sparse import csr_matrix
from aspc.courses.models import CourseReview, Course, Term, Section
from lightfm import LightFM
from lightfm.evaluation import precision_at_k, auc_score
from sklearn import preprocessing
from django.contrib.auth.models import User
from django.db import connection

import pandas as pd
import numpy as np
from scipy.sparse import lil_matrix

#data['user_emails'] = user_emails
#user_emails = array([review.author.email for review in reviews], dtype=object)

def super_requisite_already_taken(course, courses_taken_by_user):
    if course.primary_department.code == "CSCI":
        cs_courses_taken_by_user = filter(lambda course: course.primary_department.code == "CSCI", courses_taken_by_user)
        highest_cs_class_number = max(map(lambda course: course.number, cs_courses_taken_by_user))
        if course.number == 51 and highest_cs_class_number > 51:
            return True
        if (course.number == 52 or course.number == 62) and highest_cs_class_number > 62:
            return True
    elif course.primary_department.code == "MATH":
        math_courses_taken_by_user = filter(lambda course: course.primary_department.code == "MATH", courses_taken_by_user)
        highest_math_class_number = max(map(lambda course: course.number, math_courses_taken_by_user))
        if course.number < 32 and highest_math_class_number > course.number:
            return True
    return False

class Command(BaseCommand):
    args = ''
    help = 'gives course recommendations to users'

    def np_2d_array_to_sparse_matrix(self, array):
        i,j,data=[],[],[]
        for col in range(1, array.shape[1]):
            i.extend(array[:,0])
            j.extend(np.zeros(array.shape[0],int)+(col-1))
            data.extend(array[:,col])
        return sparse.coo_matrix((data,(i,j)),shape=(amax(i)+1, array.shape[1]-1))

    def rating_normalize(self, rating):
        normalized_rating = 3*(rating/5.0 - 0.6)
        return normalized_rating

    def handle(self, *args, **options):
        reviews = CourseReview.objects.all()

        user_ids = array([review.author.id for review in reviews], dtype=int32)
        course_ids = array([review.course.id for review in reviews], dtype=int32)
        #ratings = array([self.rating_normalize(review.overall_rating) for review in reviews], dtype=int32)
        ratings = array([(review.overall_rating - 2) for review in reviews], dtype=int32)

        test_train_ratio = 0.1
        cut_off = len(user_ids)-int(test_train_ratio*len(user_ids))
        data = {}

        data['train'] = sparse.coo_matrix((ratings[:cut_off],(user_ids[:cut_off],course_ids[:cut_off])), shape=(amax(user_ids)+1,amax(course_ids)+1))
        data['test'] = sparse.coo_matrix((ratings[cut_off:],(user_ids[cut_off:],course_ids[cut_off:])), shape=(amax(user_ids)+1,amax(course_ids)+1))

        seen_course = set()
        course_features = []
        for review in reviews:
            useful_rating, engagement_rating, difficulty_rating, competency_rating, lecturing_rating, ethusiasm_rating, approachable_rating = review.course.get_miscellaneous_ratings_for_recommendations()
            course_features.append((review.course.id, review.instructor.id, review.course.primary_department.id, self.rating_normalize(review.course.rating), self.rating_normalize(useful_rating), self.rating_normalize(engagement_rating), self.rating_normalize(difficulty_rating), self.rating_normalize(competency_rating), self.rating_normalize(lecturing_rating), self.rating_normalize(ethusiasm_rating), self.rating_normalize(approachable_rating)))

        course_features_unique = [course for course in course_features if course[0] not in seen_course and not seen_course.add(course[0])]
        course_features_df = DataFrame.from_records(course_features_unique, index="id", columns=["id", "instructor_id", "primary_department_id", "course_rating", "useful_rating", "engagement_rating", "difficulty_rating", "competency_rating", "lecturing_rating", "ethusiasm_rating", "approachable_rating"])
        course_features_df_binarized = get_dummies(course_features_df, columns=['instructor_id', 'primary_department_id'], sparse=True)

        index = array(course_features_df_binarized.index)
        index_as_column_array = index.reshape((-1,1))
        course_features_df_binarized_as_2d_array = array(append(index_as_column_array, course_features_df_binarized.values, axis=1), dtype=float32)

        course_features_unnormalized = self.np_2d_array_to_sparse_matrix(course_features_df_binarized_as_2d_array)
        data['course_features'] = course_features_unnormalized #preprocessing.scale(course_features_unnormalized, with_mean=False)

        course_names = array([review.course.name for review in reviews], dtype=object)
        data['course_names'] = course_names

        model = LightFM(loss='warp')
        model.fit(data['train'], item_features=data['course_features'], epochs=30, num_threads=2, verbose=False)

        # ZQ 1637, Kent 2427, Matt 1724, Patrick 1605
        for user_id in [2427, 1637, 1724, 1605]:
            #user_id = 2427
            recommendation_count = 30
            scores_for_kent = model.predict(user_id, course_ids, item_features=data['course_features'], num_threads=2)
            recommendations_for_kent = data['course_names'][argsort(-scores_for_kent)]
            #for recommendation in unique(recommendations_for_kent)[:recommendation_count]: print("%s, " % recommendation)

            user = User.objects.get(id=user_id)
            print "Top 25 recommendations next semester for " + user.email
            reviews_by_user = CourseReview.objects.filter(author=user)
            courses_taken_by_user = map(lambda review: review.course, reviews_by_user)
            course_id_of_recommendations_for_kent = course_ids[argsort(-scores_for_kent)]

            cursor = connection.cursor()
            cursor.execute("SELECT courses_course.id FROM courses_course WHERE EXISTS (SELECT * FROM courses_section WHERE term_id IN (SELECT id FROM courses_term ORDER BY year DESC, session ASC LIMIT 1) AND courses_course.id = course_id)")
            next_term_courses = map(lambda tuple: tuple[0], cursor.fetchall())

            recommendation_list = []
            for course_id in unique(course_id_of_recommendations_for_kent)[:(5*recommendation_count)]:
                course = Course.objects.get(id=course_id)
                if course not in courses_taken_by_user and course.id in next_term_courses:
                    if not super_requisite_already_taken(course, courses_taken_by_user):
                        recommendation_list.append(course)

            for recommendation in recommendation_list[:recommendation_count]:
                print recommendation

        train_precision = precision_at_k(model, data['train'], item_features=data['course_features'], k=10).mean()
        test_precision = precision_at_k(model, data['test'], item_features=data['course_features'], k=10).mean()

        train_auc = auc_score(model, data['train'], item_features=data['course_features']).mean()
        test_auc = auc_score(model, data['test'], item_features=data['course_features']).mean()

        print('Precision: train %.2f, test %.2f.' % (train_precision, test_precision))
        print('AUC: train %.2f, test %.2f.' % (train_auc, test_auc))
        import ipdb; ipdb.set_trace()
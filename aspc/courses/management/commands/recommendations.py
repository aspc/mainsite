from django.core.management.base import BaseCommand
from numpy import array, int32, float32, amax, argsort, full, append
from scipy import sparse
from pandas import unique, get_dummies
from pandas import DataFrame
from scipy.sparse import csr_matrix
from aspc.courses.models import CourseReview
from lightfm import LightFM
from lightfm.evaluation import precision_at_k, auc_score
from django.contrib.auth.models import User

import pandas as pd
import numpy as np
from scipy.sparse import lil_matrix

#data['user_emails'] = user_emails
#user_emails = array([review.author.email for review in reviews], dtype=object)
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
        if rating == 1:
            return -3
        elif rating == 2:
            return -1
        elif rating == 3:
            return 0
        elif rating == 4:
            return 1
        elif rating == 5:
            return 3
        else:
            print "Invalid rating"

    def handle(self, *args, **options):
        reviews = CourseReview.objects.all()

        user_ids = array([review.author.id for review in reviews], dtype=int32)
        course_ids = array([review.course.id for review in reviews], dtype=int32)
        ratings = array([self.rating_normalize(review.overall_rating) for review in reviews], dtype=int32)

        test_train_ratio = 0.1
        cut_off = len(user_ids)-int(test_train_ratio*len(user_ids))
        data = {}

        data['train'] = sparse.coo_matrix((ratings[:cut_off],(user_ids[:cut_off],course_ids[:cut_off])), shape=(amax(user_ids)+1,amax(course_ids)+1))
        data['test'] = sparse.coo_matrix((ratings[cut_off:],(user_ids[cut_off:],course_ids[cut_off:])), shape=(amax(user_ids)+1,amax(course_ids)+1))

        seen_course = set()
        course_features = [(review.course.id, review.instructor.id, review.course.primary_department.id)
                           for review in reviews]
        course_features_unique = [course for course in course_features if course[0] not in seen_course and not seen_course.add(course[0])]
        course_features_df = DataFrame.from_records(course_features_unique, index="id", columns=["id", "instructor_id", "primary_department_id"])
        course_features_df_binarized = get_dummies(course_features_df, columns=['instructor_id', 'primary_department_id'], sparse=True)

        index = array(course_features_df_binarized.index)
        index_as_column_array = index.reshape((-1,1))
        course_features_df_binarized_as_2d_array = array(append(index_as_column_array, course_features_df_binarized.values, axis=1), dtype=float32)

        data['course_features'] = self.np_2d_array_to_sparse_matrix(course_features_df_binarized_as_2d_array)

        course_names = array([review.course.name for review in reviews], dtype=object)
        data['course_names'] = course_names

        model = LightFM(loss='warp')
        model.fit(data['train'], item_features=data['course_features'], epochs=30, num_threads=2, verbose=False)

        # ZQ 1637, Kent 2427
        scores_for_kent = model.predict(1637, course_ids, item_features=data['course_features'], num_threads=2)
        recommendations_for_kent = data['course_names'][argsort(-scores_for_kent)]
        for recommendation in unique(recommendations_for_kent)[:20]: print("%s, " % recommendation)

        train_precision = precision_at_k(model, data['train'], item_features=data['course_features'], k=10).mean()
        test_precision = precision_at_k(model, data['test'], item_features=data['course_features'], k=10).mean()

        train_auc = auc_score(model, data['train'], item_features=data['course_features']).mean()
        test_auc = auc_score(model, data['test'], item_features=data['course_features']).mean()

        print('Precision: train %.2f, test %.2f.' % (train_precision, test_precision))
        print('AUC: train %.2f, test %.2f.' % (train_auc, test_auc))
        import ipdb; ipdb.set_trace()
###############################################################################
# Copyright (C) 2013 Lumen LLC.
#
# This file is part of the python3-canvaslms-api module Source Code.
#
# python3-canvaslms-api is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python3-canvaslms-api is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with python3-canvaslms-api. If not, see <http://www.gnu.org/licenses/>.
###############################################################################


from canvaslms.api.users import User
from canvaslms.api.submissions import Submission
import canvaslms.api

class Courses:
    'Class providing access to all course-related API endpoints.'
    def __init__(self, connector):
        self._connector = connector

    def getCourses(self, enrollment_type=None, enrollment_role=None, include=None):
        if self._connector == None:
            raise ValueError('Property \'_connector\' must be specified prior to calling this function.')

        # build enrollment_type string
        enrollment_type_str = ''
        if enrollment_type != None:
            enrollment_type = '&enrollment_type={}'.format(enrollment_type)

        # build enrollment_role string
        enrollment_role_str = ''
        if enrollment_role != None:
            enrollment_role = '&enrollment_role={}'.format(enrollment_role)

        # build include string
        include_str = ''
        if include != None:
            for i in include:
                include_str = include_str + '&include[]={}'.format(i)

        # build URL string and call the API
        url_str = 'courses?{}{}{}'.format(enrollment_type_str, enrollment_role_str, include_str)
        resp = self._connector.callAPI(url_str)
        courseList = canvaslms.api.getResponseBody(resp)

        # create Course objects from the results
        courses = []
        for crs in courseList:
            courses.append(Course(crs))

        return courses

    def getUsers(self, course_id, enrollment_type=None, enrollment_role=None, include=None, user_id=None):
        """\
Arguments:
  * course_id
  * enrollment_type: Optional. "teacher"|"student"|"ta"|"observer"|"designer" 
  * enrollment_role
  * include: Must be a list.  Possible values are: ['email', 'enrollments', 'locked', 'avatar_url']
  * user_id"""

        # build enrollment_type string
        enrollment_type_str = ''
        if enrollment_type != None:
            enrollment_type_str = '&enrollment_type={}'.format(enrollment_type)

        # build enrollment_role string
        enrollment_role_str = ''
        if enrollment_role != None:
            enrollment_role_str = '&enrollment_role={}'.format(enrollment_role)

        # build include string
        include_str = ''
        if include != None:
            for i in include:
                include_str = include_str + '&include[]={}'.format(i)

        # build user_id string
        user_id_str = ''
        if user_id != None:
            user_id_str = '&user_id={}'.format(user_id)


        url_str = 'courses/{}/users?{}{}{}{}'.format(course_id, enrollment_type_str, enrollment_role_str, include_str, user_id_str)
#        print(url_str)

        usersJSON = []
        for pg in self._connector.pages(url_str):
            userList = canvaslms.api.getResponseBody(pg)
            usersJSON = usersJSON + userList

        # create Course objects from the results
        users = []
        for usr in usersJSON:
            users.append(canvaslms.api.users.User(usr))

        return users

    def getEnrollments(self, course_id, type=None, roll=None, state=None):
        """\
Arguments:
  * course_id
  * type: Optional list. 'StudentEnrollment'|'TeacherEnrollment'|'TaEnrollment'|'DesignerEnrollment'|'ObserverEnrollment'
  * role: Optional list.
  * state: Optional list. 'active'|'invited'|'creation_pending'|'deleted'|'rejected'|'completed'|'inactive'
"""
        pass

    def getSubmissions(self, course_id, student_ids, assignment_ids=None, grouped=False, include=None):
        # TODO: check student_id to see if it's a single value or a list. Handle it appropriately.
        if self._connector == None:
            raise ValueError('Property \'_connector\' must be specified prior to calling this function.')

        student_ids_str = canvaslms.api.createGetArray('student_ids', student_ids)
        include_str = '&include[]=total_scores'
        param_str = '?per_page=1000{}{}'.format(student_ids_str, include_str)
        submissionsJSON = self._connector.allPages('courses/{}/students/submissions{}'.format(course_id, param_str))

        submissions = []
        for sbms in submissionsJSON:
            submissions.append(Submission(sbms))

        return submissions


class Course:
    'Class representing one course object as returned by the API'

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def sis_course_id(self):
        return self._sis_course_id
    @sis_course_id.setter
    def sis_course_id(self, value):
        self._sis_course_id = value

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def course_code(self):
        return self._course_code
    @course_code.setter
    def course_code(self, value):
        self._course_code = value

    @property
    def account_id(self):
        return self._account_id
    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @property
    def start_at(self):
        return self._start_at
    @start_at.setter
    def start_at(self, value):
        self._start_at = value

    @property
    def end_at(self):
        return self._end_at
    @end_at.setter
    def end_at(self, value):
        self._end_at = value

    @property
    def enrollments(self):
        return self._enrollments
    @enrollments.setter
    def enrollments(self, value):
        self._enrollments = value

    @property
    def calendar(self):
        return self._calendar
    @calendar.setter
    def calendar(self, value):
        self._calendar = value

    @property
    def syllabus_body(self):
        return self._syllabus_body
    @syllabus_body.setter
    def syllabus_body(self, value):
        self._syllabus_body = value

    @property
    def needs_grading_count(self):
        return self._needs_grading_count
    @needs_grading_count.setter
    def needs_grading_count(self, value):
        self._needs_grading_count = value

    @property
    def hide_final_grades(self):
        return self._hide_final_grades
    @hide_final_grades.setter
    def hide_final_grades(self, value):
        self._hide_final_grades = value

    def __init__(self, objectData):
        self.id = objectData.get('id')
        self.sis_course_id = objectData.get('sis_course_id')
        self.name = objectData.get('name')
        self.course_code = objectData.get('course_code')
        self.account_id = objectData.get('account_id')
        self.start_at = objectData.get('start_at')
        self.end_at = objectData.get('end_at')
        self.enrollments = objectData.get('enrollments')
        self.calendar = objectData.get('calendar')
        self.syllabus_body = objectData.get('syllabus_body')
        self.needs_grading_count = objectData.get('needs_grading_count')
        self.hide_final_grades = objectData.get('hide_final_grades')

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


import canvaslms.api
import canvaslms.api.util

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
#        courses = []
#        for crs in courseList:
#            courses.append(Course(crs))

        return courseList

    def getUsers(self, course_id, enrollment_type=None, enrollment_role=None, include=None, user_id=None):
        """\
Get all user objects for this course.

Arguments:
  * course_id
  * enrollment_type: Optional. "teacher"|"student"|"ta"|"observer"|"designer" 
  * enrollment_role
  * include: Must be a list.  Possible values are: ['email', 'enrollments', 'locked', 'avatar_url']
  * user_id
"""

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

        objs = self._connector.allPages(url_str)

        # create Course objects from the results
#        users = []
#        for usr in objs:
#            users.append(canvaslms.api.users.User(usr))

        return objs

    def getEnrollments(self, course_id, type=None, role=None, state=None):
        """\
Get all enrollment objects for this course.

Arguments:
  * course_id
  * type: Optional list. 'StudentEnrollment'|'TeacherEnrollment'|'TaEnrollment'|'DesignerEnrollment'|'ObserverEnrollment'
  * role: Optional list.
  * state: Optional list. 'active'|'invited'|'creation_pending'|'deleted'|'rejected'|'completed'|'inactive'.  Returns 'active' and 'invited' if no state parameter is given.
"""
        # TODO: handle 'type' argument
        # TODO: handle 'role' argument
        # TODO: handle 'state' argument

        if self._connector == None:
            raise ValueError('Property \'_connector\' must be specified prior to calling this function.')

        param_str = '?per_page=1000'
        objs = self._connector.allPages('courses/{}/enrollments{}'.format(course_id, param_str))

#        enrollments = []
#        for enrl in objs:
#            enrollments.append(Enrollment(enrl))
        return objs


    def getSubmissions(self, course_id, student_ids, assignment_ids=None, grouped=False, include=None):
        'Get all assignment submissions for this course'

        # TODO: check student_id to see if it's a single value or a list. Handle it appropriately.
        # TODO: handle the 'grouped' and 'include' parameters
        if self._connector == None:
            raise ValueError('Property \'_connector\' must be specified prior to calling this function.')

        student_ids_str = None
        if student_ids:
            student_ids_str = canvaslms.api.util.createGetArray('student_ids', student_ids)

        assignment_ids_str = None
        if assignment_ids:
            assignment_ids_str = canvaslms.api.util.createGetArray('assignment_ids', assignment_ids)
        
        include_str = '&include[]=total_scores'
        param_str = '?per_page=1000{}{}{}'.format(student_ids_str, assignment_ids_str, include_str)
        objs = self._connector.allPages('courses/{}/students/submissions{}'.format(course_id, param_str))

#        submissions = []
#        for sbms in objs:
#            submissions.append(Submission(sbms))

        return objs

    def getAssignments(self, course_id):
        'Get all assignment objects belonging to this course.'

        if self._connector == None:
            raise ValueError('Property \'_connector\' must be specified prior to calling this function.')

        url_str = 'courses/{}/assignments'.format(course_id)

        objs = self._connector.allPages(url_str)

        # create Course objects from the results
#        assignments = []
#        for asn in objs:
#            assignments.append(canvaslms.api.assignments.Assignment(asn))

        return objs

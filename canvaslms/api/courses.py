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

class Courses:
    'Class providing access to all course-related API endpoints.'
    def __init__(self, connector):
        self._connector = connector

    def getCourses(self, enrollment_type=None, enrollment_role=None, include=None):
        if self._connector == None:
            raise ValueError('Property \'_connector\' must be specified prior to calling this function.')

        resp = self._connector.callAPI('courses')
        respBody = canvaslms.api.getResponseBody(resp)

        return respBody

class Course:
    'Class representing one course object as returned by the API'

    @property
    def id(self):
        return self.id

    @property
    def sis_course_id(self):
        return self.sis_course_id

    @property
    def name(self):
        return self.name

    @property
    def course_code(self):
        return self.course_code

    @property
    def account_id(self):
        return self.account_id

    @property
    def start_at(self):
        return self.start_at

    @property
    def end_at(self):
        return self.end_at

    @property
    def enrollments(self):
        return self.enrollments

    @property
    def calendar(self):
        return self.calendar

    @property
    def syllabus_body(self):
        return self.syllabus_body

    @property
    def needs_grading_count(self):
        return self.needs_grading_count


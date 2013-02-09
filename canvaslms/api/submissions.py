###############################################################################
# python3-canvaslms-api Source Code
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

class Submission:
    @property
    def assignment_id(self):
        return self._assignment_id

    @assignment_id.setter
    def assignment_id(self, value):
        self._assignment_id = value

    @property
    def assignment(self):
        return self._assignment

    @assignment.setter
    def assignment(self, value):
        self._assignment = value

    @property
    def course(self):
        return self._course

    @course.setter
    def course(self, value):
        self._course = value

    @property
    def attempt(self):
        return self._attempt

    @attempt.setter
    def attempt(self, value):
        self._attempt = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        self._grade = value

    @property
    def grade_matches_current_submission(self):
        return self._grade_matches_current_submission

    @grade_matches_current_submission.setter
    def grade_matches_current_submission(self, value):
        self._grade_matches_current_submission = value

    @property
    def html_url(self):
        return self._html_url

    @html_url.setter
    def html_url(self, value):
        self._html_url = value

    @property
    def preview_url(self):
        return self._preview_url

    @preview_url.setter
    def preview_url(self, value):
        self._preview_url = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def submission_comments(self):
        return self._submission_comments

    @submission_comments.setter
    def submission_comments(self, value):
        self._submission_comments = value

    @property
    def submission_type(self):
        return self._submission_type

    @submission_type.setter
    def submission_type(self, value):
        self._submission_type = value

    @property
    def submitted_at(self):
        return self._submitted_at

    @submitted_at.setter
    def submitted_at(self, value):
        self._submitted_at = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def grader_id(self):
        return self._grader_id

    @grader_id.setter
    def grader_id(self, value):
        self._grader_id = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def late(self):
        return self._late

    @late.setter
    def late(self, value):
        self._late = value

    def __init__(self, objectData):
        self.assignment_id = objectData.get('assignment_id')
        self.assignment = objectData.get('assignment')
        self.course = objectData.get('course')
        self.attempt = objectData.get('attempt')
        self.body = objectData.get('body')
        self.grade = objectData.get('grade')
        self.grade_matches_current_submission = objectData.get('grade_matches_current_submission')
        self.html_url = objectData.get('html_url')
        self.preview_url = objectData.get('preview_url')
        self.score = objectData.get('score')
        self.submission_comments = objectData.get('submission_comments')
        self.submission_type = objectData.get('submission_type')
        self.submitted_at = objectData.get('submitted_at')
        self.url = objectData.get('url')
        self.user_id = objectData.get('user_id')
        self.grader_id = objectData.get('grader_id')
        self.user = objectData.get('user')
        self.late = objectData.get('late')

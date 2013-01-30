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

class Enrollment:
    @property
    def id(self):
        return self.id

    @property
    def course_id(self):
        return self.course_id

    @property
    def course_section_id(self):
        return self.course_section_id

    @property
    def enrollment_state(self):
        return self.enrollment_state

    @property
    def limit_privileges_to_course_section(self):
        return self.limit_privileges_to_course_section

    @property
    def root_account_id(self):
        return self.root_account_id

    @property
    def type(self):
        return self.type

    @property
    def role(self):
        return self.role

    @property
    def user_id(self):
        return self.user_id

    @property
    def html_url(self):
        return self.html_url

    @property
    def grades(self):
        return self.grades

    @property
    def user(self):
        return self.user


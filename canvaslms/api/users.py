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

class User:
    @property
    def id(self):
        return self.id

    @property
    def name(self):
        return self.name

    @property
    def sortable_name(self):
        return self.sortable_name

    @property
    def short_name(self):
        return self.short_name

    @property
    def sis_user_id(self):
        return self.sis_user_id


    # DEPRECATED
    @property
    def sis_login_id(self):
        return self.sis_login_id

    @property
    def login_id(self):
        return self.login_id

    @property
    def avatar_url(self):
        return self.avatar_url

    @property
    def enrollments(self):
        return self.enrollments

    @property
    def email(self):
        return self.email

    @property
    def locale(self):
        return self.locale

    @property
    def last_login(self):
        return self.last_login


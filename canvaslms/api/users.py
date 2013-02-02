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
        return self._id
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def sortable_name(self):
        return self._sortable_name
    @sortable_name.setter
    def sortable_name(self, value):
        self._sortable_name = value

    @property
    def short_name(self):
        return self._short_name
    @short_name.setter
    def short_name(self, value):
        self._short_name = value

    @property
    def sis_user_id(self):
        return self._sis_user_id
    @sis_user_id.setter
    def sis_user_id(self, value):
        self._sis_user_id = value

    # DEPRECATED
    @property
    def sis_login_id(self):
        return self._sis_login_id
    @sis_login_id.setter
    def sis_login_id(self, value):
        self._sis_login_id = value

    @property
    def login_id(self):
        return self._login_id
    @login_id.setter
    def login_id(self, value):
        self._login_id = value

    @property
    def avatar_url(self):
        return self._avatar_url
    @avatar_url.setter
    def avatar_url(self, value):
        self._avatar_url = value

    @property
    def enrollments(self):
        return self._enrollments
    @enrollments.setter
    def enrollments(self, value):
        self._enrollments = value

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, value):
        self._email = value

    @property
    def locale(self):
        return self._locale
    @locale.setter
    def locale(self, value):
        self._locale = value

    @property
    def last_login(self):
        return self._last_login
    @last_login.setter
    def last_login(self, value):
        self._last_login = value

    def __init__(self, objectData):
        self.id = objectData.get('id')
        self.name = objectData.get('name')
        self.sortable_name = objectData.get('sortable_name')
        self.short_name = objectData.get('short_name')
        self.sis_user_id = objectData.get('sis_user_id')
        self.sis_login_id = objectData.get('sis_login_id')
        self.login_id = objectData.get('login_id')
        self.avatar_url = objectData.get('avatar_url')
        self.enrollments = objectData.get('enrollments')
        self.email = objectData.get('email')
        self.locale = objectData.get('locale')
        self.last_login = objectData.get('last_login')

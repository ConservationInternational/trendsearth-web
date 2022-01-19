import requests
import json
from urllib.parse import quote_plus
from datetime import datetime
from dateutil import tz
from django.conf import settings

API_URL = settings.API_URL
TIMEOUT = settings.TIMEOUT


class RequestTask(object):
    def __init__(self, description, url, method, payload, headers):
        self.description = description
        self.url = url
        self.method = method
        self.payload = payload
        self.headers = headers
        self.exception = None
        self.resp = None

    def run(self):
        if self.method == 'get':
            self.resp = requests.get(self.url, json=self.payload,
                                     headers=self.headers,
                                     timeout=TIMEOUT)
        elif self.method == 'post':
            self.resp = requests.post(self.url, json=self.payload,
                                      headers=self.headers,
                                      timeout=TIMEOUT)
        elif self.method == 'put':
            self.resp = requests.put(self.url, json=self.payload,
                                     headers=self.headers,
                                     timeout=TIMEOUT)
        elif self.method == 'delete':
            self.resp = requests.delete(self.url, json=self.payload,
                                        headers=self.headers,
                                        timeout=TIMEOUT)
        elif self.method == 'patch':
            self.resp = requests.patch(self.url, json=self.payload,
                                       headers=self.headers,
                                       timeout=TIMEOUT)
        elif self.method == 'head':
            self.resp = requests.head(self.url, json=self.payload,
                                      headers=self.headers,
                                      timeout=TIMEOUT)
        else:
            self.exception = ValueError(
                "Unrecognized method: {}".format(self.method))
            return False

        return True

    def finished(self, result):
        if result:
            print('Task completed')
        else:
            if self.exception is None:
                print(f'API {self.method} not successful - probably cancelled')

            elif self.exception is requests.exceptions.ConnectionError:
                print('''API unable to access server -
                 check internet connection''')

            elif self.exception is requests.exceptions.Timeout:
                print('''API unable to login - general error''')

            else:
                print(
                    f'''API {self.method} not successful -
                     exception: {self.exception}''')
                raise self.exception

        if self.resp is not None:
            print(
                f'''API response from "{self.method}" request:
                 {self.resp.status_code}''')
        else:
            print(f'''API response from "{self.method}"
             request was None''')


class Api(object):
    def __init__(self, **kwargs):
        self.url = kwargs.pop('url', None)
        self.token = kwargs.pop('token', None)

        if self.token is None:
            self.email = kwargs.pop('email', None)
            self.password = kwargs.pop('password', None)
            self.login()

    def clean_api_response(self, resp):
        if resp is None:
            # Return 'None' unmodified
            response = resp
        else:
            try:
                # JSON conversion will fail if the server didn't return a json
                # response
                response = resp.json().copy()

                if 'password' in response:
                    response['password'] = '**REMOVED**'

                if 'access_token' in response:
                    response['access_token'] = '**REMOVED**'
                response = json.dumps(response, indent=4, sort_keys=True)
            except ValueError:
                response = resp.text

        return response

    def get_error_status(self, resp):
        try:
            # JSON conversion will fail if the server didn't return a json
            # response
            resp = resp.json()
        except ValueError:
            return ('Unknown error', None)
        status = resp.get('status', None)

        if not status:
            status = resp.get('status_code', 'None')
        desc = resp.get('detail', None)

        if not desc:
            desc = resp.get('description', 'Generic error')

        return (desc, status)

    def login(self):
        if (self.email is None or self.password is None) and self.token is None:
            return None

        resp = self.call_api(
            '/auth',
            method='post',
            payload={
                "email": self.email,
                "password": self.password
            },
        )

        if resp:
            try:
                self.token = resp.get('access_token', None)
            except KeyError:
                pass

    def call_api(self, endpoint, method='get', payload=None, use_token=False):
        if use_token:
            if self.token is None:
                self.login()
            if self.token:
                headers = {'Authorization': f'Bearer {self.token}'}
            else:
                return
        else:
            headers = {}

        # Only continue if don't need token or if token load was successful
        if (not use_token) or (self.token is not None):
            if payload:
                clean_payload = payload.copy()
                if 'password' in clean_payload:
                    clean_payload['password'] = '**REMOVED**'
            else:
                clean_payload = payload

            resp = self._make_request(
                'Trends.Earth API call',
                url=API_URL + endpoint,
                method=method,
                payload=payload,
                headers=headers
            )
            if resp.status_code == 200:
                return resp.json()
            else:
                desc, status = self.get_error_status(resp)
                # print("Error", u"Error: {} (status {}).".format(desc, status))

    def _make_request(self, description, **kwargs):
        api_task = RequestTask(description, **kwargs)
        api_task.run()
        return api_task.resp

    def get_header(self, url):
        resp = self._make_request(
            'Get head',
            url=url,
            method='head',
            payload=None,
            headers=None
        )

        if resp is not None:
            if resp.status_code == 200:
                return resp.headers
            else:
                desc, status = self.get_error_status(resp)
                # print("Error", u"Error: {} (status {}).".format(desc, status))

    def get_user(self, email='me'):
        resp = self.call_api(
            u'/api/v1/user/{}'.format(quote_plus(email)), use_token=True)
        if resp:
            return resp['data']

    def recover_pwd(self, email):
        return self.call_api(
            u'/api/v1/user/{}/recover-password'.format(quote_plus(email)),
            'post')

    def delete_user(self, email='me'):
        resp = self.call_api('/api/v1/user/me', 'delete', use_token=True)

        if resp:
            return True

    def register(self, email, password, name, organization,
                 country, role="USER"):
        payload = {"email": email,
                   "password": password,
                   "name": name,
                   "institution": organization,
                   "country": country,
                   "role": role}

        return self.call_api('/api/v1/user', method='post', payload=payload)

    def update_user(self, email, name, organization, country):
        payload = {"email": email,
                   "name": name,
                   "institution": organization,
                   "country": country}

        return self.call_api('/api/v1/user/me', 'patch',
                             payload, use_token=True)

    def update_password(self, password, repeatPassword):
        payload = {"password": password,
                   "repeatPassword": repeatPassword}

        return self.call_api(
            u'/api/v1/user/me', 'patch',
            payload,
            use_token=True)

    def get_user_execution(self, id=None, date=None):
        """

        :param id: User ID
        :param date:
        :return:
        """
        # query = ['include=script']

        query = []

        if id:
            query.append(u'user_id={}'.format(quote_plus(id)))

        if date is not None:
            query.append(u'updated_at={}'.format(date))
        query = "?" + "&".join(query)

        resp = self.call_api(
            u'/api/v1/execution{}'.format(query), method='get', use_token=True)

        if not resp:
            return None
        else:
            # do import here to avoid circular import
            data = resp['data']
            # Sort responses in descending order using start time by default
            data = sorted(data, key=lambda job_dict: round(
                datetime.strptime(job_dict['start_date'], '%Y-%m-%dT%H:%M:%S.%f').timestamp()), reverse=True)
            # Convert start/end dates into datatime objects in local time zone

            for job_dict in data:
                start_date = datetime.strptime(
                    job_dict['start_date'], '%Y-%m-%dT%H:%M:%S.%f')
                start_date = start_date.replace(tzinfo=tz.tzutc())
                start_date = start_date.astimezone(tz.tzlocal())
                job_dict['start_date'] = start_date
                end_date = datetime.strptime(
                    job_dict['end_date'], '%Y-%m-%dT%H:%M:%S.%f')
                end_date = end_date.replace(tzinfo=tz.tzutc())
                end_date = end_date.astimezone(tz.tzlocal())
                job_dict['end_date'] = end_date

            return data

    def get_execution_log(self, id):
        """
            :param id: execution ID
            :return:
        """
        resp = self.call_api(
            u'/api/v1/execution/{}/log?start=2021-01-17'.format(quote_plus(id)), 'get', use_token=True)

        if resp:
            return resp['data']
        else:
            return None

    def get_execution(self, execution):
        """
                    Get all executions
                    :param id: Script ID
                    :return:
                """
        resp = self.call_api(u'/api/v1/execution/' +
                             execution, 'get', use_token=True)

        if resp:
            return resp['data']
        else:
            return None

    def get_executions(self):
        """
            Get all executions
            :param id: Script ID
            :return:
        """
        resp = self.call_api(u'/api/v1/execution', 'get', use_token=True)

        if resp:
            return resp['data']
        else:
            return None

    def get_script(self, id=None):
        """

        :param id: Script ID
        :return:
        """
        if id:
            resp = self.call_api(
                u'/api/v1/script/{}'.format(quote_plus(id)), 'get',
                use_token=True)
        else:
            resp = self.call_api(u'/api/v1/script', 'get', use_token=True)

        if resp:
            return resp['data']
        else:
            return None

    def send_mail(self, toemail, msg):
        payload = {"recipients": toemail,
                   "html": msg, }

        return self.call_api('/api/v1/email', 'post', payload, use_token=True)

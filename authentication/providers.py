import abc
import re


class Provider:
    def __init__(self, sms_api):
        self.sms_api = sms_api

    @classmethod
    @abc.abstractmethod
    def is_belong_to_provider(cls, phone_number):
        pass

    @classmethod
    @abc.abstractmethod
    def send_sms(cls, phone_number, code):
        pass


class Irancell(Provider):
    def __init__(self, *args, **kwargs):
        super(Irancell, self).__init__(*args, **kwargs)

    @classmethod
    def is_belong_to_provider(cls, phone_number):
        return re.match('09(3[1-9])-?[0-9]{3}-?[0-9]{4}', phone_number)

    @classmethod
    def send_sms(cls, phone_number, code):
        return True


class HamrahAval(Provider):
    def __init__(self, *args, **kwargs):
        super(HamrahAval, self).__init__(*args, **kwargs)

    @classmethod
    def is_belong_to_provider(cls, phone_number):
        return re.match('09(1[0-9])-?[0-9]{3}-?[0-9]{4}', phone_number)

    @classmethod
    def send_sms(cls, phone_number, code):
        return True


class Rightel(Provider):
    def __init__(self, *args, **kwargs):
        super(Rightel, self).__init__(*args, **kwargs)

    @classmethod
    def is_belong_to_provider(cls, phone_number):
        return re.match('09(2[0-9])-?[0-9]{3}-?[0-9]{4}', phone_number)

    @classmethod
    def send_sms(cls, phone_number, code):
        return True

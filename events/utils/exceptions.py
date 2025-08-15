""" Исключения """
class NoAvailableSeats(Exception):

    pass

class UserBlocked(Exception):
    default_detail = "Ваш аккаунт заблокирован, обратитесь к Администрации"

class PastDateError(Exception):
    default_detail = "Нельзя зарегистрироваться на прошедшее мероприятие"

class AlreadyRegistered(Exception):

    pass
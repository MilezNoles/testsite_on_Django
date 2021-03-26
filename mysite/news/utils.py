class MyMixin(object):
    mixin_prop = ""

    def get_prop(self):
        return self.mixin_prop.upper()

    def get_upper(self, s):
        if isinstance(s, str):
            return s.upper()
        else:
            return s.title.upper()

# функции для отправки на почту
def get_mail_subject(nick):
    return f"{nick}, Добро пожаловать на сайт новостей"


def get_mail_context(nick, email, password):
    return f"Здравствуйте, {nick}!\n" \
           f"Поздравляем! Вы прошли успешную регистрацию в нашем проекте !\n" \
           f"Ваши регистрационные данные в проекте:\n" \
           f"Логин: {nick}\n" \
           f"Почта: {email}\n" \
           f"Пароль: {password}\n"

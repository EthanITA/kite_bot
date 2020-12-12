import kite_api
from RandomWordGenerator import RandomWord


def gen_random_word(length, const_word_size=False, include_digits=True):
    rw = RandomWord(max_word_size=length, constant_word_size=const_word_size, include_digits=include_digits)
    return rw.generate()


class KiteBot:
    def __init__(self, email=None, password=None, max_len_email=15, len_password=8):
        self.len_email = max_len_email
        self.len_password = len_password
        self.email = email
        self.password = password
        self.session_cookie = str()
        self.account = dict()

    def gen_email(self):
        def gen(l):
            return gen_random_word(l, include_digits=False)

        self.email = f"{gen(self.len_email // 3)}@{gen(self.len_email // 3)}.{gen(self.len_email - (self.len_email // 3) * 2)}"
        return self.email

    def gen_password(self):
        self.password = gen_random_word(self.len_password, const_word_size=True)
        return self.password

    def create_account(self):
        email = self.gen_email() if self.email is None else self.email
        password = self.gen_password() if self.password is None else self.password
        result = kite_api.create_account(email, password)
        self.session_cookie = result.get("cookie", "")
        self.account = result
        print(f"\tEmail: {email}\n\tPassword: {password}")
        return result

    def get_cookie_session(self):
        session_key = "kite-session"
        session = self.session_cookie.split(";")[0].split(f"{session_key}=")[1]
        return session

    def start_trial(self):
        return kite_api.start_trial(self.session_cookie)

    def get_licenses(self):
        return kite_api.get_licenses(self.session_cookie)

    def update_kite_session(self, home_dir=""):
        import json
        import sys
        if sys.platform.startswith("linux"):
            if home_dir == "":
                import getpass
                import os

                home_dir = f"{dict(os.environ).get('HOME', f'/home/{getpass.getuser()}')}/.kite"

            session_filename = "session.json"
            with open(f"{home_dir}/{session_filename}") as f:
                session_json = json.load(f)

            session_json[0]["Value"] = self.get_cookie_session()

            with open(f"{home_dir}/{session_filename}", "w") as f:
                json.dump(session_json, f)

        else:
            raise OSError("Only Linux is supported")

    def get_credentials(self):
        return self.email, self.password

    def automate(self):
        print("Creating account...")
        self.create_account()
        print("Starting pro trial...")
        self.start_trial()
        self.update_kite_session()
        print("You have to completely restart Kite now!")


if __name__ == '__main__':
    bot = KiteBot()
    bot.automate()

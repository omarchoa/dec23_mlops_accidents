import os
import pickle


class BddLogin:
    def __init__(self, user_data=None):
        self.user_data = user_data
        bdd_login_filename = "login_bdd"  # full path to the bdd filemane
        if os.path.isfile(bdd_login_filename):
            with open(bdd_login_filename, "rb") as bdd:
                self.user_data = pickle.load(bdd)
        else:
            self.user_data = {
                "alexandre_winger": "user",
                "fabrice_charraud": "user",
                "michaël_deroche": "user",
                "omar_choa": "user",
                "alban_thuet": "admin",
            }
            with open(bdd_login_filename, "wb") as bdd:
                pickle.dump(self.user_data, bdd)

    def is_(self, rights, login, password):
        key = f"{login}_{password}"
        if key in self.user_data.keys() and self.user_data[key] == rights:
            return True
        return False


if __name__ == "__main__":
    bdd = BddLogin()
    print(bdd.is_("user", "tom", ""))  # should be False
    print(bdd.is_("user", "fabrice", ""))  # should be False
    print(bdd.is_("user", "alexandre", "winger"))  # should be True
    print(bdd.is_("admin", "alban", "thuet"))  # should be True

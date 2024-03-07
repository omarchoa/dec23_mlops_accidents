import os
import pickle


class BddLogin:
    def __init__(self, user_data=None):  # override special method .__init__()
        self.user_data = user_data  # initialize .user_data
        bdd_login_filename = "login_bdd"  # full path to the bdd filemane
        if os.path.isfile(
            bdd_login_filename
        ):  # if bdd_login_filename points to a regular / existing file
            with open(
                bdd_login_filename, "rb"
            ) as bdd:  # open it for reading in binary mode as bdd
                self.user_data = pickle.load(
                    bdd
                )  # use pickle to load bdd binary file byte stream, convert it to a Python object, and store it in .user_data
        else:  # else, use the following default values for .user_data
            self.user_data = {
                "alexandre_winger": "user",
                "fabrice_charraud": "user",
                "michaël_deroche": "user",
                "omar_choa": "user",
                "alban_thuet": "admin",
            }
            with open(
                bdd_login_filename, "wb"
            ) as bdd:  # create bdd_login_filename as a new file and open it for writing in binary mode as bdd
                pickle.dump(
                    self.user_data, bdd
                )  # use pickle to convert .user_data from a Python object to a binary file byte stream, store it in bdd, and write bdd to bdd_login_filename

    def is_(
        self, rights, login, password
    ):  # define custom method .is_() with attributes .rights, .login, .password
        key = f"{login}_{password}"  # construct authentication chain
        if (
            key in self.user_data and self.user_data[key] == rights
        ):  # if authentication chain is in .user_data dictionary keys, and if requested rights match corresponding .user_data dictionary value
            return True
        return False


if __name__ == "__main__":
    bdd = BddLogin()
    print(bdd.is_(rights="user", login="tom", password=""))  # should be False
    print(bdd.is_(rights="user", login="fabrice", password=""))  # should be False
    print(
        bdd.is_(rights="user", login="alexandre", password="winger")
    )  # should be True
    print(bdd.is_(rights="admin", login="alban", password="thuet"))  # should be True

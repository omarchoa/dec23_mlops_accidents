import os
import pickle


class BddLogin:
    # override special method .__init__()
    def __init__(self):
        """
        This initialisation, create an user/login database if necesssary
        """
        self.bdd_login_filename = "login_bdd"  # full path to the bdd filemane

        # if bdd_login_filename points to a regular / existing file
        if os.path.isfile(self.bdd_login_filename):  

            # open it for reading in binary mode as bdd
            with open(self.bdd_login_filename, "rb") as bdd:
                # use pickle to load bdd binary file byte stream, convert it to a Python object, and store it in .user_data
                self.user_data = pickle.load(bdd)

        # else, use the following default values for .user_data        
        else:  
            self.user_data = {
                "alexandre_winger": "user",
                "fabrice_charraud": "user",
                "michaël_deroche": "user",
                "omar_choa": "user",
                "alban_thuet": "admin",
            }
            self._save_db()


    def _save_db(self):
        # create bdd_login_filename as a new file and open it for writing in binary mode as bdd
        with open(self.bdd_login_filename, "wb") as bdd:

            # use pickle to convert .user_data from a Python object to a binary file byte stream,
            # then store it in bdd, and write bdd to bdd_login_filename
            pickle.dump(self.user_data, bdd)


    # define custom method is_()
    def is_(self, rights, login, password):
        """
        attributes: 
            rights   : string e.g.: 'user', 'admin'
            login    : string which is the name of user
            password : string
        """
        key = f"{login}_{password}"  # construct authentication chain
        
         # if authentication chain is in .user_data dictionary keys, and if requested rights match corresponding .user_data dictionary value
        if (key in self.user_data and self.user_data[key] == rights):
            return True
        return False


    def add_name(self, rights, login, password):
        """
        attributes: 
            rights   : string e.g.: 'user', 'admin'
            login    : string which is the name of user
            password : string
        """
        key = f"{login}_{password}"
        self.user_data[key] = rights
        self._save_db()


    def remove_name(self, login):
        for key in self.user_data.keys():
            if key.startswith(f'{login}_'):
                del(self.user_data[key])
                break               
        self._save_db()


if __name__ == "__main__":
    bdd = BddLogin()
    print(bdd.is_(rights="user", login="tom", password=""))  # should be False
    print(bdd.is_(rights="user", login="fabrice", password=""))  # should be False
    print(bdd.is_(rights="user", login="alexandre", password="winger")) # should be True
    print(bdd.is_(rights="admin", login="alban", password="thuet"))  # should be True
    
    # check adding name in the login database
    print('*'*80)
    print(bdd.is_(rights="user", login="seb", password="astien"))  # should be False
    bdd.add_name(rights="user", login="seb", password="astien")
    print(bdd.is_(rights="user", login="seb", password="astien"))  # should be True
    print(bdd.is_(rights="admin", login="seb", password="astien"))  # should be False (not admin, only user)

    # check removing name in the login database
    print('*'*80)
    print(bdd.is_(rights="user", login="seb", password="astien"))  # should be True
    bdd.remove_name(login="seb")
    print(bdd.is_(rights="user", login="seb", password="astien"))  # should be False

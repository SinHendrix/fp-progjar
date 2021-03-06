from classes.client_state import ClientState
import settings

class Menu:
    Login = 1
    Register = 2
    Chat = 1
    AddFriend = 2
    ListFriend = 3
    JoinRoom = 4
    MakeRoom = 5
    Shop = 6
    MyDeck = 7
    RandomRoom = 8
    CheckShop = 1
    Buy = 2
    CheckPoint = 3
    ShopBack = 4
    SendMessage = 1
    SendPicture = 2
    CheckCardInHand = 1
    CheckCardInOwnField = 2
    CheckCardInEnemyField = 3
    DrawCard = 4
    Attack = 5
    Help = 0
    Exit = 99

    @staticmethod
    def prompting():
        print("Masukkan angka perintah (0 untuk help) > ", end='', flush=True)

    @staticmethod
    def get_command():
        return int(input())

    @staticmethod
    def check_if_help_or_menu(command):
        return command == Menu.Help or command == Menu.Exit

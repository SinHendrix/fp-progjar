class Menu:
    Login = 1
    Register = 2
    Chat = 1
    AddFriend = 2
    JoinRoom = 3
    MakeRoom = 4
    RandomRoom = 5
    SendMessage = 1
    SendPicture = 2
    Help = 0
    Exit = 99

    @staticmethod
    def prompting():
        print("Masukkan angka perintah (0 untuk help) > ", end='')

    @staticmethod
    def get_command():
        return int(input())

    @staticmethod
    def check_if_help_or_menu(command):
        return command == Menu.Help or command == Menu.Exit

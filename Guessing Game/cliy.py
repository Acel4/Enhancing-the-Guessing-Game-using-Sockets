import socket


def main():
    HOST = "127.1.1.0"
    PORT = 55443

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        username = input("Enter your username: ")
        s.sendall(username.encode())
        difficulty = input("Choose difficulty (easy/medium/hard): ")
        s.sendall(difficulty.encode())

        while True:
            response = s.recv(1024).decode()
            print(response)
            if "Congratulation" in response:
                break
            guess = input()
            s.sendall(guess.encode())


main()

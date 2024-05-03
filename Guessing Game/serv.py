import socket
import random
import json


def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as file:
            leaderboard = json.load(file)
    except FileNotFoundError:
        leaderboard = {}
    return leaderboard


def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard, file)


def generate_number(difficulty):
    if difficulty == "easy":
        return random.randint(1, 50)
    elif difficulty == "medium":
        return random.randint(1, 100)
    elif difficulty == "hard":
        return random.randint(1, 500)
    else:
        return random.randint(1, 50)


def update_leaderboard(leaderboard, username, score):
    if username in leaderboard:
        leaderboard[username] = min(leaderboard[username], score)
    else:
        leaderboard[username] = score


def display_leaderboard(leaderboard):
    print("leaderboard:")
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: [1])
    for i, (name, score) in enumerate(sorted_leaderboard, start=1):
        print(f"{i}, {name}: {score} tries")


def main():
    HOST = "127.1.1.0"
    PORT = 55443

    leaderboard = load_leaderboard()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            with conn:
                print("connected by", addr)
                username = conn.recv(1024).decode()
                difficulty = conn.recv(1024).decode()

                number_to_guess = generate_number(difficulty)
                tries = 0
                while True:
                    conn.sendall(b"Guess a NO.: ")
                    guess = int(conn.recv(1024).decode())
                    tries += 1

                    if guess == number_to_guess:
                        conn.sendall(b"Congratulations you guess the right number!")
                        update_leaderboard(leaderboard, username, tries)
                        save_leaderboard(leaderboard)
                        break
                    elif guess < number_to_guess:
                        conn.sendall(b"TRy HIGHER!")
                    else:
                        conn.sendall(b"TRy LOWER!")
                display_leaderboard(leaderboard)


main()

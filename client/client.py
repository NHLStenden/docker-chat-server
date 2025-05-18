import getpass
import os
import socket
import threading
import getopt
import curses
import sys

stop_event = threading.Event()


def get_username():
    for env_var in ("USER", "USERNAME"):
        username = os.environ.get(env_var)
        if username:
            return username
    try:
        username = getpass.getuser()
        if username:
            return username
    except Exception:
        pass
    return "gast"


def listen_for_messages(client_socket, msg_win):
    while not stop_event.is_set():
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                msg_win.addstr("\n🔌 Server disconnected.\n")
                msg_win.refresh()
                stop_event.set()
                break
            msg_win.addstr(f"📩 {message}\n")
            msg_win.refresh()
        except:
            msg_win.addstr("\n❌ Connection lost.\n")
            msg_win.refresh()
            stop_event.set()
            break


def chat_ui(stdscr, client_socket, username):
    curses.curs_set(1)
    stdscr.clear()

    height, width = stdscr.getmaxyx()
    msg_win = curses.newwin(height - 3, width, 0, 0)
    input_win = curses.newwin(3, width, height - 3, 0)

    msg_win.scrollok(True)
    input_win.addstr(f"{username}: ")
    input_win.refresh()

    listener = threading.Thread(target=listen_for_messages, args=(client_socket, msg_win))
    listener.daemon = True
    listener.start()

    max_y, max_x = msg_win.getmaxyx()

    while not stop_event.is_set():
        input_win.clear()
        input_win.addstr(f"{username}: ")
        curses.echo()
        msg = input_win.getstr().decode('utf-8')
        curses.noecho()
        if msg.lower() == "exit":
            stop_event.set()
            break
        if not msg.strip():
            continue  # Skip lege of spatie-only berichten
        try:
            formatted = f"{username}: {msg}"
            client_socket.send(formatted.encode('utf-8'))
            text = f"📝 {formatted}\n"
            y, x = msg_win.getyx()
            msg_win.addstr(y, max(y, max_x - len(text) - 1), text)
            msg_win.refresh()
        except:
            stop_event.set()
            break

    client_socket.close()


def usage():
    print("Usage: python client.py [-i <ip> | --ip=<ip>] [-p <port>|--port=<port>] [-?|--help] [chatname]")


def main(argv):
    ip = "chat_server"
    port = 12345
    username = get_username()

    try:
        opts, args = getopt.getopt(argv, "i:p:?", ["ip=", "port=", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-?", "--help"):
            usage()
            sys.exit(2)

    if len(args) > 0:
        username = args[0]

    print(f"Connecting as '{username}' to {ip}:{port}")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((ip, port))
        print(f"✅ Connected to server at {ip}:{port}")
    except Exception as e:
        print(f"❌ Could not connect: {e}")
        sys.exit(1)

    try:
        client.send(f"{username} has joined the chat.".encode('utf-8'))
    except:
        print("Failed to send join message.")
        client.close()
        sys.exit(1)

    curses.wrapper(chat_ui, client, username)
    print("👋 Client shutting down.")


if __name__ == "__main__":
    main(sys.argv[1:])

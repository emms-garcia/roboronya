from roboronya.roboronya import Roboronya


def main():
    roboronya = Roboronya()
    try:
        roboronya.run()
    except KeyboardInterrupt:
        roboronya.stop()

if __name__ == '__main__':
    main()

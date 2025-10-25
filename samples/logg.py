import logging

def main():
    logging.debug("Starting system details logging...")

if __name__ == "__main__":
    logging.basicConfig(filename='logs.log', level=logging.DEBUG)
    main()
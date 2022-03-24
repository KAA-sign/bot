from apis.cbr import CbrClient
from apis.cbr import CbrError

NOTIFY = 'USD'  

def main():
    client = CbrClient()
    current_rate = client.get_last_rate(currency=NOTIFY)

    print("{} =  {}".format(NOTIFY, current_rate))
    pass


if __name__ == '__main__':
    main()
from prediction import predict


for _ in range(int(input('Enter number of urls: '))):
    try:
        print('Malicious :(' if predict(input()) else 'Safe :)')
    except:
        print("Cannot check this url :(")
        break

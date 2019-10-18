import csv


def subsidySchedule(supply=0, HALVING_INTERVAL=210000, init_subsidy=50, coin=100000000):
    with open('bitcoin_subsidy_schedule.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        head = ['block height', 'subsidy era', 'subsidy (sats)', 'total supply (sats)']
        print(head)
        filewriter.writerow(head)
        init_subsidy_total = init_subsidy * coin
        subsidy = init_subsidy_total
        for i in range(1,34):
            supply = supply + subsidy * HALVING_INTERVAL
            row = [str(HALVING_INTERVAL * i), str(i), str(subsidy), str(supply)]
            print(row)
            filewriter.writerow(row)
            subsidy = init_subsidy_total >> i
            i = i + 1


subsidySchedule()
    
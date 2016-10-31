from datetime import date
from time import sleep
import sys
import os


class Product(object):
    """This is a class for the products of a market."""
    sales = 0  # how many products did you sale
    stock = 0  # how many products you have on stock

    def __init__(self, product_name, product_price, product_cost):
        self.name = product_name
        self.price = product_price
        self.cost = product_cost

    def __repr__(self):
        return "%s ΠΩΛΕΙΤΑΙ ΣΤΑ %.2f ΕΥΡΩ ΚΑΙ ΚΟΣΤΙΖΕΙ %.2f ΕΥΡΩ" % (self.name, self.price, self.cost)

    def save_in_file(self):
        try:
            f = open('goods.txt', 'a')
        except FileNotFoundError:
            f = open('goods.txt', 'w')
        if not self.is_in_file():
            f.write("%s: ΤΙΜΗ = %.2f ΕΥΡΩ ΚΟΣΤΟΣ = %.2f ΕΥΡΩ\n" % (self.name, self.price, self.cost))
        else:
            f.close()
            items = get_objects()
            for item in items:
                if self.name == item.name:
                    item.price = self.price
                    item.cost = self.cost
            f = open('goods.txt', 'w')
            for item in items:
                f.write("%s: ΤΙΜΗ = %.2f ΕΥΡΩ ΚΟΣΤΟΣ = %.2f ΕΥΡΩ\n" % (item.name, item.price, item.cost))
        f.close()

    def is_in_file(self):
        if not find_price(self.name):
            return False
        else:
            return True

    def find_gain(self):
        """find how much money you gained from that product"""
        return self.sales * self.price

    def find_loss(self):
        """find how much money you owe for that product"""
        return self.stock * self.cost

    def find_profit(self):
        """find your intake from that product"""
        return self.find_gain() - self.find_loss()


def get_objects():
    """Fetch objects from goods.txt, returns an array of objects"""
    f = open('goods.txt', 'r')
    lines = []
    line = f.readline()
    lines.append(line)
    while line != '':
        line = f.readline()
        lines.append(line)
    # fetch name price and cost from each line
    objects = []
    for line in lines:
        prices = []
        # find the names of products
        words = line.split(' ')
        names = []
        for word in words:
            if word == 'ΤΙΜΗ':
                break
            else:
                names.append(word)
        name = ''
        for word in names:
            name = name + word + ' '
        name = name[0:-2]
        # find prices and costs of products
        for word in words:
            if isfloat(word):
                prices.append(float(word))
        if len(prices) == 2:
            price = prices[0]
            cost = prices[1]
        elif len(prices) == 1:
            price = prices[0]
            cost = 0
        else:
            price = 0
            cost = 0
        objects.append([name, price, cost])
    objects.pop()  # last line is empty
    results = []
    for item in objects:
        results.append(Product(item[0], item[1], item[2]))
    f.close()
    return results


def update_product_list():
    """A function to write or update things in your product list."""
    number_of_products = int(input("ΠΟΣΑ ΠΡΟΙΟΝΤΑ ΘΕΛΕΙΣ ΝΑ ΠΡΟΣΘΕΣΕΙΣ Η ΝΑ ΑΝΑΝΕΩΣΕΙΣ: "))
    for i in range(number_of_products):
        name = input("\nΟΝΟΜΑ ΠΡΟΙΟΝΤΟΣ: ")
        price = float(input("%s ΠΩΛΕΙΤΑΙ ΣΤΑ: " % name))
        cost = float(input("%s ΚΟΣΤΙΖΕΙ: " % name))
        item = Product(name, price, cost)
        item.save_in_file()


def print_options():
    """Print the menu options."""
    print("\n1-ΔΗΜΙΟΥΡΓΗΣΕ Η ΑΝΑΝΕΩΣΕ ΤΗΝ ΛΙΣΤΑ ΜΕ ΤΑ ΠΡΟΙΟΝΤΑ ΣΟΥ")
    print("2-ΔΙΕΓΡΑΨΕ ΕΝΑ ΠΡΟΙΟΝ ΑΠΟ ΤΗΝ ΛΙΣΤΑ")
    print("3-ΔΕΣ ΤΗΝ ΛΙΣΤΑ ΜΕ ΤΑ ΠΡΟΙΟΝΤΑ")
    print("4-ΔΙΕΓΡΑΨΕ ΟΛΟΚΛΗΡΗ ΤΗΝ ΛΙΣΤΑ")
    print("5-ΕΠΙΣΤΡΟΦΗ\n")


def wait(process):
    print("ΠΕΡΙΜΕΝΕ ΓΙΑ %s" % process, end=' ')
    sys.stdout.flush()
    sleep(0.1)
    for i in range(3):
        print('*', end=' ')
        sys.stdout.flush()
        sleep(0.1)
    print('')
    print("%s ΟΛΟΚΛΗΡΩΘΗΚΕ" % process)


def make_your_market():
    exit_loop = False
    print(" ")
    while not exit_loop:
        print_options()
        try:
            option = int(input("ΤΙ ΕΠΙΘΥΜΕΙΣ ΝΑ ΚΑΝΕΙΣ: "))
        except ValueError:
            print("\nΠΡΕΠΕΙ ΝΑ ΕΠΙΛΕΞΕΙΣ ΕΝΑΝ ΑΡΙΘΜΟ!\n")
            continue

        if option not in range(1, 6):
            print("\nΔΙΑΛΕΞΕ ΑΝΑΜΕΣΑ ΣΤΟΥΣ %s\n" % [i for i in range(1, 6)])
            continue
        elif option == 1:
            os.system('cls')  # clear the screen
            try:
                update_product_list()
                wait('ΑΝΑΝΕΩΣΗ')
            except ValueError:
                print("\nΔΩΣΕ ΕΝΑΝ ΑΡΙΘΜΟ!\n")
        elif option == 2:
            os.system('cls')  # clear the screen
            try:
                print("\nΠΡΟΙΟΝΤΑ:\n")
                if not list_of_products():
                    print("Η ΛΙΣΤΑ ΕΙΝΑΙ ΚΕΝΗ!")
                item = input("ΠΙΟ ΠΡΟΙΟΝ ΕΠΙΘΥΜΕΙΣ ΝΑ ΑΠΟΣΥΡΕΙΣ: ")
                if delete_product(item):
                    wait('ΔΙΑΓΡΑΦΗ')
            except FileNotFoundError:
                print("ΔΕΝ ΥΠΑΡΧΕΙ ΤΟ ΑΡΧΕΙΟ goods.txt!\n")
        elif option == 3:
            os.system('cls')  # clear the screen
            try:
                wait('ΕΚΤΥΠΩΣΗ')
                print("\nΠΡΟΙΟΝΤΑ:\n")
                if not list_of_products():
                    print("Η ΛΙΣΤΑ ΕΙΝΑΙ ΚΕΝΗ!")
            except FileNotFoundError:
                print("ΔΕΝ ΥΠΑΡΧΕΙ ΤΟ ΑΡΧΕΙΟ goods.txt!\n")
        elif option == 4:
            response = input("ΕΙΣΑΙ ΣΙΓΟΥΡΟΣ (ΝΑΙ/ΟΧΙ)?").lower()
            if response == 'ναι' or response == 'ν':
                wait('ΔΙΑΓΡΑΦΗ ΛΙΣΤΑΣ')
                delete_products()
            else:
                pass
        elif option == 5:
            os.system('cls')  # clear the screen
            print("\nΕΠΙΣΤΡΟΦΗ!\n")
            exit_loop = True


def format_date():
    return str(date.today().day) + '-' + str(date.today().month) + '-' + str(date.today().year)


def month_format(number):
    if number == 1:
        return 'ΙΑΝΟΥΑΡΙΟΣ'
    elif number == 2:
        return 'ΦΕΒΡΟΥΑΡΙΟΣ'
    elif number == 3:
        return 'ΜΑΡΤΙΟΣ'
    elif number == 4:
        return 'ΑΠΡΙΛΙΟΣ'
    elif number == 5:
        return 'ΜΑΙΟΣ'
    elif number == 6:
        return 'ΙΟΥΝΙΟΣ'
    elif number == 7:
        return 'ΙΟΥΛΙΟΣ'
    elif number == 8:
        return 'ΑΥΓΟΥΣΤΟΣ'
    elif number == 9:
        return 'ΣΕΠΤΕΜΒΡΙΟΣ'
    elif number == 10:
        return 'ΟΚΤΩΜΒΡΙΟΣ'
    elif number == 11:
        return 'ΝΟΕΜΒΡΙΟΣ'
    else:
        return 'ΔΕΚΕΜΒΡΙΟΣ'


def compute_your_day():
    items = get_objects()
    if len(items) > 0:
        for item in items:
            item.sales = int(input("ΠΟΣΑ %s ΠΟΥΛΗΣΕΣ: " % item.name))
            item.stock = int(input("ΠΟΣΑ %s ΠΑΡΗΓΓΕΙΛΕΣ: " % item.name))

        gain = 0
        loss = 0

        for item in items:
            # print("For %s you need to pay %0.2f and gained %0.2f." % (item.name, item.find_loss(), item.find_gain()))
            gain += item.find_gain()
            loss += item.find_loss()

        wait('ΥΠΟΛΟΓΙΣΜΟΣ')
        print('\nΤΖΙΡΟΣ = %0.2f ΕΥΡΩ' % gain)
        print('\nΧΡΩΣΤΟΥΜΕΝΑ = %0.2f ΕΥΡΩ' % loss)
        print('\nΚΑΘΑΡΑ ΚΕΡΔΗ = %0.2f ΕΥΡΩ\n' % (gain - loss))

        # make a directory if it doesn't exist
        directory = './ΗΜΕΡΟΛΟΓΙΟ/%d/%s' % (date.today().year, month_format(date.today().month))
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open('%s/%s.txt' % (directory, format_date()), 'w')
        f.write('ΤΖΙΡΟΣ = %0.2f ΕΥΡΩ\n' % gain)
        f.write('\nΧΡΩΣΤΟΥΜΕΝΑ = %0.2f ΕΥΡΩ\n' % loss)
        f.write('\nΚΑΘΑΡΑ ΚΕΡΔΗ = %0.2f ΕΥΡΩ\n' % (gain - loss))
        f.write('\nΑΝΑΛΥΤΙΚΑ:\n')
        for item in items:
            f.write('\n%s ΠΟΥΛΗΣΕΣ %d ΚΑΙ ΠΑΡΗΓΓΕΙΛΕΣ %d\n' % (item.name, item.sales, item.stock))
        f.close()

    else:
        print("\nΠΡΕΠΕΙ ΠΡΩΤΑ ΝΑ ΕΙΣΑΓΕΙΣ ΤΑ ΠΡΟΙΟΝΤΑ ΣΟΥ!\n")


def find_price(good):
    """Find product named good in file."""
    try:
        f = open('goods.txt', 'r')
    except FileNotFoundError:
        # print("file goods.txt doesn't exist") for debugging
        return False
    counter = 1
    line = f.readline()
    while line != '':
        counter += 1
        if good in line:
            # print("%s is in line %d of file goods.txt" % (good, counter)) for debugging
            for word in line.split(' '):
                if isfloat(word):
                    return float(word)
            else:
                # print("%s doesn't have a price" % good) for debugging
                return False
        line = f.readline()
    else:
        # print("%s is not in file goods.txt" % good) for debugging
        return False


def isfloat(value):
    """Checks if value is a float"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def list_of_products():
    """Read the file of products."""
    f = open('goods.txt', 'r')
    line = f.readline()
    print(line)
    if line == '':
        return False
    while line != '':
        line = f.readline()
        print(line)
    f.close()
    return True


def delete_products():
    """Delete the file of products."""
    f = open('goods.txt', 'w')
    f.write('')
    f.close()


def delete_product(product):
    """Delete a specific product."""
    f = open("goods.txt", "r")
    lines = f.readlines()
    f.close()
    exist = False
    f = open("goods.txt", "w")
    for line in lines:
        if product not in line:
            f.write(line)
        else:
            exist = True
    f.close()
    if not exist:
        print("\n%s ΔΕΝ ΕΙΝΑΙ ΚΑΤΑΧΩΡΗΜΕΝΟ\n" % product)
        return False
    else:
        return True


def intro():
    os.system('cls')  # clear the screen
    print('')
    print('|\\    /\\     /\\   |-   | / |-- --|--')
    print('| \\  /  \\   /--\\  |_|  |/  |--   |  ')
    print('|  \\/    \\ /    \\ | \\  |\\  |__   |  ')
    print('')


if __name__ == '__main__':
    exit_loop = False
    intro()
    print("\nΚΑΛΩΣ ΟΡΙΣΑΤΕ ΣΤΗΝ ΕΦΑΡΜΟΓΗ MARKET!\n")
    while not exit_loop:
        print("1-ΚΑΤΑΧΩΡΗΣΕ ΤΑ ΠΡΟΙΟΝΤΑ ΤΟΥ ΜΑΓΑΖΙΟΥ ΣΟΥ.")
        print("2-ΚΑΤΑΧΩΡΗΣΕ ΤΙΣ ΠΩΛΗΣΕΙΣ ΚΑΙ ΤΙΣ ΠΑΡΑΓΓΕΛΙΕΣ ΠΟΥ ΕΚΑΝΕΣ ΣΗΜΕΡΑ.")
        print("3-ΕΞΟΔΟΣ.")
        try:
            option = int(input("\nΤΙ ΕΠΙΘΥΜΕΙΣ ΝΑ ΚΑΝΕΙΣ: "))
        except ValueError:
            print("\nΠΡΕΠΕΙ ΝΑ ΕΠΙΛΕΞΕΙΣ ΕΝΑΝ ΑΡΙΘΜΟ!\n")
            continue
        if option not in range(1, 4):
            os.system('cls')  # clear the screen
            print("\nΕΠΕΛΕΞΕ ΑΝΑΜΕΣΑ ΣΤΟΥΣ %s\n" % [i for i in range(1, 4)])
            continue
        elif option == 1:
            os.system('cls')  # clear the screen
            make_your_market()
        elif option == 2:
            os.system('cls')  # clear the screen
            try:
                compute_your_day()
            except FileNotFoundError:
                print('ΔΕΝ ΥΠΑΡΧΕΙ ΤΟ ΑΡΧΕΙΟ goods.txt!')
        elif option == 3:
            os.system('cls')  # clear the screen
            print("\nΕΙΣ ΤΟ ΕΠΑΝΙΔΕΙΝ!\n")
            exit_loop = True

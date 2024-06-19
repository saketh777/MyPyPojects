def collatz(number):
    if number % 2 == 0:
        result = number // 2
    else:
        result = 3 * number + 1
    print(result)
    return result

def main():
    while True:
        try:
            number = int(input("Enter an integer: "))
            break  # Exit the loop if a valid integer is entered
        except ValueError:
            print("You must enter an integer. Please try again.")

    while number != 1:
        number = collatz(number)

if __name__ == "__main__":
    main()

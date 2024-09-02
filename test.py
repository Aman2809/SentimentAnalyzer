def greet(name):
    
    return f"Hello, {name}! Welcome to your new Python project."

def main():
    user_name = input("Please enter your name: ")
    greeting = greet(user_name)
    print(greeting)

if __name__ == "__main__":
    main()
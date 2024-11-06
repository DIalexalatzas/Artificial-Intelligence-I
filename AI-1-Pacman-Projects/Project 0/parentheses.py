class Stack:
    def __init__(self):
        self.elements = []

    def size(self):
        return len(self.elements)

    def empty(self):
        if self.size() == 0:
            return True
        else:
            return False

    def push(self, element):
        self.elements.append(element)

    def pop(self):
        return self.elements.pop()


def parentheses(expression):
    mystack = Stack()   # Initialise an empty stack
    n = len(expression)
    i = 0
    while i < n:
        d = expression[i]   # Index for the input expression
        if d == '(' or d == '[' or d == '{':
            mystack.push(d)  # Push the left parentheses in the stack
        elif d == ')' or d == ']' or '}':
            if mystack.empty():  # If stack is empty and we encounter a right parentheses, they are not balanced
                print("More right parentheses than left parentheses")
                return
            else:  # Pop the top element and check if it matches
                c = mystack.pop()
                if (c == '(' and d != ')') or (c == '[' and d != ']') or (c == '{' and d != '}'):
                    print("Mismatched parentheses:", c, "and", d)
                    return
        i += 1
    if mystack.empty():
        print("Parentheses are balanced properly")
    else:
        print("More left parentheses than right parentheses")


def main():     # Main function
    expression = input("Give input expression without blanks:")
    parentheses(expression)


if __name__ == "__main__":
    main()

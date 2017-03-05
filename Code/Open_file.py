def main():
    """
        Add Documentation here
    """

    print "I am HERE!"

    print "Did u know that?"

    print "Oh and I'm going to use an additional file!"

    with open("Hello_World.py", 'r') as f:

        content = f.read()

        print "Hello, I'm the opened file, my content is:", content

if __name__ == '__main__':
    main()
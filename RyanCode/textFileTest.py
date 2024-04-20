#this creates a new file
f = open("test.txt", 'a') #f for file. a is the flag for append. if file isn't present then create it. If present then add the data to it
f.write("This is a new line\n")
f.close()

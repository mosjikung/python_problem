# Create a dictionary
my_dict = {'apple': 2, 'banana': 3, 'orange': 1}

# Create another dictionary to update from
update_dict = {'apple': 5, 'orange': 2, 'mango': 4}

# Loop through the items in the update dictionary and update the original dictionary
for key, value in  enumerate(update_dict):
    print (key)
    my_dict.update({key: value})

# Print the updated dictionary
print(my_dict)

from bs4 import BeautifulSoup
import requests
import pandas as pd

# Functions
# Normalize data
def normalize(data):
    data = data.strip(" ")
    data = data.strip("\n")
    data = data.rstrip()
    data = data.strip('"')
    data = data.strip("'")
    return data

# Login website
url = 'https://website.com/'
login = 'wp-login.php'

# Use this so the connection would simulate a broswer connection.
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'origin' : url,
    'Referer' : 'https://website-to-go-after-accessing/access/',
}

# Define a session so you won't be logged out.
s = requests.session()

# Login information
# Check the "log" and "pwd" words using the normal browser, they could be different depending the website.
# "wp-submit" is an extra payload information that could be required to connect.
payload = {
    'log' : 'username',
    'pwd' : 'password',
    'wp-submit' : 'ENTER'
}

# Connect using the headers and the login information.
login_request = s.post(url + login, headers=headers, data=payload)
print(login_request.status_code)
cookies = login_request.cookies

# When pages uses a pagination, create a loop to automatically itter over the pages.
for i in range(1,2):
    scrapping_url = f'web-example/admin.php?s=sold+houses&paged={i}'
    # Read the url by joining the main url and the sub url.
    soup = BeautifulSoup(s.get(url + scrapping_url).text, 'html.parser')

    #Just for you to know what page is being worked on.
    print(f"\n----------Working on page: {i}----------")

    # All this information should be adapted to the HTML of each website.

    # Get all name on the current paged website and add them to the list.
    name_list = []
    name_list.clear()
    name = soup.find_all('td', class_='comment column-comment has-row-actions column-primary')
    for text in name:
        text = normalize(text.text)
        name_list.append(text)

    # Get users
    users_list = []
    users_list.clear()
    users = soup.find_all('td', class_='members column-members')
    for text in users:
        text = normalize(text.text)
        users_list.append(text)

    # Get last active
    active_list = []
    active_list.clear()
    count = 0
    active = soup.find_all('td', class_='last_active column-last_active')
    for text in active:
        text = normalize(text.text)
        active_list.append(text)

    # If you need specific information at the end of a scrapped text, you can itter backwards to get it.
    # Get year
    year_list = []
    year_list.clear()
    year = soup.find_all('td', class_='comment column-comment has-row-actions column-primary')
    for text in year:
        text = normalize(text.text)
        text = text[-53:-49]
        year_list.append(text)


    # Create a list with the scrapped information in order to add it to the data frame.
    full_list = []
    # Get the quantity of object inside the list so you can properly itter and join the correct information using the index.
    # Eg. "Users_list[1]"" should be joined with "name_list[1]", "active_list[1], etc."
    for i in range(len(name_list)):
        item = [users_list[i], name_list[i], active_list[i], year_list[i]]
        full_list.append(item)

    print("----------DataFrame----------\n")
    # Add the "full_list" to a data frame and format it with the headings.
    df = pd.DataFrame(full_list, columns=["Groups", "Name", "Last time","Year"])
    # Export the information as csv to use the persistent memory.
    df.to_csv('Grupos', mode='a', index=False, header=False)
    print(df)

s.close()
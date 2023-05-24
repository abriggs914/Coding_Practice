import requests
import pandas as pd
from bs4 import BeautifulSoup


if __name__ == '__main__':

    # Send a GET request to the URL
    url = "https://www.officepools.com/nhl/classic/auth/2022/playoff/BWSPool2023/hockey"
    response = requests.get(url)
    print(f"{response=}")
    print(f"{response.content=}")

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")
    print(f"{soup=}")

    # Find the first table in the webpage
    first_table = soup.find("table")
    print(f"{first_table=}")

    if first_table:
        # Convert the first table to HTML string
        table_html = str(first_table)

        # Read the HTML table into a DataFrame
        df = pd.read_html(table_html)

        if len(df) > 0:
            # Print the first DataFrame from the list
            print("First Table:")
            print(df[0])
        else:
            print("No tables found in the first table tag.")
    else:
        print("No table tags found on the webpage.")

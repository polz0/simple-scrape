from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import matplotlib.pyplot as plt
import re

def main():
    
    # send request to known url
    request = Request(
        url='https://fred.stlouisfed.org/release/tables?rid=50&eid=3029&od=#', 
        headers={'User-Agent': 'Mozilla/6.0'}
    )

    # retrieve encoded html and close connection
    url_client = urlopen(request)
    encoded_html = url_client.read()
    url_client.close()

    # decode html and write to separate file for analysis
    site_html = encoded_html.decode('utf-8')
    print("Writing HTML to file...")
    open('target_url.html', 'w').write(site_html)

    # parse html into tags
    page_soup = soup(site_html, "html.parser")
    data_elements = page_soup.select('tr') #[class*=fred-rls-elm-ck-td]

    # create dataframe of retrieved data, force into float type
    create_dataframe(data_elements)
    df = create_dataframe(data_elements)
    df=df.astype(float)

    # ask user for viewing preference
    opt = int(input("Hello, would you like to see unemployment rate by 1) AGE GROUP, 2) GENDER, 3) MARITAL STATUS, or 4) FULL/PART-TIME STATUS?" + "\n"
                    + "Please enter 1, 2, 3, or 4. NOTE: CURRENTLY ONLY OPTIONS 3 AND 4 FUNCTIONAL." + "\n"))
    if opt == 2:
        gender_opt = int(input("Would you like to see unemployment rate for 1) WOMEN or 2) MEN? Please enter 1 or 2" + "\n"))
    else:
        gender_opt = 0

    # select portion of df to be plotted
    filtered_df = select_data(df, opt, gender_opt)
    print("\n", "Printing selected data....")
    print("\n", "DATA:", "\n", filtered_df)

    # set title, legend position, and plot
    title = page_soup.find('title')
    filtered_df.T.plot.line()
    plt.title(title.text.strip(), wrap=True)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05))
    plt.savefig('figure.png', bbox_inches='tight')
    plt.show(block=True)
    

def create_dataframe(list_elements): 
    #rows 0,1,2 of example url not data, data starts at row 3 of html
    rows_list = []
    col_names = []
    row_names = []

    #iterate through all rows of html
    for row_element in list_elements:

        # <td> elements are data, append to list 'row' if not empty
        if row_element.find_all('td'):
            row = []

            for component in row_element.find_all("td"):
                if component.text.strip() != "":
                    row.append(component.text.strip())

            if row:
                rows_list.append(row)
        # <th> elements are headers, append to list 'headers'
        elif row_element.find_all('th'):
            for component in row_element.find_all("th"):
                if any(char.isdigit() for char in component.text.strip()):
                    col_names.append(component.text.strip())

        # <span> elements are category names, append to list 'row_names'
        if row_element.find_all('span'):
            for component in row_element.find_all('span'):
                label = component.text.strip()
                if not label.isupper():
                    row_names.append(label)

    # dangerous, need to fix
    row_names = [x for x in row_names if x not in col_names]

    # convert list of lists to dataframe and return
    frame = pd.DataFrame(rows_list, columns=col_names, index=row_names)
    return frame

def select_data(df, opt, gender):
    row_names = df.index.to_list()
    selected_rows = []

    if opt == 4:
        for row in row_names:
            if re.findall(r'worker', row, re.IGNORECASE):
                selected_rows.append(row)
    elif opt == 3:
        for row in row_names:
            if re.findall(r'men', row, re.IGNORECASE):
                selected_rows.append(row)

    selected_rows = [str(r) for r in selected_rows]
    return(df.loc[selected_rows])


if __name__ == '__main__':
    main()
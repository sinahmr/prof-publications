

# Professors' Publications Finder

A simple tool for speeding up the process of searching for professors' newest publications. It runs a simple Sanic web server on `localhost:8000`.

#### Install
```bash
# If you have both Python2 and Python3 installed, you may need using pip3 instead of pip.
pip install -r requirements.txt
```
#### Prepare
Create a file named `university_name.txt` and place it in the [lists](./lists) folder. Add the name of the professors you are going to find out more about, each in a new line. You can add a blank line to have a separator in the output list view. Add as many `university_name.txt` files as you want.


#### Run
Open a terminal and activate your python virtual environment, then run
```bash
python3 main.py
```
Now open a browser and navigate to `127.0.0.1:8000/` to see the list of your desired universities. Click on each to see the list of their professors, mentioned in the corresponding `.txt` file.

In each of the university's pages, there are 3 links beside professors' names:
- `scholar`: Searches the professor's name and his/her university in Google Scholar Profiles.
- `search`: Searches the professor's name and his/her university in Google search.
- `auto`: It is designed to save you a couple of clicks, and is the main reason I have created this repository. It searches the professor's name and his/her university in Google Scholar Profiles. Now,
  - If a single result is found, redirects you to the professor's publications page, sorted by publication date;
  - If multiple results are found, redirects you to the Google Scholar Profiles search page, so that you can choose your desired profile;
  - If no result is found in Google Scholar Profiles, you will be redirected to Google search, so maybe you can find about the professor's publications somewhere else (maybe in his/her home page).

A few example `.txt` files are added in the [lists](./lists) folder. Note that names that appear multiple times in the `.txt` files will be shown only once in the list of professors.

## Update Feb. 12, 2020   
Added some unimportant features:

- Logo for Universities
- Professors' profile picture
- A simple CSS style

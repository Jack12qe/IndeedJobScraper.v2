import requests
from bs4 import BeautifulSoup

LIMIT = 50


def extract_last_page(URL):
    # return 'requests.models.Response'
    # it is the structure of html of indeed
    indeed_result = requests.get(URL)

    # return 'bs4.BeautifulSoup'
    indeed_soup = BeautifulSoup(indeed_result.text, "html.parser")

    # return 'bs4.element.Tag'
    pagination = indeed_soup.find("ul", {"class": "pagination-list"})

    # return element.ResultSet'
    links = pagination.find_all("a")

    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(link):
    # getting job name
    job_td = link.find("td", {"class", "resultContent"})
    # don't progress if it is not job post
    if job_td is None:
        return None
    job_header = job_td.find("div", {"class", "heading4"})
    # get a job name
    job_name = job_header.find("a").find("span").string

    company_name = extract_company_name(job_td)
    company_loc = extract_company_location(job_td)
    job_income = extract_job_income(job_td)
    job_post_link = search_job_link(job_td)

    return {
        "title": job_name,
        "company": company_name,
        "income": job_income,
        "location": company_loc,
        "link": job_post_link,
    }


def extract_job_income(job_td):
    job_income_element = job_td.find(
        "div", {"class": "heading6 tapItem-gutter metadataContainer"}
    ).find("div", {"class": "salary-snippet"})
    if job_income_element:
        job_income = job_income_element.get_text()
        # job_income = escape_comma(job_income)
    else:
        job_income = "None information"
    return job_income


def search_job_link(job_td):
    company_id = job_td.find("div", {"class", "heading4"}).find("a")["data-jk"]
    link = f"https://jp.indeed.com/%E4%BB%95%E4%BA%8B?jk={company_id}"
    return link


def extract_company_name(job_td):
    # getting company name
    company_div = job_td.find(
        "div", {"class", "heading6 company_location tapItem-gutter companyInfo"}
    )
    company_span = company_div.find("span", {"class", "companyName"})
    # get a company name
    if company_span is None:
        company_name = "company name: none"
    else:
        company_name = company_span.string
    return company_name


def extract_company_location(job_td):
    company_div = job_td.find(
        "div", {"class", "heading6 company_location tapItem-gutter companyInfo"}
    )
    company_loc = company_div.find("div", {"class": "companyLocation"}).get_text()
    return company_loc


def extract_jobs(URL, last_page):
    global LIMIT
    jobs = []
    for page in range(last_page):
        print(f"Scraping page: {page + 1}")
        result_url = f"{URL}&start={page*LIMIT}"
        result_html = requests.get(result_url)
        soup = BeautifulSoup(result_html.text, "html.parser")
        # list of each job post
        links = soup.find("ul", {"class", "jobsearch-ResultsList"})
        for link in links:
            job_obj = extract_job(link)
            # exclude if job object is none
            if job_obj is None:
                continue
            jobs.append(job_obj)
    return jobs


def get_jobs(searchKeyWord):
    global LIMIT
    URL = f"https://jp.indeed.com/%E6%B1%82%E4%BA%BA?q={searchKeyWord}&limit={LIMIT}"
    last_page = extract_last_page(URL)
    indeed_jobs = extract_jobs(URL, last_page)
    return indeed_jobs

import json
import boto3
import io
import os
import ast
from jobscraper import JobPosting, Company
from helper_functions import send_email, upload_file, read_df, get_new_postings
import pandas as pd


def lambda_handler(event, context):

    bucket_name = "jobscraper-bucket"
    file_path = "postings.csv"

    postings_df = read_df(bucket_name, file_path)
    companies_df = pd.read_csv("companies.csv")
    companies = companies_df["Company"]

    updated_postings = []
    for i in range(len(companies)):

        scraping_info = ast.literal_eval(companies.iloc[i])
        company_name = scraping_info[0]
        curr_company = Company(
            name=company_name, site_link=scraping_info[1], scrape_protocol=scraping_info[2])

        curr_postings = curr_company.fetch_current_postings()

        if company_name in postings_df.columns:
            prev_postings = postings_df[company_name].iloc[0]

            new_postings = get_new_postings(
                str(curr_postings), str(prev_postings))

            postings_df[company_name] = [new_postings]
            updated_postings += new_postings

        else:
            updated_postings += curr_postings
            postings_df[company_name] = [curr_postings]

    if updated_postings:

        email_subject = str(updated_postings[0])
        email_body = ""
        for posting in updated_postings:
            email_body += str(posting) + "\n\n"

        send_email(email_subject, email_body)
        upload_file(bucket_name, postings_df, file_path)

        return "New postings posted"

    return "No new postings"

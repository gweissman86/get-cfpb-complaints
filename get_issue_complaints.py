import csv
import requests
import json

def get_complaints(start_date, end_date):

    url = r'https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/trends?date_received_min={}&date_received_max={}&lens=product&sub_lens=issue&sub_lens_depth=50&trend_depth=50&trend_interval=year'
    
    r = requests.get(url.format(start_date, end_date))
    r_dict = r.json()
    product_dicts = r_dict['aggregations']['product']['product']['buckets']

    complaint_counts = []
    for product_dict in product_dicts:
        product = product_dict['key']
        issue_dicts = product_dict['sub-issue']['buckets']
        for issue_dict in issue_dicts:
            issue = issue_dict['key']
            complaints = issue_dict['doc_count']
            complaint_counts.append([product, issue, complaints])

    complaint_counts.sort(key=lambda row: row[1])
    complaint_counts.sort(key=lambda row: row[0])

    csv_filename = f'complaints_{start_date}_{end_date}.csv'

    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Product', 'Issue', 'Complaints'])
        for row in complaint_counts:
            csv_writer.writerow(row)
        
    input(f'Complaint data saved as {csv_filename}')
    
start_date = input("Enter complaint start date in format 'YYYY-MM-DD':")
end_date = input("Enter complaint end date in format 'YYYY-MM-DD':")

get_complaints(start_date, end_date)



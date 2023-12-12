import json
from datetime import date
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def get_data(username):
    authenticator = IAMAuthenticator(
        "EWxgC_Bv2XBMBTnKXmkMi5uz6BFm9zx-3a9BETDvxLSJ")
    service = CloudantV1(authenticator=authenticator)
    DB_NAME = 'journalentries'

    service.set_service_url(
        "https://9baa4b99-e5d7-4cf0-8540-d2ff0b9c0b07-bluemix.cloudantnosqldb.appdomain.cloud")

    response = service.post_find(db=DB_NAME, selector={"username": {
                                 "$eq": username}}).get_result()

    user_data = response['docs']

    return user_data


def add_entry(incoming_data):

    authenticator = IAMAuthenticator(
        "EWxgC_Bv2XBMBTnKXmkMi5uz6BFm9zx-3a9BETDvxLSJ")
    service = CloudantV1(authenticator=authenticator)
    DB_NAME = 'journalentries'
    service.set_service_url(
        "https://9baa4b99-e5d7-4cf0-8540-d2ff0b9c0b07-bluemix.cloudantnosqldb.appdomain.cloud")

    date_now = date.today().strftime("%Y-%m-%d")

    new_entry = {
        "username": incoming_data["username"],
        "date": date_now,
        "journal_title": incoming_data["journal_title"],
        "public": incoming_data["public"],
        "content": incoming_data["content"],
        "mood": incoming_data["mood"]
    }

    dict = {
        "entry": new_entry
    }

    response = service.post_document(
        db='journalentries', document=dict['entry'])

    print("added")


def get_public_data():

    authenticator = IAMAuthenticator(
        "EWxgC_Bv2XBMBTnKXmkMi5uz6BFm9zx-3a9BETDvxLSJ")
    service = CloudantV1(authenticator=authenticator)
    DB_NAME = 'journalentries'

    service.set_service_url(
        "https://9baa4b99-e5d7-4cf0-8540-d2ff0b9c0b07-bluemix.cloudantnosqldb.appdomain.cloud")

    response = service.post_find(
        db=DB_NAME, selector={"public": {"$eq": "true"}}).get_result()

    user_data = response['docs']

    return user_data

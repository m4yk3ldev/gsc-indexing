from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import pandas as pd

# https://developers.google.com/search/apis/indexing-api/v3/prereqs#header_2
JSON_KEY_FILE = "indexing-api-330403-4e76f72be32c.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
http = credentials.authorize(httplib2.Http())


def indexURL(urls, http):
    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

    for u in urls:

        content = {'url': u.strip(), 'type': "URL_UPDATED"}
        json_ctn = json.dumps(content)

        response, content = http.request(ENDPOINT, method="POST", body=json_ctn)

        result = json.loads(content.decode())

        # For debug purpose only
        if "error" in result:
            print("Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"],
                                              result["error"]["message"]))
        else:
            print("urlNotificationMetadata.url: {}".format(result["urlNotificationMetadata"]["url"]))
            print("urlNotificationMetadata.latestUpdate.url: {}".format(
                result["urlNotificationMetadata"]["latestUpdate"]["url"]))
            print("urlNotificationMetadata.latestUpdate.type: {}".format(
                result["urlNotificationMetadata"]["latestUpdate"]["type"]))
            print("urlNotificationMetadata.latestUpdate.notifyTime: {}".format(
                result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]))


"""
data.csv has 2 columns: URL and date.
I just need the URL column.
"""
csv = pd.read_csv("Tabla.csv")
csv[["URL"]].apply(lambda x: indexURL(x, http))

from httpx import request
import requests

req = request(
    "GET",
    "https://translate-pa.googleapis.com/v1/translate",
    params={
        "params.client":"gtx",
        "query.source_language":"auto",
        "query.target_language":"bn",
        "query.display_language":"en-GB",
        "query.text":"hello",
        "key":"AIzaSyDLEeFI5OtFBwYBIoK_jj5m32rZK5CkCXA",
        "data_types":["TRANSLATION","SENTENCE_SPLITS","BILINGUAL_DICTIONARY_FULL"]
    },
)
print(req.json())

request_info = {
    "Request URL":"https://translate-pa.googleapis.com/v1/translate?params.client=gtx&query.source_language=auto&query.target_language=bn&query.display_language=en-GB&query.text=Download&key=AIzaSyDLEeFI5OtFBwYBIoK_jj5m32rZK5CkCXA&data_types=TRANSLATION&data_types=SENTENCE_SPLITS&data_types=BILINGUAL_DICTIONARY_FULL",
    "Request Method" :"GET",
    "Remote Address":"[2404:6800:4002:830::200a]:443",
    "Referrer Policy ":"strict-origin-when-cross-origin"
}
queary = {
    "params.client" :"gtx",
    "query.source_language":"auto",
    "query.target_language":"bn",
    "query.display_language":"en-GB",
    "query.text":"Download",
    "key":"AIzaSyDLEeFI5OtFBwYBIoK_jj5m32rZK5CkCXA",
    "data_types":"TRANSLATION",
    "data_types":"SENTENCE_SPLITS",
    "data_types":"BILINGUAL_DICTIONARY_FULL"
}
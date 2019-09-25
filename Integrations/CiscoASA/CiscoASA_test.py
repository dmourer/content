import demistomock as demisto
import requests
from CiscoASA import Client

MOCK_RULES_GLOBAL = {
                      "kind": "collection#ExtendedACE",
                      "selfLink": "https://example.com/api/access/global/rules",
                      "rangeInfo": {
                        "offset": 0,
                        "limit": 1,
                        "total": 1
                      },
                      "items": [
                        {
                          "kind": "object#ExtendedACE",
                          "selfLink": "https://example.com/api/access/global/rules/1090940913",
                          "permit": True,
                          "sourceAddress": {
                            "kind": "IPv4Address",
                            "value": "8.8.8.8"
                          },
                          "destinationAddress": {
                            "kind": "AnyIPAddress",
                            "value": "any"
                          },
                          "sourceService": {
                            "kind": "NetworkProtocol",
                            "value": "ip"
                          },
                          "destinationService": {
                            "kind": "NetworkProtocol",
                            "value": "ip"
                          },
                          "active": True,
                          "remarks": [],
                          "ruleLogging": {
                            "logInterval": 300,
                            "logStatus": "Default"
                          },
                          "position": 1,
                          "isAccessRule": True,
                          "objectId": "1090940913"
                        },
{
                          "kind": "object#ExtendedACE",
                          "selfLink": "https://example.com/api/access/global/rules/123456789",
                          "permit": True,
                          "sourceAddress": {
                            "kind": "IPv4Address",
                            "value": "1.1.1.1"
                          },
                          "destinationAddress": {
                            "kind": "AnyIPAddress",
                            "value": "any"
                          },
                          "sourceService": {
                            "kind": "NetworkProtocol",
                            "value": "ip"
                          },
                          "destinationService": {
                            "kind": "NetworkProtocol",
                            "value": "ip"
                          },
                          "active": True,
                          "remarks": [],
                          "ruleLogging": {
                            "logInterval": 300,
                            "logStatus": "Default"
                          },
                          "position": 1,
                          "isAccessRule": True,
                          "objectId": "123456789"
                        }
                      ]
                    }


def test_get_all_rules(requests_mock):

    from CiscoASA import list_rules_command

    requests_mock.get("https://example.com/api/access/global/rules", json=MOCK_RULES_GLOBAL, status_code=200)

    client = Client("https://example.com", auth=("username", "password"), verify=False, proxy=False)

    args = {"interface_type": "Global"}

    _, outputs, _ = list_rules_command(client, args)

    #Assert that the rules  are exported as expected (in the outputs)
    assert '1090940913' == outputs.get('CiscoASA.Rules(val.ID && val.ID == obj.ID)')[0].get("ID")
    assert '123456789' == outputs.get('CiscoASA.Rules(val.ID && val.ID == obj.ID)')[1].get("ID")

    empty_mock = {
                  "selfLink": "https://example.com/api/access/out",
                  "rangeInfo": {
                    "offset": 0,
                    "limit": 0,
                    "total": 0
                  },
                  "items": []
                }
    requests_mock.get("https://example.com/api/access/global/rules", json=empty_mock, status_code=200)

    _, outputs, _ = list_rules_command(client, args)


    # Assert outputs is empty when there's no rule
    assert [] == outputs.get('CiscoASA.Rules(val.ID && val.ID == obj.ID)')


def test_rule_by_id(requests_mock):
    from CiscoASA import rule_by_id_command

    requests_mock.get("https://example.com/api/access/global/rules/123456789", json=MOCK_RULES_GLOBAL.get('items')[1],
                      status_code=200)

    client = Client("https://example.com", auth=("username", "password"), verify=False, proxy=False)

    args = {"interface_type": "Global",
            "interface_name": 'name',
            'rule_id': '123456789'
            }

    _, outputs, _ = rule_by_id_command(client, args)

    # Assert that the rule is exported as expected (in the outputs)
    assert '123456789' == outputs.get('CiscoASA.Rules(val.ID && val.ID == obj.ID)')[0].get("ID")


def test_create_rule(requests_mock):
    args = {
        'source': "any",
        'destination': "1.1.1.1",
        'permit': "True",
        'interface_name': "",
        'interface_type': "Global",
        'remarks': "This,is,remark",
        'position': 2,
        'logging_level':"Default",
        'active': 'True'
    }

    requests_mock.post("https://example.com/api/access/global/rules", json=MOCK_RULES_GLOBAL.get('items')[1],
                      status_code=201)

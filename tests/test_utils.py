import utils as sut
import json
import pytest

SLACK_WORKFLOW_BUILDER_WEBHOOK_VARIABLES_MAX = 20

def assert_dict_is_flat(d: dict):
    for k,v in d.items():
        assert type(v) != dict

###############################################
# Tests
###############################################

def test_is_valid_slack_channel_name_too_long():
    name = "a" * 81
    is_valid = sut.is_valid_slack_channel_name(name)
    assert not is_valid


def test_is_valid_slack_channel_name_has_spaces_and_caps():
    name = "CAP_nocap woh"
    is_valid = sut.is_valid_slack_channel_name(name)
    assert not is_valid


def test_is_valid_slack_channel_name_happy_path():
    # Channel names may only contain lowercase letters, numbers, hyphens, underscores and be max 80 chars.
    name = "acceptable-channel-name_1"
    is_valid = sut.is_valid_slack_channel_name(name)
    assert not is_valid


def test_is_valid_url_happy_path_http():
    url = "http://abcdefg.com/you/arent-here/"
    is_valid = sut.is_valid_url(url)
    assert is_valid


def test_is_valid_url_happy_path_https():
    url = "https://abcdefg.com/you/ssl/"
    is_valid = sut.is_valid_url(url)
    assert is_valid


def test_is_valid_url_garbage():
    url = "silly other input text"
    is_valid = sut.is_valid_url(url)
    assert not is_valid


def test_load_json_body_from_input_with_nested_json():
    # testing scenario of JSON string output from previous step,
    # wanting to use it inside the JSON body of another webhook.
    input_str = """
{
"user": "Kevin Quinn",
"found": "TKM6AU1FG",
"webhook_status": "200",
"webhook_resp": ""{  \\"statusCode\\" : 200}""
}
"""
    body = sut.load_json_body_from_input_str(input_str)
    assert type(body) is dict

def test_flatten_payload_reaction_added():
    e = {
        "type": "reaction_added",
        "user": "U024BE7LH",
        "reaction": "thumbsup",
        "item_user": "U0G9QF9C6",
        "item": {
            "type": "message",
            "channel": "C0G9QF9GZ",
            "ts": "1360782400.498405"
        },
        "event_ts": "1360782804.083113"
    }
    new_payload = sut.flatten_payload_for_slack_workflow_builder(e)
    assert len(new_payload.keys()) <= SLACK_WORKFLOW_BUILDER_WEBHOOK_VARIABLES_MAX
    assert_dict_is_flat(new_payload)
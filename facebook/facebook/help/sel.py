from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from jsonpath_ng.ext import parse

def all_comments(body: HtmlResponse) -> list:
    return body.xpath("//div[contains(@class, 'userContentWrapper')]").extract()

def get_if_exists(selector, xpath: str) -> str:
    content = selector.xpath(xpath).extract()
    if len(content) > 0:
        return content[0]
    
    return "N/A"

def get_int_if_exists(selector, xpath: str) -> int:
    content = selector.xpath(xpath).extract()
    if len(content) > 0:
        return int(content[0])
    
    return 0

def get_comment_number(selector) -> int:
    content = selector.xpath("//a[@data-comment-prelude-ref]/text()").extract()
    if len(content) > 0:
        return int(content[0].split(" ")[0])
    
    return 0

def get_name(selector) -> str:
    private_name = get_if_exists(selector, "//span[@class='fwb fcg']//span[contains(@class, '_39_n')]/text()")
    if private_name == "N/A":
        return get_if_exists(selector, "//span[@class='fwb fcg']//a/text()")
    
    return private_name

def contains_node(selector, xpath: str) -> bool:
    nodes = selector.xpath(xpath)
    return len(nodes) > 0

def get_comment_content(selector) -> str:
    content = selector.xpath("//div[@data-ad-preview='message']//text()").extract()
    if len(content) > 0:
        return "".join(content)

    return "N/A"

def comment_data(comment: str) -> dict:
    selector = HtmlResponse(url="", body=comment, encoding="utf-8")

    data = {
        "link": get_if_exists(selector, "//span[@class='fwb fcg']//a/@href"),
        "name": get_name(selector),
        "comment": get_comment_content(selector),
        "timestamp": get_int_if_exists(selector, "//span[contains(@class, 'timestampContent')]/parent::abbr/@data-utime"),
        "tagged": contains_node(selector, "//span[@class='fcg'][contains(., 'was mentioned in a')]"),
        "cid": get_int_if_exists(selector, "//input[@name='ft_ent_identifier' and @type='hidden']/@value")
    }

    return data

def first_user(body: HtmlResponse) -> str:
    return body.xpath("//div[contains(@class, 'userContentWrapper')]//span[@class='fwb fcg']//a/text()").extract()[0]


def meta_comment_ids(json_body) -> list:
    legacy_ids = list(parse('$..require..comments..legacyid').find(json_body))
    facebook_ids = list(parse('$..require..comments..ftentidentifier').find(json_body))

    ids: list = []

    if len(legacy_ids) != len(facebook_ids):
        return ids
    
    for i in range(len(legacy_ids)):
        ids.append(facebook_ids[i].value + "_" + legacy_ids[i].value)
    
    return ids


def meta_comments(json_body: dict) -> list:
    links = list(parse("$..require..profiles..uri").find(json_body))
    full_names = list(parse("$..require..profiles..name").find(json_body))
    first_names = list(parse("$..require..profiles..firstName").find(json_body))
    uids = list(parse("$..require..profiles..id").find(json_body))

    comments = list(parse('$..require..comments..body').find(json_body))
    authors = list(parse('$..require..comments..author').find(json_body))
    comment_ids = meta_comment_ids(json_body)
    
    commenters: list = []

    if len(comments) is not len(authors) or (len(links) is not len(full_names) or len(links) is not len(uids)):
        print("length mismatch :(")
        return commenters

    meta_comments = create_meta_comments(uids, comments, authors, comment_ids)

    for i in range(len(links)):
        commenters.append({
            "name": full_names[i].value,
            "link": links[i].value,
            "uid": uids[i].value,
            "comments": meta_comments[i]
        })
    
    return commenters


# def extract_last_name(first_name: str, full_name: str) -> str:
#     return full_name[len(first_name) + 1:]

def create_meta_comments(user_ids: list, comments: list, authors: list, comment_ids: list) -> list:
    # Returns a list of lists of dicts. 
    # The outer list should be the same length as user_ids.
    meta_comments: list = []

    for i in range(len(user_ids)):
        meta_comments.append([])
        for j in range(len(authors)):
            if authors[j].value == user_ids[i].value:
                meta_comments[i].append({
                    "comment": comments[j].value["text"],
                    "info": comments[j].value["ranges"],
                    "id": comment_ids[j],
                })
    
    return meta_comments

def reactions(response, kind: str) -> list:
    names = response.xpath("//li//a[@data-gt and @data-hovercard]/text()")
    links =  response.xpath("//li//a[@data-gt and @data-hovercard]/@href")

    reactions: list = []

    if len(names) != len(links):
        print("Non-fatal error: Reaction links and names mismatched")
        return reactions

    for i in range(len(names)):
        reactions.append({
            "kind": kind,
            "user_details": {
                "name": names[i].extract(),
                "link": links[i].extract()
            }
        })

    return reactions

def meta_comment_reacts(json_body: dict) -> list:
    reaction_body = list(parse
    ("$..jsmods..markup..__html").find(json_body))

    if len(reaction_body) == 0:
        return []

    return reactions(Selector(text=reaction_body[0].value), "unknown")


# "https://www.facebook.com/pages_reaction_units/more/?page_id=1657775594549456&cursor=%7B%22timeline_cursor%22%3A%222645646350%22%2C%22timeline_section_cursor%22%3Anull%2C%22has_next_page%22%3Afalse%7D&surface=www_pages_community_tab&unit_count=8&__user=100029134355964&__a=1"

path = "https://www.facebook.com/pages_reaction_units/more/?"
page_id_param = "&page_id={pid}"
user_id_param = "&__user={uid}"
cursor = "&cursor=%7B%22timeline_cursor%22%3A%{cn}%22%2C%22timeline_section_cursor%22%3Anull%2C%22has_next_page%22%3Afalse%7D"
remaining_params = "&surface=www_pages_community_tab&unit_count=8&__a=1"

def page_url(page_id: int, user_id: int) -> str:
    return "".join([
            path,
            page_id_param.format(pid=page_id),
            cursor,
            user_id_param.format(uid=user_id),
            remaining_params,
    ])

react_url = "https://www.facebook.com/ufi/reaction/profile/browser/fetch/?limit=500&reaction_type={reaction_id}&total_count=1&ft_ent_identifier={cid}&dpr=1&__a=1"

def reaction_url(user_id: int) -> str:
        return react_url + user_id_param.format(uid=user_id)

def meta_comment_url() -> str:
        return "https://www.facebook.com/ajax/ufi/comment_fetch.php?dpr=1"

def meta_comment_body(user_id: int) -> str:
        # NOTE, you might have to change fb_dtsg
        return "ft_ent_identifier={cid}&length=22&__a=1&fb_dtsg=AQHhxQX9ZtFX:AQGaX9MIrn6k" + user_id_param.format(uid=user_id)

def meta_comment_react(user_id: int) -> str:
        return "https://www.facebook.com/ufi/reaction/profile/dialog/?ft_ent_identifier={mcid}&dpr=1&__asyncDialog=1&__a=1&__req=6y&__rev=4497859&__spin_r=4497859&__spin_b=trunk&__spin_t=1541277517" + user_id_param.format(uid=user_id)
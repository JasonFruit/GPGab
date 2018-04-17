import users

for user in users.search_users("hadley"):
    print(user.user_ids[0].name, [uid.email for uid in user.user_ids])

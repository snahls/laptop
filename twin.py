import twint
import pandas as pd
birth = ["#birth", "#childbirth", "#christening", "#childbearing"]
birthday = ["#hbd", "#birthday"]
marriage = ["#marriage", "#wedding", "#announcements", "#marriagegoals", "#hooked"]
vacation = ["#vacation", "#islandlife", "#travel", "#travelphotography", "#holidays", "#roadtrip", "#trip", "#adventure"]
graduation = ["#graduation", "#graduationday", "#graduate", "#graduating"]
career = ["#careergoals", "#newjob", "#gothired", "#firstdayfeeling"]
relocation = ["#movingto", "#housing", "#relocate", "#relocation"]



import os



filename = "birthday.csv"
df = pd.DataFrame(columns = ['id', 'tweet'],dtype = object)
df.to_csv(filename, sep=',', index=False)


for hashtag in birthday: 
    if os.path.exists("tag.csv"):
        os.remove("tag.csv")
    c = twint.Config()
    print(hashtag)
    c.Search = hashtag
    c.Limit = 5000
    c.Store_csv = True
    c.Output = "tag.csv"
    c.Lang = "en"
    twint.run.Search(c)
    if os.path.exists("tag.csv"):
        import pandas as pd
        data = pd.read_csv("tag.csv")
        print(len(data))
        data = data[data['language'] == 'en']
        print(len(data))
        data = data[data['urls'] == '[]']
        print(len(data))
        data = data[data['photos'] == '[]']
        print(len(data))
        data = data[data['retweet'] == False]
        print(len(data))
        data = data[data['video'] == 0]
        print(len(data))
        data[['id','tweet']].dropna().to_csv(filename, sep=',', index=False, mode='a', header=False)
        print(len(data))


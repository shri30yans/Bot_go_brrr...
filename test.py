import utils.awards as awards
all_award_names=[]
for award in list(awards.awards_list.values())[::-1]:
    all_award_names.append(award.name.lower())
    print(all_award_names)

# bad_teams = set()

# bad = [3,4]

# new = [2, 1, 3]

# bad_teams.add(tuple(sorted(bad)))

# if not tuple(sorted(new)) in bad_teams:
#     print("not in team")
# else:
#     print("it is in team")


# for s in bad_teams:
#     if set(new).issuperset(set(s)):
#         print("in team")
#     else:
#         print("not in team")

# for i in range(10):
#     bad_teams.add(tuple(sorted(new)))
# print(bad_teams)



# print(set(new) == (set(bad)))

bad_teams = set()
good_teams = set()

a = [1, 2]
bad_teams.add(tuple(sorted(a)))
a = [1, 3]
bad_teams.add(tuple(sorted(a)))

a = [2, 3, 4]
good_teams.add(tuple(sorted(a)))


def check(mission_success, mission):
    good_teams_copy = good_teams.copy()
    if mission_success:
        if not tuple(sorted(mission)) in bad_teams:
            is_super = False
            for bt in bad_teams:
                if set(mission).issuperset(set(bt)):
                    is_super = True
            if not is_super:
                good_teams.add(tuple(sorted(mission)))
    else:
        for gt in good_teams_copy:
            if set(gt).issuperset(set(mission)) or set(gt) == set(mission):
                good_teams.remove(gt)

        bad_teams.add(tuple(sorted(mission)))



print(bad_teams)
print(good_teams)
print()
mission = [2, 3, 4]
check(False, mission)

print(bad_teams)
print(good_teams)
from trueskill import Rating, quality_1vs1, rate_1vs1, quality, rate
alice, bob = Rating(25), Rating(30)  # assign Alice and Bob's ratings
if quality_1vs1(alice, bob) < 0.50:
    print('This match seems to be not so fair')
alice, bob = rate_1vs1(alice, bob)  # update the ratings after the match

print('\n\nHey there')

r1 = Rating()
r2 = Rating()

print('{:.1%} chance to draw'.format(quality_1vs1(r1, r2)))

new_r1, new_r2 = rate_1vs1(r1, r2, drawn=True)
print(new_r1)
print(new_r2)


r1 = Rating()  # 1P's skill
r2 = Rating()  # 2P's skill
r3 = Rating()  # 3P's skill
t1 = [r1]  # Team A contains just 1P
t2 = [r2, r3]  # Team B contains 2P and 3P

print('{:.1%} chance to draw'.format(quality([t1, t2])))
#13.5% chance to draw
(new_r1,), (new_r2, new_r3) = rate([t1, t2], ranks=[0, 1])
print(new_r1)
#trueskill.Rating(mu=33.731, sigma=7.317)
print(new_r2)
#trueskill.Rating(mu=16.269, sigma=7.317)
print(new_r3)

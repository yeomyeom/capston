import pickle
save_dir1 = 'intersection.pickle'  # 저장 경로
save_dir2 = 'adv_difference.pickle'
save_dir3 = 'nonadv_difference.pickle'
with open(save_dir1, "rb") as f1:
    intersection = pickle.load(f1)
print("교집합",intersection)
with open(save_dir2, "rb") as f2:
    adv_difference = pickle.load(f2)
print("광고성 차집합",adv_difference)
with open(save_dir3, "rb") as f3:
    nonadv_difference = pickle.load(f3)
print("비광고성 차집합",nonadv_difference)
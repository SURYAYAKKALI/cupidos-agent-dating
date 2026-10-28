import json

with open('dataset_instagram-scraper_2026-10-28_12-31-22-594.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total profiles in dataset: {len(items)}")
for i, item in enumerate(items):
    u = item.get("username", "") or ""
    fn = item.get("fullName", "") or ""
    bio = (item.get("biography", "") or "").replace("\n", " ")[:60]
    posts = item.get("postsCount", 0)
    followers = item.get("followersCount", 0)
    # safe ascii
    safe_line = f"{i+1:2d}. @{u:20s} | {fn:25s} | Followers: {followers:10d} | Posts: {posts:4d} | Bio: {bio}"
    print(safe_line.encode("ascii", "replace").decode("ascii"))

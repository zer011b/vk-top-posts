import argparse
import vk

# Limit, set by vk api for wall.get (see https://vk.com/dev/wall.get)
const_vk_max_wall_get_count=100

# Limit on number of wall.get requests (see https://vk.com/dev/data_limits)
const_vk_max_wall_get=5000

# Version of VK API
cont_vk_api_version="5.103"

# Checks =======================================================================
# Check that string is >=0 int value
def is_positive(string):
  value = int(string)
  if value < 0:
    msg = "%r should be >= 0" % string
    raise argparse.ArgumentTypeError(msg)
  return value

# Check that string is not empty
def is_not_empty(string):
  if string == "":
    msg = "Parameter should be non-empty"
    raise argparse.ArgumentTypeError(msg)
  return string

# VK API =======================================================================
# Get object id and type from url
def vk_utils_resolveScreenName(api, url):
  name=url.split("/")[-1]
  res = api.utils.resolveScreenName(screen_name=name)
  #return (res.get("type"), int(res.get("object_id")))
  return int(res.get("object_id"))

# Get posts on the wall
def vk_wall_get(api, owner_id, domain, offset, count, filter, extended, fields):
  return api.wall.get(owner_id=-owner_id,
                      domain=domain,
                      offset=offset,
                      count=count,
                      filter=filter,
                      extended=extended,
                      fields=fields)

# Get posts on the wall with predetermined & unused data
def vk_wall_get_simple(api, owner_id, offset, count):
  return vk_wall_get(api, owner_id, "", offset, count, "owner", 0, "")

# VK API Python wrapper (https://github.com/voronind/vk) =======================
def create_vk_session(token):
  return vk.Session(access_token=token)

def create_vk_api(session):
  return vk.API(session, v=cont_vk_api_version)

# Output =======================================================================
# Get post url from ids
def get_post_url(wall_id, post_id):
  return "https://vk.com/wall-" + str(wall_id) + "_" + str(post_id)

def show_post(index, post):
  print(str(index) + ") " + post.get("post_url") + " : "
        + "likes(" + str(post.get("likes")) + "), "
        + "comments(" + str(post.get("comments")) + "), "
        + "reposts(" + str(post.get("reposts")) + "), "
        + "views(" + str(post.get("views")) + "), ")

def show_posts(posts, count):
  print("\n----------------------------------------------------------------")
  for i in range(count):
    show_post(i, posts[i])

# Wall posts analysis ==========================================================
# Parse single wall.get request and return count of received posts
def parse_request(posts, api, id, offset, count):
  if count == 0:
    return 0

  res = vk_wall_get_simple(api, id, offset, count)
  items = res.get("items")
  size = len(items)
  for i in range(size):
    post_id = items[i].get("id")

    likes = items[i].get("likes").get("count");
    comments = items[i].get("comments").get("count")
    reposts = items[i].get("reposts").get("count")
    views = 0
    if items[i].get("views") != None:
      views = items[i].get("views").get("count")

    posts.append({'raw': items[i],
                  'post_id': post_id,
                  'post_url': get_post_url(id, post_id),
                  'likes': likes,
                  'comments': comments,
                  'reposts': reposts,
                  'views': views})
  return size


# Analyze specified amount of posts
def analyze_count(api, num_posts, id, top_count, url, sort_str):
  if num_posts <= 0 or top_count <= 0:
    return

  print("Analyzing " + str(num_posts) + " posts from " + url)

  posts=[]

  num_iterations = num_posts // const_vk_max_wall_get_count
  left_offset = num_iterations * const_vk_max_wall_get_count
  left_count = num_posts - left_offset

  size = 0

  for i in range(num_iterations):
    size += parse_request(posts, api, id, i * const_vk_max_wall_get_count, const_vk_max_wall_get_count)

  size += parse_request(posts, api, id, left_offset, left_count)

  print("...received " + str(size) + " posts...")

  print("...showing " + str(top_count) + " top posts by " + sort_str + "...")

  sorted_posts = sorted(posts, key=lambda post: post.get(sort_str), reverse=True)
  show_posts(sorted_posts, min(top_count,len(sorted_posts)))


def main ():
  parser = argparse.ArgumentParser()
  parser.add_argument("--count", help="specify the amount of posts to analyze",
                      type=is_positive, default=0)
  parser.add_argument("--url", help="specify the url of group (club), user, etc.",
                      type=is_not_empty, default="")
  parser.add_argument("--top", help="specify the amount of top posts to be shown",
                      type=is_positive, default=1)
  parser.add_argument("--access-token", help="specify access token",
                      type=is_not_empty, default="")
  parser.add_argument("--likes", help="sort by likes", action="store_true")
  parser.add_argument("--comments", help="sort by comments", action="store_true")
  parser.add_argument("--reposts", help="sort by reposts", action="store_true")
  parser.add_argument("--views", help="sort by views", action="store_true")
  args = parser.parse_args()

  vk_session = create_vk_session(args.access_token)
  vk_api = create_vk_api(vk_session)

  id = vk_utils_resolveScreenName(vk_api, args.url)

  sort_str = "likes"
  if args.likes:
    sort_str = "likes"
  elif args.comments:
    sort_str = "comments"
  elif args.reposts:
    sort_str = "reposts"
  elif args.views:
    sort_str = "views"

  if args.count > 0:
    analyze_count(vk_api, args.count, id, args.top, args.url, sort_str)


if __name__ == "__main__":
    # execute only if run as a script
    main()

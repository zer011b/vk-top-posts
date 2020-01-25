This is vk.com group walls parser for top posts.

# Prerequisites

```
pip install vk
```

# Usage

```
python3 parse.py --help
```

Typical usage example:
```
python3 parse.py --count 100 --id <group_id> --show-top 10 --access-token <token>
```

Access token can be obtained from service token of standalone app (https://vk.com/dev/service_token). To create standalone app, see https://vk.com/dev/standalone.

# TODO

- sort by likes, comments, reposts, views
- add start/end date mode

This is vk.com walls parser, which shows top posts. Sorting can be done by likes, comments, reposts and views.

# Prerequisites

```
pip install vk
```

# Usage

```
python3 parse.py --help
```

There are two modes:

1. Parse N latest posts:
```
python3 parse.py --count <N> --url <url> --top <M> --access-token <token> --likes
```

2. Parse all posts from start date to end date
```
python3 parse.py --start-date <dd/mm/yyyy> --end-date <dd/mm/yyyy> --url <url> --top <M> --access-token <token> --likes
```

Access token can be obtained from service token of standalone app (https://vk.com/dev/service_token). To create standalone app visit https://vk.com/dev/standalone.

# TODO

- download attachments automatically

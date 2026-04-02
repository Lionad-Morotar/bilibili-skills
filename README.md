# bilibili-skills

Claude Skill for Bilibili operations — browse videos, search, download audio, manage interactions, and automate workflows.

## Installation

```bash
cd ~/.claude
npx skills add https://github.com/Lionad-Morotar/bilibili-skills
```

## Usage

```sh
/bilibili {your command}
```

If your IDE doesn't support SlashCommands, add a prefix to your prompt:

```plaintext
使用 bilibili 技能，{your command}
```

This ensures the AI follows the documented patterns. Without the prefix, skill triggering may be inconsistent depending on how well your prompt matches the skill description keywords.

## Features

- Video information & metadata extraction
- Audio download with ASR-ready segmentation
- Search videos and users
- Hot rankings and trending feeds
- Favorites and watch-later management
- Social interactions (like, coin, triple)
- Structured output (YAML/JSON) for automation

## Prerequisites

Install bilibili-cli:

```bash
uv tool install bilibili-cli
# or with audio support
uv tool install "bilibili-cli[audio]"
```

Then login:

```bash
bili login
```

## License

MIT

---

thanks:
- https://github.com/jackwener/bilibili-cli
- https://nemo2011.github.io/bilibili-api
